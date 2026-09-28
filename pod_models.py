import numpy as np
from scipy.stats import chi2
from sklearn.linear_model import LogisticRegression


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def logits(X, θ_0, Θ):
    return θ_0 + (X * Θ).sum(-1)


def PoD(X, θ_0, Θ):
    return sigmoid(logits(X, θ_0, Θ))


def DNVGL(a):
    """
    PoD curve recommendation from the DNVGL report [1].

    [1] Probabilistic Methods for Planning of Inspection for Fatigue Cracks in
        Offshore Structures (Recommended Practice DNVGL-RP-C210, 2015).
        url: https://www.dnv.com/energy/standards-guidelines/dnv-rp-c210-probabilistic-methods-for-planning-of-inspection-for-fatigue-cracks-in-offshore-structures/
    """
    return 1.0 - 1.0 / (1.0 + (a / 37.15) ** 0.954)


def Campbell(a):
    """
    PoD curve as determined by Campbell et al. [1].

    [1] Probability of Detection Study for Visual Inspection of Steel Bridges:
        Volume 2-Full Project Report (2019). L.E. Campbell, L.R. Snyder,
        J.M. Whitehead, R.J. Connor, and J.B. Lloyd.
        doi: 10.5703/1288284317104
    """
    return PoD(a[..., None], -1.01 / 2.0263, np.array([1.0 / 2.0263 * 0.0393701]))


def log_likelihood(Z, X, θ_0, Θ):
    l = logits(X, θ_0, Θ)
    return (Z * l - np.logaddexp(0, l)).sum(axis=-1)


def negative_log_likelihood_ratio(Z, X, θ_0_null, Θ_null, θ_0_MLE, Θ_MLE):
    ll_null = log_likelihood(Z, X, θ_0_null, Θ_null)
    ll_MLE = log_likelihood(Z, X, θ_0_MLE, Θ_MLE)
    return -2 * (ll_null - ll_MLE)


def χ_sq(df, α):
    return chi2.isf(α, df)


def χ_sq_p(df, s):
    return chi2.sf(s, df)


def fit_model(X, Z):
    logistic_regression = LogisticRegression(C=np.inf)
    fitted_model = logistic_regression.fit(X, Z)
    θ_0_MLE, Θ_MLE = fitted_model.intercept_[0], fitted_model.coef_[0]
    return θ_0_MLE, Θ_MLE


def train_and_validate(training_X, training_Z, validation_X, validation_Z):
    θ_0_MLE, Θ_MLE = fit_model(training_X, training_Z)
    return log_likelihood(validation_Z, validation_X, θ_0_MLE, Θ_MLE)


def minimum_missed_cracks(results):
    return min(stats["missed_crack_count"] for stats in results.values())


def MC_simulation(
    inspection_methods,
    prior_mean,
    prior_coefficient_of_variation,
    num_samples=100000,
    batch_size=1000,
    rng=None,
):
    if prior_mean <= 0:
        raise ValueError("mean must be positive")
    if prior_coefficient_of_variation <= 0:
        raise ValueError("coefficient_of_variation must be positive")
    if rng is None:
        rng = np.random.default_rng

    σ = prior_coefficient_of_variation * prior_mean
    σ_log = np.sqrt(np.log(1 + σ**2 / prior_mean**2))
    μ_log = np.log(prior_mean**2 / np.sqrt(σ**2 + prior_mean**2))

    results = dict()
    for name, curve in inspection_methods.items():
        results[name] = dict(
            model=curve,
            missed_cracks=[],
            missed_crack_count=0,
        )

    cracks = []
    crack_count = 0

    min_missed_cracks = 0
    while min_missed_cracks < num_samples:
        print(
            f"Generated {crack_count} cracks, Minimum missed cracks: {min_missed_cracks}/{num_samples}",
            end="\r",
        )
        crack_length_mm = rng.lognormal(mean=μ_log, sigma=σ_log, size=batch_size)
        cracks.append(crack_length_mm)
        crack_count += batch_size

        for curve in results.values():
            detection_probability = curve["model"](crack_length_mm)
            comparison = rng.uniform(0, 1, batch_size)
            missed_cracks = detection_probability < comparison
            curve["missed_cracks"].append(crack_length_mm[missed_cracks])
            curve["missed_crack_count"] += missed_cracks.sum()

        min_missed_cracks = minimum_missed_cracks(results)
    print("\r")

    cracks = np.concatenate(cracks)
    for curve in results.values():
        curve["missed_cracks"] = np.concatenate(curve["missed_cracks"])

    results["generated_cracks"] = cracks

    return results


def metric_KL(s_1, scale_1, s_2, scale_2):
    return (
        np.log(s_2 / s_1)
        + (s_1**2 + np.log(scale_1 / scale_2) ** 2) / (2 * s_2**2)
        - 0.5
    )


def metric_C(missed_crack_length, total_crack_length):
    return missed_crack_length / total_crack_length

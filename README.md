# About
Code and data accompanying "A Statistical Approach for Evaluation of Automated Visual Crack Detection Using Probability of Detection" [[1]](#1).

# Inspection method comparison framework
The primary contribution of [[1]](#1) is a framework to allow for the quantitative comparison of different inspection methods for e.g. crack detection in steel bridges. In the next sections, we 
- describe how to structure inspection data in order to use our code on your inspection method, and 
- explain the contents of the scripts and notebooks that are relevant to the comparison framework.

## Data for fitting PoD models
The notebooks in this repository (described below) determine PoD curves from inspection data. One can provide one's own inspection method data; to be able to run the notebooks as is, this should be Excel `.xlsx` files, containing at least the following columns: 
- `data_statistics.ipynb`: `length_mm`, `length_pix`, `tp_probs`, `fp_probs`, and `Detection_hit_miss`. 
- `general_pod.ipynb`: `length_mm` and `Detection_hit_miss`. 
- `resolution_effect.ipynb`: `length_mm`, `length_pix`, and `Detection_hit_miss`. 

The column `length_mm` gives the length of the crack in millimetres; `length_pix` gives the length of the crack in pixels; `tp_probs` gives the detection score of any bounding box considered sufficiently close to the ground truth bounding box; `fp_probs` gives the detection score of any bounding box considered sufficiently far away from the ground truth bounding box; `Detection_hit_miss` gives the highest detection score among all of the bounding box considered sufficiently close to the ground truth bounding box.

## Contents of notebooks
- `pod_models.py`: Basic functions to define, fit, and test the PoD models.
- `data_statistics.ipynb`: Exploration of the data statistics. Used to generate Figs. 2, 4, 5, 12 in [[1]](#1).
- `general_pod.ipynb`: Fit the crack length PoD curve model on our CV method's inspection capability, determine confidence bounds, and compare to the PoD curves from the DNVGL recommendation [[2]](#2) and determined by Campbell et al. [[3]](#3). Used to generate Fig. 6 in [[1]](#1).
- `resolution_effect.ipynb`: Fit the crack length and resolution curve models, using the parametric and the binning approach, on our CV method's inspection capability and compare to the PoD curves from the DNVGL recommendation [[2]](#2) and determined by Campbell et al. [[3]](#3). Used to generate Figs. 13, 14, 15 in [[1]](#1).
- `MC_sim.ipynb`: Apply comparison framework Alg. 1 from [[1]](#1) to the PoD curves fitted in `general_pod.ipynb` and `resolution_effect.ipynb` and the PoD curves from the DNVGL recommendation [[2]](#2) and determined by Campbell et al. [[3]](#3). Used to generate Fig. 9, Figs. A.18-A.29, Tabs. 1-3.

# Cite
If you use this code in your own work, please cite our paper:

<a id="1">[1]</a> Kompanets, A., Sherry, F.M., Duits, R., Leonetti, D., Snijder, H.H. "A Statistical Approach for Evaluation of Automated Visual Crack Detection Using Probability of Detection." arXiv preprint (2026). https://doi.org/10.48550/arXiv.XXXX.YYYYY
```
@article{Kompanets2026StatisticalDetection,
  title       = {A Statistical Approach for Evaluation of Automated Visual Crack Detection Using Probability of Detection},
  author      = {Kompanets, Andrii and Sherry, Finn M. and Duits, Remco and Leonetti, Davide and Snijder, H.H. (Bert)},
  journal     = {arXiv preprint},
  year        = {2026},
  pages       = {1--40},
  doi         = {10.48550/arXiv.XXXX.YYYYY},
}
```

We compare to the PoD curve in the DNVGL recommendation:

<a id="2">[2]</a> DNV GL. "Probabilistic Methods for Planning of Inspection for Fatigue Cracks in Offshore Structures." (DNVGL-RP-C210, 2015). https://www.dnv.com/energy/standards-guidelines/dnv-rp-c210-probabilistic-methods-for-planning-of-inspection-for-fatigue-cracks-in-offshore-structures/
```
@techreport{DNVGL_RP_C210_2015,
  title        = {Probabilistic Methods for Planning of Inspection for Fatigue Cracks in Offshore Structures},
  institution  = {{DNV GL}},
  number       = {DNVGL-RP-C210},
  type         = {Recommended Practice},
  year         = {2015},
  url          = {https://www.dnv.com/energy/standards-guidelines/dnv-rp-c210-probabilistic-methods-for-planning-of-inspection-for-fatigue-cracks-in-offshore-structures/},
}
```

We also compare to the PoD curve measured by Campbell et al:

<a id="3">[3]</a> Campbell, L.E., Snyder, L.R., Whitehead, J.M., Connor, R.J., Lloyd, J.B. "Probability of Detection Study for Visual Inspection of Steel Bridges: Volume 2—Full Project Report." Indiana. Dept. of Transportation (2019). https://doi.org/10.5703/1288284317104
```
@techreport{Connor2019ProbabilityReport,
  title         = {Probability of {D}etection {S}tudy for {V}isual {I}nspection of {S}teel {B}ridges: {V}olume 2—{F}ull {P}roject {R}eport},
  author        = {Campbell, L.E. and Snyder, L.R. and Whitehead, J.M. and Connor, R.J. and Lloyd, J.B.},
  year          = {2019},
  institution   = {Indiana. Dept. of Transportation},
  doi           = {10.5703/1288284317104}
}
```
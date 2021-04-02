"""Library of statisitical algorithms to fit biodemographic functions
included in module bdm_lib.py for modeling basic biological processes in any
organism using physiologically based demographic models (PBDMs, see
https://doi.org/10.1111/epp.12224).
"""

import numpy as np

from lmfit import Model, Parameters, report_fit
from .bdm_plot import get_development_rates

# Data:
# Experimental temperatures
temperature_list_tuta = [10, 15, 20, 25, 30, 17, 22, 26, 28, 30, 33, 14, 19,
                         27, 6, 10, 15, 20, 25, 30, 33, 36]
# Developmental rates measured at the experimental temperatures above
development_rate_list_tuta = [0.0087, 0.0156, 0.0286, 0.0435, 0.0556, 0.0154,
                              0.0312, 0.0417, 0.0500, 0.0500, 0.0588, 0.0131,
                              0.0250, 0.0417, 0.0080, 0.0099, 0.0173, 0.0276,
                              0.0409, 0.0508, 0.0546, 0]


pars = Parameters()

""" Place math constraint that
upper_temperature_threshold >= lower_temperature_threshold
https://lmfit.github.io/lmfit-py/constraints.html """
pars.add('lower_temperature_threshold', value=1, vary=True, min=-100, max=100)
pars.add('delta', value=1, min=0, vary=True)
pars.add('upper_temperature_threshold', vary=True, min=-100, max=100,
         expr='lower_temperature_threshold+delta')

pars.add('a_scale_parameter', min=0)
pars.add('b_shape_parameter', min=0)

# Model:
model = Model(get_development_rates, independent_vars=['temperature_list'])

result = model.fit(development_rate_list_tuta,
                   temperature_list=temperature_list_tuta,
                   nan_policy='propagate')

print(result.values)

# Check out
# https://lmfit.github.io/lmfit-py/
# https://zenodo.org/badge/DOI/10.5281/zenodo.4516651.svg
# https://mike.depalatis.net/blog/lmfit.html

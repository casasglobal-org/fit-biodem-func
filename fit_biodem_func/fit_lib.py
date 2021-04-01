"""Library of statisitical algorithms to fit biodemographic functions
included in module bdm_lib.py for modeling basic biological processes in any
organism using physiologically based demographic models (PBDMs, see
https://doi.org/10.1111/epp.12224).
"""

import numpy as np

from lmfit import Model, Parameter, report_fit
from bdm_lib import development_rate

# Data:

# Experimental temperatures
temperature_list = [10, 15, 20, 25, 30, 17, 22, 26, 28, 30, 33, 14, 19, 27, 6,
                    10, 15, 20, 25, 30, 33, 36]
# Developmental rates measured at the experimental temperatures above
development_rate_list_tuta = [0.0087, 0.0156, 0.0286, 0.0435, 0.0556, 0.0154,
                              0.0312, 0.0417, 0.0500, 0.0500, 0.0588, 0.0131,
                              0.0250, 0.0417, 0.0080, 0.0099, 0.0173, 0.0276,
                              0.0409, 0.0508, 0.0546, 0]

# Model:
model = Model(development_rate, independent_vars=['temperature'])
result = model.fit(development_rate_list_tuta,
                   temperature=temperature_list)

print(result.values)

# Check out
# https://lmfit.github.io/lmfit-py/
# https://zenodo.org/badge/DOI/10.5281/zenodo.4516651.svg
# https://mike.depalatis.net/blog/lmfit.html

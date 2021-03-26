"""Library of statisitical algorithms to fit biodemographic functions
included in module bdm_lib.py for modeling basic biological processes in any
organism using physiologically based demographic models (PBDMs, see
https://doi.org/10.1111/epp.12224).
"""

import lmfit

from bdm_lib import development_rate


# Check out
# https://lmfit.github.io/lmfit-py/
# https://zenodo.org/badge/DOI/10.5281/zenodo.4516651.svg
# https://mike.depalatis.net/blog/lmfit.html

f = Parameter(name (str) – Name of the Parameter,
    value (float, optional) – Numerical Parameter value.
    vary (bool, optional) – Whether the Parameter is varied during a fit (default is True).
    min (float, optional) – Lower bound for value (default is -numpy.inf, no lower bound).
    max (float, optional) – Upper bound for value (default is numpy.inf, no upper bound).
    expr (str, optional) – Mathematical expression used to constrain the value during the fit (default is None).
    brute_step (float, optional) – Step size for grid points in the brute method (default is None).
    user_data (optional) – User-definable extra attribute used for a Parameter (default is None).)

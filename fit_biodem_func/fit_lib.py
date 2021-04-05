"""Library of statisitical algorithms to fit biodemographic functions
included in module bdm_lib.py for modeling basic biological processes in any
organism using physiologically based demographic models (PBDMs, see
https://doi.org/10.1111/epp.12224).
"""

import numpy as np
import lmfit

# from .bdm_lib import development_rate

# Data:
# Experimental temperatures
temperature_list_tuta = np.array([10, 15, 20, 25, 30, 17, 22, 26, 28, 30, 33,
                                  14, 19, 27, 6, 10, 15, 20, 25, 30, 33, 36])
# Developmental rates measured at the experimental temperatures above
development_rate_list_tuta = np.array([0.0087, 0.0156, 0.0286, 0.0435, 0.0556,
                                       0.0154, 0.0312, 0.0417, 0.0500, 0.0500,
                                       0.0588, 0.0131, 0.0250, 0.0417, 0.0080,
                                       0.0099, 0.0173, 0.0276, 0.0409, 0.0508,
                                       0.0546, 0])


class DevelopmentRateModel(lmfit.Model):
    def __init__(self, *args, **kwargs):
        def development_rate(
            temperature,
            a_scale_parameter,
            b_shape_parameter,
            lower_temperature_threshold,
            upper_temperature_threshold
        ):
            """Temperature-dependent developmental rate modified from
                Briere et al(1999) https://doi.org/10.1093/ee/28.1.22
                a_scale_parameter, b_shape_parameter are constants
                lower_temperature_threshold, upper_temperature_threshold
                are lower and upper thermal thresholds
                temperature_series is a list of temperatures."""
            development_rate = (
                a_scale_parameter
                * (temperature - lower_temperature_threshold)
                / pow(1 + b_shape_parameter,
                      (temperature - upper_temperature_threshold))
            )
            return development_rate
            super(DevelopmentRateModel, self).__init__(development_rate, *args,
                                                       **kwargs)

    def guess(self, data, **kwargs):
        params = self.make_params()

        def pset(param, value):
            params["%s%s" % (self.prefix, param)].set(value=value)
        pset("a_scale_parameter", 0.0001)
        pset("b_scale_parameter", 2)
        pset("lower_temperature_threshold", np.min(data))
        pset("upper_temperature_threshold", np.max(data))
        return lmfit.models.update_param_vals(params, self.prefix, **kwargs)


model = DevelopmentRateModel()
params = model.guess(development_rate_list_tuta, temperature=temperature_list_tuta)
fit = model.fit(development_rate_list_tuta, params, temperature=temperature_list_tuta)



# Check out
# https://lmfit.github.io/lmfit-py/
# https://zenodo.org/badge/DOI/10.5281/zenodo.4516651.svg
# https://mike.depalatis.net/blog/lmfit.html
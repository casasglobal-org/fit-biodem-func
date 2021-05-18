"""Library of statisitical algorithms to fit biodemographic functions
included in module bdm_lib.py for modeling basic biological processes in any
organism using physiologically based demographic models (PBDMs, see
https://doi.org/10.1111/epp.12224).
"""

from matplotlib import pyplot as plt
from .bdm_lib import development_rate
from lmfit import Parameter
import numpy as np
import lmfit
# import matplotlib
# matplotlib.use('Agg')  # https://stackoverflow.com/a/15713545/8677447

# Data:
# dtype=float hint from https://stackoverflow.com/a/43287598/8677447
# Experimental temperatures
temperature_list_tuta = np.array([10, 15, 20, 25, 30, 17, 22, 26, 28, 30, 33,
                                  14, 19, 27, 6, 10, 15, 20, 25, 30, 33, 36],
                                 dtype=float)
# Developmental rates measured at the experimental temperatures above
development_rate_list_tuta = np.array([0.0087, 0.0156, 0.0286, 0.0435, 0.0556,
                                       0.0154, 0.0312, 0.0417, 0.0500, 0.0500,
                                       0.0588, 0.0131, 0.0250, 0.0417, 0.0080,
                                       0.0099, 0.0173, 0.0276, 0.0409, 0.0508,
                                       0.0546, 0.0000], dtype=float)


class DevelopmentRateModel(lmfit.Model):
    def __init__(self, *args, **kwargs):
        super(DevelopmentRateModel, self).__init__(development_rate,
                                                   *args, **kwargs)

    def guess(self, data, temperature, **kwargs):
        params = self.make_params()

        def pset(param, value):
            params["%s%s" % (self.prefix, param)].set(value=value)
        pset("a_scale_parameter", 0.0024)
        pset("b_shape_parameter", 3.95)
        pset("lower_temperature_threshold", np.min(temperature))
        pset("upper_temperature_threshold", 40)
        return lmfit.models.update_param_vals(params, self.prefix, **kwargs)


if __name__ == "__main__":

    # Instantiate model
    model = DevelopmentRateModel(nan_policy='propagate')
    # Guess parameters
    params = model.guess(development_rate_list_tuta,
                         temperature=temperature_list_tuta)
    # Fit function
    fit = model.fit(development_rate_list_tuta, params,
                    temperature=temperature_list_tuta)
    # Print fit report
    print(fit.fit_report())
    # Plot fit results
    fit.plot_fit()
    fit.plot_residuals()
    plt.show()

    model2 = DevelopmentRateModel(nan_policy='propagate')
    result = model2.fit(development_rate_list_tuta,
                        temperature=temperature_list_tuta,
                        a_scale_parameter=Parameter(
                           'a_scale_parameter', value=0.0024, vary=False),
                        b_shape_parameter=Parameter(
                           'b_shape_parameter', value=3.95, vary=False),
                        lower_temperature_threshold=Parameter(
                           'lower_temperature_threshold',
                           value=7.9, vary=False),
                        upper_temperature_threshold=Parameter(
                           'upper_temperature_threshold',
                           value=34.95, vary=False)
                        )

    print(result.fit_report())
    result.plot_fit()
    result.plot_residuals()
    plt.show()

    # Check out
    # https://lmfit.github.io/lmfit-py/
    # https://doi.org/10.5281/zenodo.4516651
    # https://mike.depalatis.net/blog/lmfit.html

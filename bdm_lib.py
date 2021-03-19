"""Library of bio-demographic functions for modeling basic biological
processes in any organism using physiologically based demographic models
(PBDMs, see https://doi.org/10.1111/epp.12224).
"""

from matplotlib import pyplot as plt
import numpy as np

# Sample parameters for the developmental rate function of Tuta absoluta
lower_temperature_threshold_tuta = 7.9
upper_temperature_threshold_tuta = 34.95
a_scale_parameter_tuta = 0.0024
b_shape_parameter_tuta = 3.95
temperatures_sample = np.linspace(-5, 40, 1000)


def development_rate(
    a_scale_parameter,
    b_shape_parameter,
    lower_temperature_threshold,
    upper_temperature_threshold,
    temperature_series
):
    """Temperature-dependent developmental rate modified from
        Briere et al(1999) https://doi.org/10.1093/ee/28.1.22
        a_scale_parameter, b_shape_parameter are constants
        lower_temperature_threshold, upper_temperature_threshold
        are lower and upper thermal thresholds
        temperature_series is a list of temperatures."""
    development_rate_series = []
    for temperature in temperature_series:
        if (
            lower_temperature_threshold <=
                temperature <= upper_temperature_threshold
                ):
            development_rate = (
                a_scale_parameter
                * (temperature - lower_temperature_threshold)
                / (1 + b_shape_parameter
                    ** (temperature - upper_temperature_threshold))
            )
        else:
            development_rate = 0
        development_rate_series.append(development_rate)
    return development_rate_series


def plot_bdm_func(
    x_data, y_data, title, x_label, y_label,
    lower_temperature_threshold,
    upper_temperature_threshold
):
    """Plot biodemographic function to see how it looks."""
    plt.plot(x_data, y_data)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.xlim((lower_temperature_threshold, upper_temperature_threshold))
    plt.show()


if __name__ == "__main__":
    # Compute developmental rates for Tuta absoluta
    development_rate_series_tuta = development_rate(
        a_scale_parameter_tuta,
        b_shape_parameter_tuta,
        lower_temperature_threshold_tuta,
        upper_temperature_threshold_tuta,
        temperatures_sample
        )

    # Plot developmental rate function for Tuta absoluta
    plot_bdm_func(
        x_data=temperatures_sample,
        y_data=development_rate_series_tuta,
        title=r"Developmental rate of $\it{Tuta\ absoluta}$",
        x_label='Temperature (°C)',
        y_label='Day$^-1$',
        lower_temperature_threshold=lower_temperature_threshold_tuta-1,
        upper_temperature_threshold=upper_temperature_threshold_tuta+1
        )


    """ The following equations need to be turned into functions
        as they are part of the libary.

    # Per capita fecundity profile on female age in days at the optimum temperature
    # from Bieri et al (1983) https://doi.org/10.5169/seals-402070

    ovip(age_days) = constant_f * days / constant_g ^ age_days


    # The oviposition scalar (originally called FFTemperature in the Pascal code

    T_scalar = 1.0 - ((T - lower_temperature_threshold_threshold - a) / a) ^ 2

    with a_scale_parameterant = (upper_temperature_threshold_threshold - lower_temperature_threshold_threshold) / 2


    # The temperature dependent mortality taken from Lobesia botrana paper
    # Gutierrez et al. (2012) https://doi.org/10.1111/j.1461-9563.2011.00566.x

    mu(T) = c_constant (T - T_min_mortality / T_min_mortality ) ^ 2

    def print_colors():

    """

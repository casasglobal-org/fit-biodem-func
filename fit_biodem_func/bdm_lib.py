"""Library of bio-demographic functions for modeling basic biological
processes in any organism using physiologically based demographic models
(PBDMs, see https://doi.org/10.1111/epp.12224).
"""


def development_rate_bounded(
    temperature,
    a_scale_parameter,
    b_shape_parameter,
    lower_temperature_threshold,
    upper_temperature_threshold,
):
    """Temperature-dependent developmental rate modified from
        Briere et al(1999) https://doi.org/10.1093/ee/28.1.22
        a_scale_parameter, b_shape_parameter are constants
        lower_temperature_threshold, upper_temperature_threshold
        are lower and upper thermal thresholds
        temperature_series is a list of temperatures."""
    development_rate_bounded = 0
    if lower_temperature_threshold < temperature < upper_temperature_threshold:
        development_rate_bounded = (
            a_scale_parameter
            * (temperature - lower_temperature_threshold)
            / (1 + b_shape_parameter
                ** (temperature - upper_temperature_threshold))
        )
    return development_rate_bounded


def development_rate(
    temperature,
    a_scale_parameter,
    b_shape_parameter,
    lower_temperature_threshold,
    upper_temperature_threshold,
):
    """Temperature-dependent developmental rate modified from
        Briere et al(1999) https://doi.org/10.1093/ee/28.1.22
        a_scale_parameter, b_shape_parameter are constants
        lower_temperature_threshold, upper_temperature_threshold
        are lower and upper thermal thresholds
        temperature_series is a list of temperatures.
        Version without temperature bounds. See development_rate_bounded"""
    development_rate = (
        a_scale_parameter
        * (temperature - lower_temperature_threshold)
        / (1 + b_shape_parameter
            ** (temperature - upper_temperature_threshold))
    )
    return development_rate



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

"""Get plotting code from bdm_lib.py, implement it here and import functions
here for modeling basic biological processes in any organism using
physiologically based demographic models (PBDMs, see https
"""

from matplotlib import pyplot as plt
import numpy as np

from bdm_lib import development_rate


# Sample parameters for the developmental rate function of Tuta absoluta
lower_temperature_threshold_tuta = 7.9
upper_temperature_threshold_tuta = 34.95
a_scale_parameter_tuta = 0.0024
b_shape_parameter_tuta = 3.95

# Sample parameters for the developmental rate function
# of Mediterranean fruit fly (Ceratitis capitata) adults
lower_temperature_threshold_medfly = 9.5
upper_temperature_threshold_medfly = 33.7
a_scale_parameter_medfly = 0.0059
b_shape_parameter_medfly = 4.8

# Some temperature-like values for plotting
temperature_list = np.linspace(-5, 40, 1000)


def plot_bdm_func(
    x_data, y_data, title, x_label, y_label,
    lower_temperature_threshold, upper_temperature_threshold
):
    """Plot biodemographic function to see how it looks."""
    plt.plot(x_data, y_data)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.xlim((lower_temperature_threshold, upper_temperature_threshold))
    plt.show()


def get_development_rates(
    temperature_list,
    a_scale_parameter, b_shape_parameter,
    lower_temperature_threshold, upper_temperature_threshold
):
    """Take a list fo temperatures and turn it into
        a list of corresponding developmental rates."""
    dev_list = []
    for temperature in temperature_list:
        dev_daily = development_rate(
                temperature,
                a_scale_parameter,
                b_shape_parameter,
                lower_temperature_threshold,
                upper_temperature_threshold,
        )
        dev_list.append(dev_daily)
    return dev_list


if __name__ == "__main__":
    # Compute developmental rates for Tuta absoluta
    development_rate_list_tuta = get_development_rates(
        temperature_list,
        a_scale_parameter_tuta,
        b_shape_parameter_tuta,
        lower_temperature_threshold_tuta,
        upper_temperature_threshold_tuta
        )

    # Compute developmental rates for Ceratitis capitata
    development_rate_list_medfly = get_development_rates(
        temperature_list,
        a_scale_parameter_medfly,
        b_shape_parameter_medfly,
        lower_temperature_threshold_medfly,
        upper_temperature_threshold_medfly,
        )

    # Plot developmental rate function for Tuta absoluta
    plot_bdm_func(
        x_data=temperature_list,
        y_data=development_rate_list_tuta,
        title=r"Developmental rate of $\it{Tuta\ absoluta}$",
        x_label='Temperature (°C)',
        y_label='Day$^-1$',
        lower_temperature_threshold=lower_temperature_threshold_tuta-2,
        upper_temperature_threshold=upper_temperature_threshold_tuta+2
        )

    # Plot developmental rate function for Ceratitis capitata
    plot_bdm_func(
        x_data=temperature_list,
        y_data=development_rate_list_medfly,
        title=r"Developmental rate of $\it{Ceratitis\ capitata}$",
        x_label='Temperature (°C)',
        y_label='Day$^-1$',
        lower_temperature_threshold=lower_temperature_threshold_medfly-2,
        upper_temperature_threshold=upper_temperature_threshold_medfly+2
        )

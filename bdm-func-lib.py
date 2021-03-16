"""Library of bio-demographic functions for modeling basic biological 
processes in any organism using physiologically based demographic models 
(PBDMs, see https://doi.org/10.1111/epp.12224)
"""
import math

import matplotlib.pyplot as plt
import numpy as np

T_l_tuta_absoluta = 7.9
T_u_tuta_absoluta = 34.95
a_tuta_absoluta = 0.0024
b_tuta_absoluta = 3.95
T_curr_sample = np.linspace(-5,40,1000)

def development_rate(a_const, b_const, T_lower, T_upper, T_curr):
    """Temperature-dependent developmental rate modified from 
        Briere et al (1999) https://doi.org/10.1093/ee/28.1.22
        a_const, b_const are constants
        T_lower, T_upper are lower and upper thermal thresholds
        T_curr is the current temperature"""
    R = []
    for T_day in T_curr:
        if T_day <= T_lower:
            R_day = 0
        elif T_day >= T_upper:
            R_day = 0
        else:
            R_day = (a_const * (T_day - T_lower)
                    / (1 + b_const ** (T_day - T_upper)))
        R.append(R_day)
    return R

plt.plot(T_curr_sample, development_rate(a_tuta_absoluta, 
    b_tuta_absoluta, 
    T_l_tuta_absoluta, 
    T_u_tuta_absoluta, 
    T_curr_sample), label = "R(t)")
plt.legend(loc = "upper left")
plt.xlabel('Temperature (°C)')
plt.ylabel('Day$^-1$')
plt.title(r"Developmental rate $\it{Tuta\ absoluta}$")
plt.show()

""" The following equations need to be turned into functions
# Per capita fecundity profile on female age in days at the optimum temperature
# from Bieri et al (1983) https://doi.org/10.5169/seals-402070

ovip(age_days) = constant_f * days / constant_g ^ age_days 


# The oviposition scalar (originally called FFTemperature in the Pascal code

T_scalar = 1.0 - ((T - T_lower_threshold - a) / a) ^ 2

with a_constant = (T_upper_threshold - T_lower_threshold) / 2


# The temperature dependent mortality taken from Lobesia botrana paper
# Gutierrez et al. (2012) https://doi.org/10.1111/j.1461-9563.2011.00566.x

mu(T) = c_constant (T - T_min_mortality / T_min_mortality ) ^ 2

def print_colors():

"""


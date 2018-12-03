import numpy as np

def power_matrix(voltage, current, power_factor):
    power_angle = np.arccos(power_factor)
    current = current*(np.cos(power_angle)-np.sign(power_factor)*(1j)*np.sin(power_angle))
    return np.array([
        [voltage],
        [current]
    ])

def power_factor(voltage, current):
    power_angle = np.angle(voltage*current)
    return np.sign(power_angle)*np.cos(power_angle)

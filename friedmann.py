#!/usr/bin/env python3
import json

from collections import deque
from math import pi
from sys import argv

# Physical constants.
G = 66450.0   # m^3 / kg / yr^2
H = 7.20e-11   # yr^-1

# Simulation constants.
DELTA_T = 1.0e8   # yr
MIN_A = 1.0e-3
MAX_TIME = 1.0e10   # yr


def simulate(rho_m0, rho_r0, rho_de0):
    results = deque()

    # Run simulation backwards.
    # Set initial values.
    a = 1.0
    v = H
    t = 0.0

    while a > MIN_A:
        results.appendleft((t, a))

        delta_a = v * -DELTA_T
        delta_v = accel(a, rho_m0, rho_r0, rho_de0) * -DELTA_T

        a += delta_a
        v += delta_v
        t += -DELTA_T

    # Run simulation forwards.
    # Reset initial values.
    a = 1.0
    v = H
    t = 0.0

    while t < MAX_TIME:
        delta_a = v * DELTA_T
        delta_v = accel(a, rho_m0, rho_r0, rho_de0) * DELTA_T

        a += delta_a
        v += delta_v
        t += DELTA_T

        results.append((t, a))

    return results


def accel(a, rho_m0, rho_r0, rho_de0):
    matter_term = rho_m0 / (a * a)
    radiation_term = 2 * rho_r0 / (a * a * a)
    dark_energy_term = -2 * rho_de0 * a

    return (-4 * pi * G / 3) * (matter_term + radiation_term + dark_energy_term)


if __name__ == '__main__':
    #rho_m0 = 2.53e-27
    #rho_r0 = 5.60e-31
    #rho_de0 = 6.78e-27

    rho_m0 = argv[1]  # kg / m^3
    rho_r0 = argv[2]   # kg / m^3
    rho_de0 = argv[3]   # kg / m^3

    results = simulate(rho_m0, rho_r0, rho_de0)

    # Put results into JSON.
    data = []
    for t, a in results:
        data.append({'t': t, 'a' : a})

    json_data = json.dumps(data)
    print(json_data)

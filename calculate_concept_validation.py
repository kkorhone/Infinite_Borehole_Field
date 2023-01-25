import matplotlib.pyplot as plt
import scipy.interpolate
import scipy.optimize
import scipy.signal
import pygfunction
import pandas as pd
import numpy as np

def calc(N, B):

    monthly_fraction = np.ones(12) / 12     # Heat extraction @ constant rate

    T_surface = 5.8                         # [degC]
    q_geothermal = 42.9e-3                  # [W/m^2]

    k_rock = 2.3                            # [W/(m*K)]
    Cp_rock = 850                           # [J/(kg*K)]
    rho_rock = 2800                         # [kg/m^3]

    R_borehole = 0.100                      # [K/(W/m)]

    borehole_length = 200.0                 # [m]
    borehole_radius = 0.150 / 2             # [m]

    num_years = 50                          # [1]

    T_target = -1.5                         # [degC]

    a_rock = k_rock / (rho_rock * Cp_rock)  # [m^2/s]

    t_max = num_years * 365 * 24 * 3600     # [s]

    delta_t = 730 * 3600                    # [s]

    borehole_geometry = (N, N)
    borehole_spacing = (B, B)

    T_initial = T_surface + q_geothermal / k_rock * (0.5 * borehole_length) # Temperature @ midpoint

    borehole_field = pygfunction.boreholes.rectangle_field(N_1=borehole_geometry[0], N_2=borehole_geometry[1], B_1=borehole_spacing[0], B_2=borehole_spacing[1], H=borehole_length, D=0, r_b=borehole_radius)

    total_borehole_length = borehole_geometry[0] * borehole_geometry[1] * borehole_length

    t = pygfunction.utilities.time_geometric(delta_t, t_max, 50)
    g = pygfunction.gfunction.uniform_temperature(borehole_field, t, a_rock, nSegments=1, disp=False)

    ti = np.arange(delta_t, t_max+delta_t, delta_t)
    gi = scipy.interpolate.interp1d(t, g)(ti)

    def evaluate_mean_fluid_temperatures(annual_heat_load):

        monthly_heat_load = annual_heat_load * monthly_fraction

        heat_rate = np.ravel(np.tile(monthly_heat_load*1_000_000/730.0, (1, num_years)))

        specific_heat_rate = heat_rate / total_borehole_length
        delta_q = np.hstack((-specific_heat_rate[0], np.diff(-specific_heat_rate)))

        T_wall = T_initial + scipy.signal.fftconvolve(delta_q, gi/(2.0*np.pi*k_rock), mode="full")[:len(ti)]
        T_fluid = T_wall - R_borehole * specific_heat_rate

        return T_fluid

    def cost_function(annual_heat_load):

        T_fluid = evaluate_mean_fluid_temperatures(annual_heat_load)

        return np.abs(np.min(T_fluid) - T_target)

    annual_heat_load = scipy.optimize.fminbound(cost_function, 1, 100000, xtol=0.001)

    T_fluid = evaluate_mean_fluid_temperatures(annual_heat_load)

    return annual_heat_load, T_fluid[-1]

if __name__ == "__main__":

    df = pd.DataFrame(columns=["N", "E_max", "T_fluid"])

    for N in range(101):

        E_max, T_fluid = calc(N, 20)

        df.loc[len(df)] = [N, E_max, T_fluid]
        df.to_excel("results_concept_validation.xlsx")

        print(f"{N} {E_max:.0f} {T_fluid:.6f}")

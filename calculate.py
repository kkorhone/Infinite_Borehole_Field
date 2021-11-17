from geology import Material, Geology, Layer
from scipy.optimize import minimize_scalar
from comsol import Parameters, init_model
import numpy as np
import time
import mph

def time_elapsed(seconds):
    seconds = int(np.floor(seconds))
    minutes = seconds // 60
    seconds %= 60
    if minutes == 0:
        return f"{seconds}s"
    elif seconds == 0:
        return f"{minutes}m"
    return f"{minutes}m{seconds}s"

monthly_extraction = np.array([0.155, 0.148, 0.125, 0.099, 0.064, 0.000, 0.000, 0.000, 0.061, 0.087, 0.117, 0.144])
monthly_injection = np.array([0, 0, 0, 0, 0, 0.250, 0.500, 0.250, 0, 0, 0, 0]) / 5

params = Parameters(L_borehole=110, D_borehole=0.110, borehole_spacing=500, E_annual=16.2, monthly_extraction=monthly_extraction, monthly_injection=monthly_injection)

material = Material("Rock Material", 3.5, 800, 2700)

geology = Geology("Bedrock Geology", 8, 0.06, [Layer("Bedrock Layer", 0, -1000, material)])

print(params) # 19.6

model = init_model(mph.start(), params, geology)

def cost_function(E_annual):
    tic = time.time()
    model.parameter("E_annual", f"{E_annual}[MWh]")
    model.solve()
    T_ave = model.evaluate("T_ave", "degC")
    cost = np.abs(np.min(T_ave))
    toc = time.time()
    print(f"time_elapsed={time_elapsed(toc-tic)}, E_annual={E_annual:.3f} MWh, cost={cost:.6f} K")
    return cost

result = minimize_scalar(cost_function, method="bounded", bounds=[5, 50], options={"disp": True})

print(result)

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

def cost_function(model, E_annual):
    tic = time.time()
    model.parameter("E_annual", f"{E_annual}[MWh]")
    model.solve()
    T_ave = model.evaluate("T_ave", "degC")
    cost = np.abs(np.min(T_ave))
    toc = time.time()
    print(f"time_elapsed={time_elapsed(toc-tic)}, E_annual={E_annual:.3f} MWh, cost={cost:.6f} K")
    return cost

if __name__ == "__main__":

#    params = Parameters(L_borehole=200, D_borehole=0.140, borehole_spacing=1000, E_annual=38.1966, num_years=50)
#
#    print(params)
#    
#    material = Material("Granite", k=2.5, Cp=700, rho=2800)
#
#    print(material)
#
#    geology = Geology("Bedrock", T_surface=10, q_geothermal=0.070, layers=[Layer("Rock", material, 0, -1000)])
#
#    print(geology)
#    
#    client = mph.start()
#
#    model = init_model(client, params, geology)
#    
#    result = minimize_scalar(lambda x: cost_function(model,x), method="bounded", bounds=[0, 100], options={"disp": True, "xatol": 0.001})
#    
#    print(result)

    monthly_fractions = [0.194717, 0.17216, 0.128944, 0.075402, 0.024336, 0, 0, 0, 0.025227, 0.076465, 0.129925, 0.172824]

    miocene = Material("Miocene", 1.8, 840, 2200, 0.1)
    lower_oligocene = Material("Lower Oligocene", 1.5, 2100, 2000, 0.05)
    upper_oligocene = Material("Upper Oligocene", 1.8, 900, 2500, 0.1)
    eocene = Material("Eocene", 2, 840, 2100, 0.15)
    triassic = Material("Triassic", 2.5, 850, 2700, 0.15)

    geology = Geology("B-179", 13.2, 0.0828568)
    geology.add_layers([Layer("Miocene", miocene, 0, -351.0), Layer("upper_oligocene", upper_oligocene, -351.0, -600), Layer("lower_oligocene", lower_oligocene, -600, -1025),Layer("eocene", eocene,-1025, -1240.0), Layer("triassic", triassic,-1240.0, -1304.5)])

    params = Parameters(L_borehole=300, D_borehole=0.150, borehole_spacing=20, E_annual=30, num_years=50, monthly_fractions=monthly_fractions)

    client = mph.start(cores=8)

    model = init_model(client, params, geology)

    model.save("blerp.mph")
    
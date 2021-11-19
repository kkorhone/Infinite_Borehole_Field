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
    
    monthly_fractions = [0.194717, 0.17216, 0.128944, 0.075402, 0.024336, 0, 0, 0, 0.025227, 0.076465, 0.129925, 0.172824]
    
    geology1 = Geology("B-21", 13.2, 0.0938)
    geology2 = Geology("B-30", 13.2, 0.0905)
    geology3 = Geology("B-39", 13.2, 0.098)
    geology4 = Geology("B-48", 13.2, 0.0867)
    geology5 = Geology("B-63", 13.2, 0.0928)
    geology6 = Geology("B-13", 13.2, 0.083581)
    geology7 = Geology("B-56", 13.2, 0.083625)
    geology8 = Geology("B-179", 13.2, 0.0828568)
    geology9 = Geology("B-180", 13.2, 0.082739)

    quaternary = Material("Quaternary", 3, 1800, 1800, 0.3)
    miocene = Material("Miocene", 1.8, 840, 2200, 0.1)
    upper_oligocene = Material("Upper Oligocene", 1.8, 900, 2500, 0.1)
    lower_oligocene = Material("Lower Oligocene", 1.5, 2100, 2000, 0.05)
    eocene = Material("Eocene", 2, 840, 2100, 0.15)
    triassic = Material("Triassic", 2.5, 850, 2700, 0.15)

    geology1.add_layers([Layer("Quaternary", quaternary, 0, -15.30), Layer("Lower Oligocene", lower_oligocene, -15.3, -523.0), Layer("Eocene", eocene, -523, -633.0), Layer("Triassic", triassic, -633.0, -766.4)])
    geology2.add_layers([Layer("Quaternary", quaternary, 0, -16.50), Layer("Lower Oligocene", lower_oligocene, -16.5, -551.0), Layer("Eocene", eocene, -551, -695.3), Layer("Triassic", triassic, -695.3, -800.0)])
    geology3.add_layers([Layer("Quaternary", quaternary, 0, -14.40), Layer("Upper Oligocene", upper_oligocene, -14.4, -285.4), Layer("Lower Oligocene", lower_oligocene, -285.4, -482), Layer("Triassic", triassic, -482, -650)])
    geology4.add_layers([Layer("Quaternary", quaternary, 0,  -7.90), Layer("Miocene", miocene,  -7.90, -360.30), Layer("upper_oligocene", upper_oligocene, -360.30, -507.00), Layer("lower_oligocene", lower_oligocene, -507.00, -1081.7), Layer("eocene", eocene,-1081.7, -1128.00), Layer("triassic",triassic, -1128, -1198)])
    geology5.add_layers([Layer("Quaternary", quaternary, 0, -24.85), Layer("Miocene", miocene, -24.85, -700.00), Layer("upper_oligocene", upper_oligocene, -700.00, -701.00)])
    geology6.add_layers([Layer("Quaternary", quaternary, 0, -12.00), Layer("Miocene", miocene, -12.00, -424.82), Layer("upper_oligocene", upper_oligocene, -424.82, -647.42), Layer("lower_oligocene", lower_oligocene, -647.42, -1194.0), Layer("eocene", eocene,-1194.0, -1234.82)])
    geology7.add_layers([Layer("Quaternary", quaternary, 0, -15.00), Layer("Miocene", miocene, -15.00, -439.10), Layer("upper_oligocene", upper_oligocene, -439.10, -775.40), Layer("lower_oligocene", lower_oligocene, -775.40, -1095.0), Layer("eocene", eocene,-1095.0, -1172.00), Layer("triassic",triassic, -1172, -1233)])
    geology8.add_layers([Layer("Miocene", miocene, 0, -351.0), Layer("upper_oligocene", upper_oligocene, -351.0, -600), Layer("lower_oligocene", lower_oligocene, -600, -1025),Layer("eocene", eocene,-1025, -1240.0), Layer("triassic", triassic,-1240.0, -1304.5)])
    geology9.add_layers([Layer("Miocene", miocene, 0, -347.3), Layer("upper_oligocene", upper_oligocene, -347.3, -580), Layer("lower_oligocene", lower_oligocene, -580, -1027),Layer("eocene", eocene,-1027, -1228.4), Layer("triassic", triassic,-1228.4, -1270.0)])

    client = mph.start()
    
    # Evaluates single-borehole potentials...
    
    params = Parameters(L_borehole=150, D_borehole=0.150, borehole_spacing=20, E_annual=30, num_years=50, monthly_fractions=monthly_fractions)
    
    for geology in [geology1, geology2, geology3, geology4, geology5, geology6, geology7, geology8, geology9]:
        
        print(geology)
        
        model = init_model(client, params, geology)
        
        result = minimize_scalar(lambda x: cost_function(model,x), method="bounded", bounds=[0, 100], options={"disp": True, "xatol": 0.001})
        
        print(result)

    # Evaluates borehole field potentials...
    
    params = Parameters(L_borehole=150, D_borehole=0.150, borehole_spacing=1000, E_annual=30, num_years=50, monthly_fractions=monthly_fractions)
    
    for geology in [geology1, geology2, geology3, geology4, geology5, geology6, geology7, geology8, geology9]:
        
        print(geology)
        
        model = init_model(client, params, geology)
        
        result = minimize_scalar(lambda x: cost_function(model,x), method="bounded", bounds=[0, 100], options={"disp": True, "xatol": 0.001})
        
        print(result)

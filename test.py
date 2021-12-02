from geology import Material, Geology, Layer
from scipy.optimize import minimize_scalar
from comsol import Parameters, init_model, save_model, temp_function
import mph

if __name__ == "__main__":

    material1 = Material("M1", 1.5, 700, 2700)
    material2 = Material("M2", 2.0, 700, 2700)
    material3 = Material("M3", 3.0, 700, 2700)

    geology = Geology("G", 13, 0.08)
    
    geology.add_layer(Layer("L1",    0,  -50, material1, 0.20))
    geology.add_layer(Layer("L2",  -50, -100, material2, 0.05))
    geology.add_layer(Layer("L3", -100, -500, material3, 0.15))

    params = Parameters(L_borehole=300, D_borehole=0.150, borehole_spacing=500, E_annual=30, num_years=50)

    client = mph.start(cores=8)

    model = init_model(client, params, geology)

    save_model(model)

    print(temp_function(model, 50))

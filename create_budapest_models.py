from budapest import make_geologies
from itertools import product
from comsol import Parameters, init_model
import os, mph

if __name__ == "__main__":

    monthly_fractions = [0.194717, 0.17216, 0.128944, 0.075402, 0.024336, 0, 0, 0, 0.025227, 0.076465, 0.129925, 0.172824]

    # -------------------------------------------------------------------------
    # Models without groundwater flow.
    # -------------------------------------------------------------------------

    geologies = make_geologies(darcy_flux="ignore")

    client = mph.start(cores=6)

    for case in product(*[geologies, [100, 200], [20, 500]]):

        geology, L_borehole, borehole_spacing = case

        params = Parameters(L_borehole=L_borehole, D_borehole=0.150, borehole_spacing=borehole_spacing, E_annual=0, num_years=50, monthly_fractions=monthly_fractions)

        model = init_model(client, params, geology)

        model_name = f"geology_{geology.tag}_{L_borehole}m_{borehole_spacing}m_without_groundwater_flow.mph"

        model.save(os.path.join("Shallow_Geothermal_Potential_Models", model_name))

    # -------------------------------------------------------------------------
    # Models with groundwater flow.
    # -------------------------------------------------------------------------

    geologies = make_geologies(darcy_flux="predefined")

    client = mph.start(cores=6)

    for case in product(*[geologies, [100, 200], [20, 500]]):

        geology, L_borehole, borehole_spacing = case

        params = Parameters(L_borehole=L_borehole, D_borehole=0.150, borehole_spacing=borehole_spacing, E_annual=0, num_years=50, monthly_fractions=monthly_fractions)

        model = init_model(client, params, geology)

        model_name = f"geology_{geology.tag}_{L_borehole}m_{borehole_spacing}m_with_groundwater_flow.mph"

        model.save(os.path.join("Shallow_Geothermal_Potential_Models", model_name))

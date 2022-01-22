import scipy.optimize
import numpy as np
import pyautogui
import os, time


pyautogui.FAILSAFE = False


def write_dat_file(file_name, params):
    file = open(file_name, "w")
    file.write("& Version=4.20\n")
    file.write("SI=yes\n")
    file.write("\n")
    file.write("\n")
    file.write("\n")
    file.write("\n")
    file.write("\n")
    file.write(f"{params['k_ground']} ThermCondGround\n")
    file.write(f"{params['C_ground']} HeatCap\n")
    file.write(f"{params['T_surface']} InitGroundSurfTemp\n")
    file.write(f"{params['q_geothermal']} GeothermalHeatFlux\n")
    file.write(f"{params['rec_num']} RecNum\n")
    file.write(f"{params['rec_num']}\n")
    file.write(f"{params['L_borehole']} BHDepth\n")
    file.write(f"{params['borehole_spacing']} B\n")
    file.write(f"{params['D_borehole']} BoreholeDiam\n")
    file.write("SINGLE-U\n")
    file.write("0.00060 BhVolFlow m3/s\n")
    file.write("1 Volflow index\n")
    file.write("1 Volflow factor\n")
    file.write("0.05000 PipeDiam\n")
    file.write("0.00460 PipeThick\n")
    file.write("0.22000 PipeThCond\n")
    file.write("0.10000 LinOutDiam\n")
    file.write("0.00400 LinThick\n")
    file.write("0.40000 LinThCond\n")
    file.write("0.00000 mc\n")
    file.write("0.04000 UPipeDiam\n")
    file.write("0.00240 UPipeThick\n")
    file.write("0.42000 UPipeThCond\n")
    file.write("0.07500 UPipeShankSpace\n")
    file.write("0.60000 ThermCondFill\n")
    file.write(" 4.07999992370605E-0001 hc_thermcond\n")
    file.write(" 4.21600000000000E+0003 hc_heatcap\n")
    file.write(" 9.68000000000000E+0002 hc_dens\n")
    file.write(" 6.30000000819564E-0003 hc_visc\n")
    file.write("-99 hc_freeze\n")
    file.write("0 calculate_borehole_resistance (yes=1,no=0)\n")
    file.write("10 multipoles\n")
    file.write(f" {params['R_borehole']} bore_rb\n")
    file.write(" 0 bore_ra\n")
    file.write(f" {params['R_borehole']} bore_rb_const\n")
    file.write(" 0 bore_ra_const\n")
    file.write("0 internal_heat_transfer (yes=1,no=0)\n")
    file.write("0 baseloadenergy_mode (yes=1,no=0)\n")
    file.write(f"{params['E_annual']} annual_heat_load\n")
    file.write(f"{params['SPF']} SPF_Heat\n")
    file.write(f"{params['SPF'] >= 99999 and 1 or 0} direct (yes=1,no=0)\n")
    file.write(f"{(params['SPF']-1)/params['SPF']*params['monthly_fractions'][0]*params['E_annual']} monthly heat load  1\n")
    file.write(f"{(params['SPF']-1)/params['SPF']*params['monthly_fractions'][1]*params['E_annual']} monthly heat load  2\n")
    file.write(f"{(params['SPF']-1)/params['SPF']*params['monthly_fractions'][2]*params['E_annual']} monthly heat load  3\n")
    file.write(f"{(params['SPF']-1)/params['SPF']*params['monthly_fractions'][3]*params['E_annual']} monthly heat load  4\n")
    file.write(f"{(params['SPF']-1)/params['SPF']*params['monthly_fractions'][4]*params['E_annual']} monthly heat load  5\n")
    file.write(f"{(params['SPF']-1)/params['SPF']*params['monthly_fractions'][5]*params['E_annual']} monthly heat load  6\n")
    file.write(f"{(params['SPF']-1)/params['SPF']*params['monthly_fractions'][6]*params['E_annual']} monthly heat load  7\n")
    file.write(f"{(params['SPF']-1)/params['SPF']*params['monthly_fractions'][7]*params['E_annual']} monthly heat load  8\n")
    file.write(f"{(params['SPF']-1)/params['SPF']*params['monthly_fractions'][8]*params['E_annual']} monthly heat load  9\n")
    file.write(f"{(params['SPF']-1)/params['SPF']*params['monthly_fractions'][9]*params['E_annual']} monthly heat load 10\n")
    file.write(f"{(params['SPF']-1)/params['SPF']*params['monthly_fractions'][10]*params['E_annual']} monthly heat load 11\n")
    file.write(f"{(params['SPF']-1)/params['SPF']*params['monthly_fractions'][11]*params['E_annual']} monthly heat load 12\n")
    file.write(f"{params['monthly_fractions'][0]} monthly heat factor  1\n")
    file.write(f"{params['monthly_fractions'][1]} monthly heat factor  2\n")
    file.write(f"{params['monthly_fractions'][2]} monthly heat factor  3\n")
    file.write(f"{params['monthly_fractions'][3]} monthly heat factor  4\n")
    file.write(f"{params['monthly_fractions'][4]} monthly heat factor  5\n")
    file.write(f"{params['monthly_fractions'][5]} monthly heat factor  6\n")
    file.write(f"{params['monthly_fractions'][6]} monthly heat factor  7\n")
    file.write(f"{params['monthly_fractions'][7]} monthly heat factor  8\n")
    file.write(f"{params['monthly_fractions'][8]} monthly heat factor  9\n")
    file.write(f"{params['monthly_fractions'][9]} monthly heat factor 10\n")
    file.write(f"{params['monthly_fractions'][10]} monthly heat factor 11\n")
    file.write(f"{params['monthly_fractions'][11]} monthly heat factor 12\n")
    file.write("0.00000 annual_cool_load\n")
    file.write("3.00000 SPF_Cool\n")
    file.write("0 direct (yes=1,no=0)\n")
    file.write("0.00000 monthly cool load  1\n")
    file.write("0.00000 monthly cool load  2\n")
    file.write("0.00000 monthly cool load  3\n")
    file.write("0.00000 monthly cool load  4\n")
    file.write("0.00000 monthly cool load  5\n")
    file.write("0.00000 monthly cool load  6\n")
    file.write("0.00000 monthly cool load  7\n")
    file.write("0.00000 monthly cool load  8\n")
    file.write("0.00000 monthly cool load  9\n")
    file.write("0.00000 monthly cool load 10\n")
    file.write("0.00000 monthly cool load 11\n")
    file.write("0.00000 monthly cool load 12\n")
    file.write("0.00000 monthly cool factor  1\n")
    file.write("0.00000 monthly cool factor  2\n")
    file.write("0.00000 monthly cool factor  3\n")
    file.write("0.00000 monthly cool factor  4\n")
    file.write("0.00000 monthly cool factor  5\n")
    file.write("0.00000 monthly cool factor  6\n")
    file.write("0.00000 monthly cool factor  7\n")
    file.write("0.00000 monthly cool factor  8\n")
    file.write("0.00000 monthly cool factor  9\n")
    file.write("0.00000 monthly cool factor 10\n")
    file.write("0.00000 monthly cool factor 11\n")
    file.write("0.00000 monthly cool factor 12\n")
    file.write(" 0.00000000000000E+0000 monthly heat peak load  1\n")
    file.write(" 0.00000000000000E+0000 monthly heat peak load  2\n")
    file.write(" 0.00000000000000E+0000 monthly heat peak load  3\n")
    file.write(" 0.00000000000000E+0000 monthly heat peak load  4\n")
    file.write(" 0.00000000000000E+0000 monthly heat peak load  5\n")
    file.write(" 0.00000000000000E+0000 monthly heat peak load  6\n")
    file.write(" 0.00000000000000E+0000 monthly heat peak load  7\n")
    file.write(" 0.00000000000000E+0000 monthly heat peak load  8\n")
    file.write(" 0.00000000000000E+0000 monthly heat peak load  9\n")
    file.write(" 0.00000000000000E+0000 monthly heat peak load 10\n")
    file.write(" 0.00000000000000E+0000 monthly heat peak load 11\n")
    file.write(" 0.00000000000000E+0000 monthly heat peak load 12\n")
    file.write(" 0.00000000000000E+0000 monthly heat duration  1\n")
    file.write(" 0.00000000000000E+0000 monthly heat duration  2\n")
    file.write(" 0.00000000000000E+0000 monthly heat duration  3\n")
    file.write(" 0.00000000000000E+0000 monthly heat duration  4\n")
    file.write(" 0.00000000000000E+0000 monthly heat duration  5\n")
    file.write(" 0.00000000000000E+0000 monthly heat duration  6\n")
    file.write(" 0.00000000000000E+0000 monthly heat duration  7\n")
    file.write(" 0.00000000000000E+0000 monthly heat duration  8\n")
    file.write(" 0.00000000000000E+0000 monthly heat duration  9\n")
    file.write(" 0.00000000000000E+0000 monthly heat duration 10\n")
    file.write(" 0.00000000000000E+0000 monthly heat duration 11\n")
    file.write(" 0.00000000000000E+0000 monthly heat duration 12\n")
    file.write(" 0.00000000000000E+0000 monthly cool peak load  1\n")
    file.write(" 0.00000000000000E+0000 monthly cool peak load  2\n")
    file.write(" 0.00000000000000E+0000 monthly cool peak load  3\n")
    file.write(" 0.00000000000000E+0000 monthly cool peak load  4\n")
    file.write(" 0.00000000000000E+0000 monthly cool peak load  5\n")
    file.write(" 0.00000000000000E+0000 monthly cool peak load  6\n")
    file.write(" 0.00000000000000E+0000 monthly cool peak load  7\n")
    file.write(" 0.00000000000000E+0000 monthly cool peak load  8\n")
    file.write(" 0.00000000000000E+0000 monthly cool peak load  9\n")
    file.write(" 0.00000000000000E+0000 monthly cool peak load 10\n")
    file.write(" 0.00000000000000E+0000 monthly cool peak load 11\n")
    file.write(" 0.00000000000000E+0000 monthly cool peak load 12\n")
    file.write(" 0.00000000000000E+0000 monthly cool duration  1\n")
    file.write(" 0.00000000000000E+0000 monthly cool duration  2\n")
    file.write(" 0.00000000000000E+0000 monthly cool duration  3\n")
    file.write(" 0.00000000000000E+0000 monthly cool duration  4\n")
    file.write(" 0.00000000000000E+0000 monthly cool duration  5\n")
    file.write(" 0.00000000000000E+0000 monthly cool duration  6\n")
    file.write(" 0.00000000000000E+0000 monthly cool duration  7\n")
    file.write(" 0.00000000000000E+0000 monthly cool duration  8\n")
    file.write(" 0.00000000000000E+0000 monthly cool duration  9\n")
    file.write(" 0.00000000000000E+0000 monthly cool duration 10\n")
    file.write(" 0.00000000000000E+0000 monthly cool duration 11\n")
    file.write(" 0.00000000000000E+0000 monthly cool duration 12\n")
    file.write("-1.00000000000000E+0000 tfluid_min_required\n")
    file.write(" 1.50000000000000E+0001 tfluid_max_required\n")
    file.write("0 include_peak_load (yes=1,no=0)\n")
    file.write(f"{params['num_years']} max_number_of_cycles\n")
    file.write("1 start_month\n")
    file.write("-1\n")
    file.write("-1\n")
    file.write("-1\n")
    file.write("-1\n")
    file.write("-1\n")
    file.write("-1\n")
    file.write("-1\n")
    file.write("-1\n")
    file.write("-1\n")
    file.write("-1\n")
    file.write("-1\n")
    file.write("0.00000 annual DHW\n")
    file.write("3.00000 SPF DHW\n")
    file.write("0 Config min\n")
    file.write("797 Config max\n")
    file.write(" 3.00000000000000E+0001 Land area width\n")
    file.write(" 2.00000000000000E+0001 Land area height\n")
    file.write("5 Spacing min\n")
    file.write("100 Spacing max\n")
    file.write(" 5.00000000000000E+0001 Depth min\n")
    file.write(" 3.00000000000000E+0002 Depth max\n")
    file.write("2000 Borehole num max\n")
    file.write("1 detail (yes=1,no=0)\n")
    file.write("0 round off (yes=1,no=0)\n")
    file.write("0 Also list cases with warnings (yes=1,no=0)\n")
    file.write("2 Step\n")
    file.write("0 Sort index\n")
    file.write("EUR\n")
    file.write(" 0.00000000000000E+0000 Cost fix\n")
    file.write(" 0.00000000000000E+0000 Cost fix per bh \n")
    file.write(" 0.00000000000000E+0000 Cost drilling per m \n")
    file.write(" 0.00000000000000E+0000 Cost soil drilling per bh \n")
    file.write(" 0.00000000000000E+0000 Cost soil drilling per m\n")
    file.write(" 0.00000000000000E+0000 depth soil drilling\n")
    file.write(" 0.00000000000000E+0000 Cost ditch per m\n")
    file.write("qtest.txt\n")
    file.write("qtest.txt\n")
    file.write("qtest.txt\n")
    file.write("qtest.txt\n")
    file.write("qxls.txt\n")
    file.write("0 Show results after\n")
    file.write("0 CB_SolveHours (yes=1,no=0)\n")
    file.write("1 CB_UseInitialBase (yes=1,no=0)\n")
    file.write("1 CB_UseInitialPeak (yes=1,no=0)\n")
    file.write("0 CB_readqifile (yes=1,no=0)\n")
    file.write("0 CB_UseAnnualVariation (yes=1,no=0)\n")
    file.write("1 CB_useheat (yes=1,no=0)\n")
    file.write("1 CB_usecool (yes=1,no=0)\n")
    file.write("0 CB_usedhw (yes=1,no=0)\n")
    file.write("0 File option index\n")
    file.write("E:\\TEMP\\kkorhone\\\n")
    file.close()


def eval_fluid_temp(params, E_annual):
    params["E_annual"] = E_annual
    if os.path.exists("eval.out"):
        os.remove("eval.out")
    if os.path.exists("eval.dat"):
        os.remove("eval.dat")
    write_dat_file("eval.dat", params)
    w = pyautogui.getWindowsWithTitle("Earth Energy Designer")[0]
    w.activate()
    pyautogui.keyDown("altleft")
    pyautogui.press("f")
    pyautogui.keyUp("altleft")
    pyautogui.press("1")
    pyautogui.press("f9")
    time.sleep(1)
    file = open("eval.out", "r")
    lines = file.readlines()
    file.close()
    for line in lines:
        if line.strip().startswith("Annual heating load (DHW excluded)"):
            ahl = float(line[36:-4].strip())
        if line.strip().startswith("Minimum mean fluid temperature"):
            mft = float(line[32:-18].strip())
    print(f"E_annual={ahl} T_fluid={mft}")
    return mft


def optimize_energy(params, bounds, T_target):

    import win32api

    win32api.WinExec(r"C:\Program Files (x86)\BLOCON\EED_v4.20\EED_v4_20.exe")

    time.sleep(5)

    write_dat_file("eval.dat", params)

    w = pyautogui.getWindowsWithTitle("Earth Energy Designer")[0]
    w.activate()

    # File -> Open -> "eval.dat"
    pyautogui.keyDown("altleft")
    pyautogui.press("f")
    pyautogui.keyUp("altleft")
    pyautogui.press("o")
    pyautogui.keyDown("altleft")
    pyautogui.press("n")
    pyautogui.keyUp("altleft")
    pyautogui.write("eval.dat")
    pyautogui.press("enter")

    # File -> Save
    pyautogui.keyDown("altleft")
    pyautogui.press("f")
    pyautogui.keyUp("altleft")
    pyautogui.press("s")

    # Settings -> Show results with more digits
    pyautogui.keyDown("altleft")
    pyautogui.press("e")
    pyautogui.keyUp("altleft")
    pyautogui.press("h")

    obj_func = lambda E_annual: np.abs(eval_fluid_temp(params, E_annual) - T_target)

    E_max = scipy.optimize.fminbound(obj_func, bounds[0], bounds[1], xtol=1e-3)

    T_fluid = eval_fluid_temp(params, E_max)

    w.close()

    return E_max, T_fluid


if __name__ == "__main__":

    params = {
        "k_ground": 3.45,
        "C_ground": 6.78e6,
        "T_surface": 1.23,
        "q_geothermal": 0.0456,
        "rec_num": 761,
        "L_borehole": 123,
        "D_borehole": 0.140,
        "borehole_spacing": 34,
        "R_borehole": 0.123,
        "E_annual": 3456,
        "SPF": 3,
        "num_years": 50,
        "monthly_fractions": np.array([0.194717, 0.17216, 0.128944, 0.075402, 0.024336, 0, 0, 0, 0.025227, 0.076465, 0.129925, 0.172824])
    }

    optimize_energy(params, [1e3, 10e3], T_target=-1.5)

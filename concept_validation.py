<<<<<<< HEAD
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

plt.rcParams["font.family"] = "serif"
plt.rcParams["font.serif"] = "Times"
plt.rcParams["font.size"] = 13
plt.rcParams["text.usetex"] = True

data_frame = pd.read_excel("concept_validation.xlsx")

N = data_frame["N"].values
E = data_frame["E_max"].values

#for n in range(1,51):
#    i = np.where(N >= n**2)[0]
#    p = np.polyfit(N[i], E[i], 1)
#    e = np.polyval(p,N[i]) - E[i]
#    RMSE = np.sqrt(sum(e**2)/len(e))
#    print(n, RMSE)

n = 50
i = np.where(N >= n**2)[0]
p = np.polyfit(N[i], E[i], 1)

Ni = np.arange(len(data_frame), 1001)**2
Ei = np.polyval(p, Ni)

#plt.figure()
#plt.plot(N, E, "r.")
#plt.plot(Ni, Ei, "b-")
#plt.axvspan(N[i[0]], N[i[-1]], color=[0.85,0.85,0.85])
#plt.show()
#raise SystemExit

plt.figure()
plt.semilogx(N, E/N, "-", color="r")
plt.semilogx(Ni, Ei/Ni, "--", color="r")
plt.axhline(9.7, color="b", ls="--")

plt.gca().set_xlim([1, 100000])
plt.gca().set_ylim([5, 30])

plt.xlabel("Number of boreholes in the field")
plt.ylabel("Average yield of a borehole in the field [MWh/a]")

#ax1.set_xlim([1, 10000])
#ax2.set_xlim([1, 10000])
#t1 = Y1[-1]
#t2 = Y2[-1]
#t3 = Y3[-1]
#t4 = Y4[-1]
#t5 = Y5[-1]

#ax2.text(9000, Y1[-1]+0.65, "$B$ = 10 m", ha="right")
#ax1.text(9000, y2[-1]+0.50, "$B$ = 20 m", ha="right")
#ax1.text(9000, y3[-1]+0.40, "$B$ = 30 m", ha="right")
#ax2.text(9000, Y4[-1]+0.40, "$B$ = 40 m", ha="right")
#ax2.text(9000, Y5[-1]+0.60, "$B$ = 50 m", ha="right")

#ax1.set_xticks([1, 10, 100, 1_000, 10_000])
#ax1.set_xticklabels(["1", "10", "100", "1,000", "10,000"])

#plt.legend((h1, h2), ("100-m deep boreholes", "200-m deep boreholes"), ncol=1, handlelength=1, labelspacing=0.333)

plt.tight_layout()

plt.savefig("concept_validation.png")

plt.show()
=======
{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "name": "Copy of budapest.ipynb",
      "provenance": [],
      "collapsed_sections": [],
      "authorship_tag": "ABX9TyOnmcqjqHFVdUpy/AVLty6Y",
      "include_colab_link": true
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    },
    "accelerator": "GPU"
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/kkorhone/Infinite_Borehole_Field/blob/main/concept_validation.py\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "VzzulnGkJbzf"
      },
      "source": [
        "# Pygfunction validation of the concept of an infinite borehole field\n",
        "\n",
        "This code finds the maximal amount of shallow geothermal energy $E_{\\rm field}$ [MWh/a] that can be extracted from borehole fields of increasing sizes. NB: $N=60$ seems to be the upper limit that colab can do."
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "D0wzBJpgJN8v"
      },
      "source": [
        "**First, the pygfunction library needs to be installed.**"
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 731
        },
        "id": "_25t8ChDHZ0-",
        "outputId": "2e25b7d8-e820-4355-d41a-6c263967949b"
      },
      "source": [
        "pip install pygfunction"
      ],
      "execution_count": 2,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Collecting pygfunction\n",
            "  Downloading pygfunction-2.1.0-py3-none-any.whl (116 kB)\n",
            "\u001b[K     |████████████████████████████████| 116 kB 4.3 MB/s \n",
            "\u001b[?25hCollecting coolprop>=6.4.1\n",
            "  Downloading CoolProp-6.4.1-cp37-cp37m-manylinux1_x86_64.whl (4.2 MB)\n",
            "\u001b[K     |████████████████████████████████| 4.2 MB 35.2 MB/s \n",
            "\u001b[?25hCollecting scipy>=1.6.2\n",
            "  Downloading scipy-1.7.3-cp37-cp37m-manylinux_2_12_x86_64.manylinux2010_x86_64.whl (38.1 MB)\n",
            "\u001b[K     |████████████████████████████████| 38.1 MB 1.4 MB/s \n",
            "\u001b[?25hCollecting matplotlib>=3.3.4\n",
            "  Downloading matplotlib-3.5.1-cp37-cp37m-manylinux_2_5_x86_64.manylinux1_x86_64.whl (11.2 MB)\n",
            "\u001b[K     |████████████████████████████████| 11.2 MB 30.9 MB/s \n",
            "\u001b[?25hRequirement already satisfied: numpy>=1.20.1 in /usr/local/lib/python3.7/dist-packages (from pygfunction) (1.21.5)\n",
            "Requirement already satisfied: pyparsing>=2.2.1 in /usr/local/lib/python3.7/dist-packages (from matplotlib>=3.3.4->pygfunction) (3.0.7)\n",
            "Requirement already satisfied: cycler>=0.10 in /usr/local/lib/python3.7/dist-packages (from matplotlib>=3.3.4->pygfunction) (0.11.0)\n",
            "Collecting fonttools>=4.22.0\n",
            "  Downloading fonttools-4.29.1-py3-none-any.whl (895 kB)\n",
            "\u001b[K     |████████████████████████████████| 895 kB 47.6 MB/s \n",
            "\u001b[?25hRequirement already satisfied: pillow>=6.2.0 in /usr/local/lib/python3.7/dist-packages (from matplotlib>=3.3.4->pygfunction) (7.1.2)\n",
            "Requirement already satisfied: packaging>=20.0 in /usr/local/lib/python3.7/dist-packages (from matplotlib>=3.3.4->pygfunction) (21.3)\n",
            "Requirement already satisfied: kiwisolver>=1.0.1 in /usr/local/lib/python3.7/dist-packages (from matplotlib>=3.3.4->pygfunction) (1.3.2)\n",
            "Requirement already satisfied: python-dateutil>=2.7 in /usr/local/lib/python3.7/dist-packages (from matplotlib>=3.3.4->pygfunction) (2.8.2)\n",
            "Requirement already satisfied: six>=1.5 in /usr/local/lib/python3.7/dist-packages (from python-dateutil>=2.7->matplotlib>=3.3.4->pygfunction) (1.15.0)\n",
            "Installing collected packages: fonttools, scipy, matplotlib, coolprop, pygfunction\n",
            "  Attempting uninstall: scipy\n",
            "    Found existing installation: scipy 1.4.1\n",
            "    Uninstalling scipy-1.4.1:\n",
            "      Successfully uninstalled scipy-1.4.1\n",
            "  Attempting uninstall: matplotlib\n",
            "    Found existing installation: matplotlib 3.2.2\n",
            "    Uninstalling matplotlib-3.2.2:\n",
            "      Successfully uninstalled matplotlib-3.2.2\n",
            "\u001b[31mERROR: pip's dependency resolver does not currently take into account all the packages that are installed. This behaviour is the source of the following dependency conflicts.\n",
            "albumentations 0.1.12 requires imgaug<0.2.7,>=0.2.5, but you have imgaug 0.2.9 which is incompatible.\u001b[0m\n",
            "Successfully installed coolprop-6.4.1 fonttools-4.29.1 matplotlib-3.5.1 pygfunction-2.1.0 scipy-1.7.3\n"
          ]
        },
        {
          "output_type": "display_data",
          "data": {
            "application/vnd.colab-display-data+json": {
              "pip_warning": {
                "packages": [
                  "matplotlib",
                  "mpl_toolkits",
                  "scipy"
                ]
              }
            }
          },
          "metadata": {}
        }
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "**The calculations.**"
      ],
      "metadata": {
        "id": "qw5dDDD_V7rx"
      }
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "tffzeZaLHvnj"
      },
      "source": [
        "import matplotlib.pyplot as plt\n",
        "import scipy.interpolate\n",
        "import scipy.optimize\n",
        "import scipy.signal\n",
        "import pygfunction\n",
        "import numpy as np\n",
        "\n",
        "def main(N, B):\n",
        "\n",
        "    monthly_fraction = np.ones(12) / 12     # Heat extraction @ constant rate\n",
        "\n",
        "    T_surface = 5.8                         # [degC]\n",
        "    q_geothermal = 42.9e-3                  # [W/m^2]\n",
        "    \n",
        "    k_rock = 2.3                            # [W/(m*K)]\n",
        "    Cp_rock = 850                           # [J/(kg*K)]\n",
        "    rho_rock = 2800                         # [kg/m^3]\n",
        "    \n",
        "    R_borehole = 0.100                      # [K/(W/m)]\n",
        "    \n",
        "    borehole_length = 200.0                 # [m]\n",
        "    borehole_radius = 0.150 / 2             # [m]\n",
        "\n",
        "    num_years = 50                          # [1]\n",
        "\n",
        "    T_target = -1.5                         # [degC]\n",
        "    \n",
        "    a_rock = k_rock / (rho_rock * Cp_rock)  # [m^2/s]\n",
        "    \n",
        "    t_max = num_years * 365 * 24 * 3600     # [s]\n",
        "\n",
        "    delta_t = 730 * 3600                    # [s]\n",
        "    \n",
        "    borehole_geometry = (N, N)\n",
        "    borehole_spacing = (B, B)\n",
        "    \n",
        "    T_initial = T_surface + q_geothermal / k_rock * (0.5 * borehole_length) # Temperature @ midpoint\n",
        "    \n",
        "    ts = borehole_length**2 / (9.0 * a_rock)\n",
        "\n",
        "    borehole_field = pygfunction.boreholes.rectangle_field(N_1=borehole_geometry[0], N_2=borehole_geometry[1], B_1=borehole_spacing[0], B_2=borehole_spacing[1], H=borehole_length, D=0, r_b=borehole_radius)\n",
        "\n",
        "    total_borehole_length = borehole_geometry[0] * borehole_geometry[1] * borehole_length\n",
        "\n",
        "    t = pygfunction.utilities.time_geometric(delta_t, t_max, 50)\n",
        "    g = pygfunction.gfunction.uniform_temperature(borehole_field, t, a_rock, nSegments=1, disp=False)\n",
        "\n",
        "    ti = np.arange(delta_t, t_max+delta_t, delta_t)\n",
        "    gi = scipy.interpolate.interp1d(t, g)(ti)\n",
        "    \n",
        "    def evaluate_mean_fluid_temperatures(annual_heat_load):\n",
        "\n",
        "        monthly_heat_load = annual_heat_load * monthly_fraction\n",
        "\n",
        "        heat_rate = np.ravel(np.tile(monthly_heat_load*1_000_000/730.0, (1, num_years)))\n",
        "\n",
        "        specific_heat_rate = heat_rate / total_borehole_length\n",
        "        delta_q = np.hstack((-specific_heat_rate[0], np.diff(-specific_heat_rate)))\n",
        "        \n",
        "        T_wall = T_initial + scipy.signal.fftconvolve(delta_q, gi/(2.0*np.pi*k_rock), mode=\"full\")[:len(ti)]\n",
        "        T_fluid = T_wall - R_borehole * specific_heat_rate\n",
        "        \n",
        "        return T_fluid\n",
        "    \n",
        "    def cost_function(annual_heat_load):\n",
        "\n",
        "        T_fluid = evaluate_mean_fluid_temperatures(annual_heat_load)\n",
        "\n",
        "        return np.abs(np.min(T_fluid) - T_target)\n",
        "    \n",
        "    annual_heat_load = scipy.optimize.fminbound(cost_function, 1, 100000, xtol=0.001)\n",
        "    \n",
        "    T_fluid = evaluate_mean_fluid_temperatures(annual_heat_load)\n",
        "    \n",
        "    print(borehole_geometry[0]*borehole_geometry[1], annual_heat_load)\n",
        "\n",
        "if __name__ == \"__main__\":\n",
        "\n",
        "    for N in range(61, 71):\n",
        "        main(N, 20)\n"
      ],
      "execution_count": null,
      "outputs": []
    }
  ]
}
>>>>>>> 2a08aa48a9943ea824759006ccb30701ac143d75

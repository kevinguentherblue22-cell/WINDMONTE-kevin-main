import math
import numpy as np
import pickle


def DREs(input_data, G):
    """Minimal wrapper to compute CL/CD from a list of input dicts."""

    out = []

    # Default geometry values if G is not provided
    if G is None:
        G = {}

    design = G["Design"] 

    # allow G to override S and W, otherwise use defaults
    S_local = G.get('S', 1)
    W_local = G.get('W', 0)

    for e in input_data:
        N_meas = e.get('NF', 0)
        A_meas = e.get('AF', 0)
        Theta = e.get('Theta', 0)
        Q = e.get('Q', 1)

        A_rad = math.radians(Theta)

        #N_aero = N_meas + W_local * math.cos(A_rad)
        #A_aero = A_meas - W_local * math.sin(A_rad)

        #L = N_aero * math.cos(A_rad) - A_aero * math.sin(A_rad)
        #D = N_aero * math.sin(A_rad) + A_aero * math.cos(A_rad)

        L = N_meas * math.cos(A_rad) - A_meas * math.sin(A_rad) + W_local
        D = N_meas * math.sin(A_rad) + A_meas * math.cos(A_rad)

        C_L = L / (Q * S_local)
        C_D = D / (Q * S_local)

        AOA = Theta - G["Theta_offset"]

        out.append({
            'NF': N_meas,
            'AF': A_meas,
            'SF': e.get('SF', 0),
            'PM': e.get('PM', 0),
            'RM': e.get('RM', 0),
            'YM': e.get('YM', 0),
            'Theta': Theta,
            'Q': Q,
            'S': S_local,
            'W': W_local,
            'CL': C_L,
            'CD': C_D,
            'AOA': AOA
        })

    return out
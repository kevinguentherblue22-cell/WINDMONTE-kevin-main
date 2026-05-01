import math
import numpy as np
import pickle



def DREs(input_data, G=None):
    """Minimal wrapper to compute CL/CD from a list of input dicts.

    Keeps the same calculation form used above. Expects input_data to be
    a list of dicts with keys 'NF','AF','Theta'. Returns a list of dicts
    including 'CL' and 'CD'.
    """
    out = []

    # Minimal local defaults (used if G is not provided). These mirror
    # the constants used previously in the module's example code.
   # V_default = 95.33
   # RHO_default = 0.002378
  #  S_default = 7.44
   # W_default = 15

design = 'B' # Design A, B, C, or D

if design == 'A':
    theta_offset = 0 # Angle of attack offset in degrees


elif design == 'B':
    theta_offset = 0 # Angle of attack offset in degrees


elif design == 'C':
    theta_offset = -10 # Angle of attack offset in degrees

elif design == 'D':
    theta_offset = -10 # Angle of attack offset in degrees

    # allow G to override S and W, otherwise use defaults
    S_local = G.get('S') 
    W_local = G.get('W') 
    
    for e in input_data:
        N_meas = e.get('NF', 0)
        A_meas = e.get('AF', 0)
        Theta = e.get('Theta', 0)
        Q = e.get('Q', 0)
        A_rad = math.radians(Theta)

        N_aero = N_meas + W_local * math.cos(A_rad)
        A_aero = A_meas - W_local * math.sin(A_rad)

        L = N_aero * math.cos(A_rad) - A_aero * math.sin(A_rad) 
        D = N_aero * math.sin(A_rad) + A_aero * math.cos(A_rad)

        C_L = L / (Q * S_local)
        C_D = D / (Q * S_local)

        AOA = Theta - Theta_offset

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






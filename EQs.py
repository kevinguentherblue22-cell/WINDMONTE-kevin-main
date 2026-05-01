import math
import numpy as np
import pickle


# This realies on all my arrays being the same length
AOA_raw = [-9 + 0.5*i for i in range(51)] # Angle of Attack in degrees


#Model Constants
#Model Constants

RHO = 0.00242 # Air Density in slugs/ft^3

S = .774 # Wing Area in ft^2

 

design = 'B' # Design A, B, C, or D

if design == 'A':

    Q = 14.6 # Dynamic Pressure in psf

    theta_offset = 0 # Angle of attack offset in degrees

    W = 10 # Weight in lbs

elif design == 'B':

    Q = 20 # Dynamic Pressure in psf

    theta_offset = 0 # Angle of attack offset in degrees

    W = 10 # Weight in lbs

elif design == 'C':

    Q = 20 # Dynamic Pressure in psf

    theta_offset = -10 # Angle of attack offset in degrees

    W = 15 # Weight in lbs

elif design == 'D':

    Q = 14.6 # Dynamic Pressure in psf

    theta_offset = -10 # Angle of attack offset in degrees

    W = 15 # Weight in lbs

 

V = np.sqrt(2*Q/RHO) # Wind Tunnel Speed in ft/s

#Update AOA_raw to AOA_list
AOA_list = AOA_raw # Angle of Attack in degrees
CL_list = [.0806*a+.2495 for a in AOA_list] # Lift Coefficient
CD_list = [.0271+.0534*x**2 for x in CL_list] # Drag Coefficient

Theta_list = [a + AOA_offset for a in AOA_list]

# Initializing array to store results
N_mean_list = np.zeros(len(CL_list))
A_mean_list = np.zeros(len(CL_list))
data = []

#Creates a range to run through all values of input arrays
for i in range(len(CL_list)):
    
    # Getting current values from input arrays
    CL = CL_list[i] 
    CD = CD_list[i]
    Theta = Theta_list[i]
    
    #Converts degrees to radians
    A = float(np.radians(Theta)) # Angle of Attack in radians

    # Equations to get L and D
    L = Q * S * CL # Lift in lbs
    D = Q * S * CD # Drag in lbs

    # Equations to get N_aero and A_aero
    N_aero = L * math.cos(A) + D * math.sin(A) # Aerodynamic Normal Force in lbs
    A_aero = - L * math.sin(A) + D * math.cos(A) # Aerodynamic Axial Force in lbs

    # Equations to get N_meas and A_meas
    N_meas = N_aero - W * math.cos(A) # Measured Normal Force in lbs
    A_meas = A_aero + W * math.sin(A) # Measured Axial Force in lbs

    #Stores all values as data
    data.append({'NF': N_meas, 'AF': A_meas, 'SF': 0, 'PM': 0, 'RM': 0,'YM': 0, 'Theta': Theta, 'Q': Q, 'S': S, 'W': W, 'AOA': AOA_list[i]})

testinfo = {'S': S, 'W': W, 'RunNum': 1}

# Wind tunnel speed and angles (AOA, model constants, dynamic pressure (q), desity sea level)
#saves the dictioary as a pickle file 
with open("wind_forces_inputs.pkl", "wb") as f: 
    pickle.dump((data, testinfo), f)

#prints the results to check accuracy
print('end')


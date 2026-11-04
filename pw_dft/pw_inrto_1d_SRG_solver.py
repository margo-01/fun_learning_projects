# 1D Plane Wave Schroedinger Equation (SRG) solver

import numpy as np
import matplotlib.pyplot as plt



def deriv1_1d(x, f_x):
    df_1d_array = []
    for i in range(0, len(x)-1):
        df_1d = (f_x[i+1]-f_x[i])/(x[i+1]-x[i])
        df_1d_array.append(df_1d)
    return df_1d_array

def deriv2_1d(x, f_x):
    n = len(x)
    d2f = np.zeros(n)
    
    for i in range(1, n - 1):
        d2f[i] = (f_x[i+1] - 2*f_x[i] + f_x[i-1]) / (x[i+1] - x[i])**2
    
    d2f[0] = (f_x[1] - 2*f_x[0]) / (x[i+1] - x[i])**2
    d2f[-1] = (f_x[-2] - 2*f_x[-1]) / (x[i+1] - x[i])**2
    return d2f

def int_trap_1d(x, f_x):
    int_array = np.zeros(len(x))
    for i in range(len(x)-1):
        int_array[i] = (x[i+1]-x[i])*((f_x[i]+f_x[i+1])/2) 
    #int_array[len(x)-1] = int_array[0]
    int_val = np.sum(int_array)
    return int_array, int_val    

def norm_const(x, f_x):
    nn = int_trap_1d(x, f_x**2)[1]
    n = np.sqrt(1/nn)
    return n


def T_kin(x):
    T = np.zeros((len(x), len(x)))
    for j in range(len(x)):
        e_j = np.zeros(len(x))
        e_j[j] = 1.0
        
        d2e_j = deriv2_1d(x, e_j)
        T[:,j] = -0.5*d2e_j
    return T


def V_pot_periodic(x, V_0, L):
    V_pot = np.zeros((len(x), len(x)))
    for j in range(len(x)):
        V_pot[j,j] = V_0* np.cos((2*np.pi* x[j])/L)  
    return V_pot



def build_H(x, V_0, L):
    T_mat = T_kin()
    V_mat = V_pot_periodic(x, V_0, L)
    H_mat = T_mat+V_mat
    return H_mat













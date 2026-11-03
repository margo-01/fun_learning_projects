#KS-1D Harmonic Oscillator

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


def V_pot_HO(x):
    V_HO = np.zeros((len(x), len(x)))
    for j in range(len(x)):
        V_HO[j,j] = x[j]**2    
    return V_HO
def calculate_density(n_el, x, psi):
    density = np.zeros(len(x))

    for i in range(n_el):
        n = i-np.ceil(i/2)
        n = int(n)
        density += (norm_const(x_grid, psi_gn[:,n])*psi_gn[:,n])**2
        
    print('# electrons:',int_trap_1d(x_grid, density)[1])
    return density

def calculate_exchange(x, density):
    E_ex = (-3/4)*((3/np.pi)**(1/3))*int_trap_1d(x, density)[1]**(4/3)
    v_ex = (-(3/np.pi)**(1/3))*(density)**(1/3)
    return E_ex, v_ex

def calculate_coulomb(x,density):
    eps = 1e-1
    v_cc = np.zeros(len(x))
    for i in range(len(x)):
        func = density*(1/np.sqrt((x[i] - x)**2 + eps))
        v_cc[i] = int_trap_1d(x, func)[1]
        
    E_cc = int_trap_1d(x, 0.5*v_cc*density)[1]           
    return E_cc, v_cc

def scf_log(n, E, convergence):
    if n > 0:
        diff = abs(E[n]-E[n-1])
        
        print(f'Energy: {E[n]}, Energy difference: {diff}, convergence reached? {convergence}')
    else:
        print(f'Initial energy: {E[n]}')
        

x_grid = np.linspace(-5, 5, 200)

T_kin_mat = T_kin(x_grid)
V_HO_mat = V_pot_HO(x_grid)

#H_HO = T_kin_mat + V_HO_mat

#epsilon_n , psi_gn = np.linalg.eigh(H_HO)

#SCF loop
n_max = 1000
E_conv = 0.000001
convergence = False
density = np.zeros(len(x_grid))
n = 0
E_values = [0]

while n < n_max and convergence == False:
    print(f'**********STARTING THE SCF CYCLE # {n}**********')
    scf_log(n, E_values, convergence)
    
    E_cc, v_cc = calculate_coulomb(x_grid, density)
    E_x, v_x = calculate_exchange(x_grid, density)
    T_kin_mat = T_kin(x_grid)
    V = V_pot_HO(x_grid)+np.diagflat(v_x) + np.diagflat(v_cc)
    H_HO = T_kin_mat+V
    
    epsilon_n , psi_gn = np.linalg.eigh(H_HO)
    density= calculate_density(17, x_grid, psi_gn)
    
    
    E_values.append(epsilon_n[0])
    print(epsilon_n[0])
    if n > 1:
        convergence = abs(epsilon_n[0]-E_values[n-1]) < E_conv 
    n += 1
    
    
    

#write a nice plotting animation













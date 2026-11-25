import numpy as np


from cell import Cell, PWBasis, make_pw_basis


def kinetic_diag(basis):
    t_mat = 0.5*basis.g2
    return t_mat

def potential_matrix(basis, v_r):
    N = basis.cell.npts
    vg = basis.cell.to_g(v_r)
    d = (basis.miller[:, None, :] - basis.miller[None, :, :]) % N     # (npw, npw, 3)
    return vg[d[..., 0], d[..., 1], d[..., 2]]
    
    
    
def dense_hamiltonian(basis, v_r):
    t_mat= np.diag(kinetic_diag(basis)).astype(complex)
    v_mat = potential_matrix(basis, v_r)
    H_mat = t_mat +v_mat
    return H_mat

def cosine_potential(cell, V0):
    
    V = V0*np.cos((2*np.pi*cell.grid[..., 0])/cell.L) 
    
    return V

def harmonic_potential(cell):
    r0 = np.array([cell.L/2, cell.L/2, cell.L/2])

    dr = cell.grid - r0

    V = 0.5 * np.sum(dr**2, axis=-1)

    return V

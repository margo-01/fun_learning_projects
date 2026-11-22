import numpy as np


from cell import Cell, PWBasis, make_pw_basis

cell = Cell(10.0, 16, 1.5)
basis = make_pw_basis(cell)
print(basis.npw)

def kinetic_diag(basis):
    t_mat = 0.5*basis.g2
    return t_mat

def potential_matrix(basis, v_r ):
    V_g = np.fft.fft(v_r)
    


E = kinetic_diag(basis)
unit = 0.5 * (2 * np.pi / 10.0) ** 2
shell, count = np.unique(np.round(E / unit).astype(int), return_counts=True)
print(list(zip(shell.tolist(), count.tolist())))      # (n^2, degeneracy)


def cosine_potential(cell, grid):
    V = 0.2*np.cos((2*np.pi*grid)/cell.L) # hardcoded V_0
    
    return V



v = cosine_potential(cell, 0.02)
Vm = potential_matrix(basis, v)
print(Vm.shape)
print(np.abs(Vm - Vm.conj().T).max() < 1e-14)                  # Hermitian
print(np.count_nonzero(np.abs(Vm) > 1e-12))                    # number of coupled pairs
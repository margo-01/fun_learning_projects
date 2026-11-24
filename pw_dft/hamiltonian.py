import numpy as np


from cell import Cell, PWBasis, make_pw_basis

cell = Cell(10.0, 16, 1.5)
basis = make_pw_basis(cell)
print(basis.npw)

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

E = kinetic_diag(basis)
unit = 0.5 * (2 * np.pi / 10.0) ** 2
shell, count = np.unique(np.round(E / unit).astype(int), return_counts=True)
print(list(zip(shell.tolist(), count.tolist())))      # (n^2, degeneracy)


def cosine_potential(cell, V0):
    
    V = V0*np.cos((2*np.pi*cell.grid[..., 0])/cell.L) 
    
    return V

def harmonic_potential(cell):
    V = (cell.grid[..., 0])**2-cell.L/2**2
    return 0.5*V

v = cosine_potential(cell, 0.02)
Vm = potential_matrix(basis, v)
print(Vm.shape)
print(np.abs(Vm - Vm.conj().T).max() < 1e-14)                  # Hermitian
print(np.count_nonzero(np.abs(Vm) > 1e-12))                    # number of coupled pairs


H = dense_hamiltonian(basis, v)
w = np.linalg.eigvalsh(H)
print(w[:8])
g = 2 * np.pi / 10.0
print("2nd-order estimate of E0:", -0.02 ** 2 / g ** 2)


print(" ecut    npw       E0       E0 - 1.5")
for ecut in [2, 4, 6, 8, 10]:
    cell32 = Cell(10.0, 32, ecut)
    v_ho = harmonic_potential(cell32)                 # 0.5 |r - r0|^2, exact levels 1.5, 2.5 (x3), 3.5 ...
    b = make_pw_basis(cell32)
    w = np.linalg.eigvalsh(dense_hamiltonian(b, v_ho))
    print(f"{ecut:5d} {b.npw:6d}  {w[0]:.6f}  {w[0] - 1.5:.2e}")
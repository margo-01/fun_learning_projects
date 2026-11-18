import numpy as np


from cell import Cell, PWBasis, make_pw_basis

cell = Cell(10.0, 16, 1.5)
basis = make_pw_basis(cell)
print(basis.npw)

def kinetic_diag(basis):
    t_mat = 0.5*basis.g2
    return t_mat

def potential_matrix():
    pass


E = kinetic_diag(basis)
unit = 0.5 * (2 * np.pi / 10.0) ** 2
shell, count = np.unique(np.round(E / unit).astype(int), return_counts=True)
print(list(zip(shell.tolist(), count.tolist())))      # (n^2, degeneracy)
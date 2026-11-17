import numpy as np


from cell import Cell, PWBasis, make_pw_basis

cell = Cell(10.0, 16, 1.5)
basis = make_pw_basis(cell)

def kinetic_diag(basis):
    t_mat = 0.5*basis.g2
    return t_mat

def potential_matrix():
    pass



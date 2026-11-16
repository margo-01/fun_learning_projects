# grids and unit cell setup

import numpy as np
from dataclasses import dataclass



class Cell:
    def __init__(self, L: float, npts: int):
        self.L = L
        self.npts = npts
        self.grid = self.make_grid(L, npts)
        self.G_vec = self.make_gvec(L, npts)
        self.G_vec_sq = self.get_g2(L, npts)

    def make_grid(self, L: float, npts: int):
        d_x = L/npts
        x = np.arange(0, npts)*d_x
        grid_array = np.stack(np.meshgrid(x,x,x, indexing='ij'), axis = -1)
        return grid_array
    
    def make_miller_indices(self, npts: int):
        freq = np.fft.fftfreq(npts, 1/npts)
        return np.round(freq * npts).astype(int)
    # fix the unit cell to be a cube of length L

    def make_gvec(self, L: float, npts: int):
        freq = self.make_miller_indices(npts)
        g = (2*np.pi/L)*freq
        G_vec = np.stack(np.meshgrid(g,g,g, indexing='ij'), axis = -1)
        return G_vec
        

    def get_g2(self, L: float, npts: int):
        G_vec_sq = self.make_gvec(L, npts)**2 
        G_vec_sq = G_vec_sq[:,:,:].sum(axis=-1)
        return G_vec_sq


    def to_g(self, f_r):
        c_g = np.fft.fftn(f_r)*(1/len(f_r))
        return c_g
        

    def to_r(self, c_g):
        f_r = np.fft.ifftn(c_g)*(len(c_g))
        return f_r

    def inner_r(self, f, g):
        inner_r = np.sum(np.conjugate(f) * g * (1/f.size))
        return inner_r
        
    def inner_g(self, c, d):
        inner_g = np.sum(np.conjugate(c)* d)
        return inner_g
        

    def gradient(self, f_r, L):
        G_vec = self.make_gvec(L, f_r.shape[0])
        G_vec = G_vec
        c_g = self.to_g(f_r)
        dr_f_r = [self.to_r(1j*c_g*G_vec[:,:,:,a] ) for a in range(3)]
        
        return np.stack(dr_f_r, axis=-1)

    def laplacian(self, f_r, L):
        c_g = self.to_g(f_r)
        G_vec_sq = self.get_g2(L, f_r.shape[0])
        d2r2_f_r = self.to_r(-G_vec_sq*c_g).real
        return d2r2_f_r

    def make_ecut_mask(self, L, npts, e_cut):
        G_vec = self.make_gvec(L, npts)
        R = np.sqrt(2*e_cut)
        mask = [G_vec<R for a in range(3)]
        return np.stack(np.array(mask), axis = -1)


    def suggest_npts(self, L, e_cut, npts):  
        pass




class PWBasis:
    def __init__(self, Cell):
        self.cell = Cell

    def build_basis(self, e_cut):
        G_vec = self.cell.G_vec
        mask = self.cell.make_ecut_mask(self.cell.L, self.cell.npts, e_cut)
        basis = G_vec[mask]
        return basis

@dataclass
class PWBasis:
    cell: Cell
    ecut: float
    mask: np.ndarray      # bool (N,N,N): which FFT-grid points are in the sphere
    miller: np.ndarray    # int  (npw,3)
    gvec: np.ndarray      # float (npw,3)
    g2: np.ndarray        # float (npw,)

    @property
    def npw(self):
        return self.g2.size


def make_pw_basis(cell: Cell, ecut: float) -> PWBasis:
    mask = cell.make_ecut_mask(cell.L, cell.npts, ecut)
    miller = cell.make_miller()[mask] 
    gvec = cell.G_vec[mask] #booleian indexing mask applied to 3D array of G-vectors
    g2 = cell.G_vec_sq[mask]
    
    return PWBasis(cell=cell, ecut=ecut, mask=mask, miller=miller, gvec=gvec, g2=g2)
# grids and unit cell setup

import numpy as np



def make_grid(L: float, npts:int ):
    d_x = L/npts
    x = np.arange(0, npts)*d_x
    grid_array = np.stack(np.meshgrid(x,x,x, indexing='ij'), axis = -1)
    return grid_array


# fix the unit cell to be a cube of length L

def make_gvec(L: float, npts:int):
    freq = np.fft.fftfreq(npts, 1/npts)
    g = (2*np.pi/L)*freq
    G_vec = np.stack(np.meshgrid(g,g,g, indexing='ij'), axis = -1)
    return G_vec
    

def get_g2(L, npts):
    G_vec_sq = make_gvec(L, npts)**2 
    G_vec_sq = G_vec_sq[:,:,:].sum(axis=-1)
    return G_vec_sq


def to_g(f_r):
    c_g = np.fft.fftn(f_r)*(1/f_r.size)
    return c_g
    

def to_r(c_g):
    f_r = np.fft.ifftn(c_g)*(c_g.size)
    return f_r
















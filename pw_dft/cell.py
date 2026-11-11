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

def inner_r(f,g):
    inner_r = np.dot(np.conjugate(f), g).sum()*(1/f.size)
    return inner_r
    
def inner_g(c,d):
    inner_g = np.dot(np.conjugate(c), d).sum()
    return inner_g
    
N, L = 8, 10.0
grid = make_grid(L, N)
m = np.array([1, -2, 0])
f = np.exp(1j * grid @ (2 * np.pi / L * m))     # a single plane wave
c = to_g(f)
print(np.round(abs(c[1, -2, 0]), 12))            # all weight in one coefficient ...
print(np.round(abs(c).sum(), 12))                # ... and nowhere else
print(to_g(3.0 * np.ones((N, N, N)))[0, 0, 0])   # constant function -> c_0 = its value
rnd = np.random.default_rng(0).normal(size=(N, N, N))
print(np.abs(to_r(to_g(rnd)) - rnd).max() < 1e-12)   # round trip

rng = np.random.default_rng(0)
f = rng.normal(size=(8, 8, 8)) + 1j * rng.normal(size=(8, 8, 8))
g = rng.normal(size=(8, 8, 8)) + 1j * rng.normal(size=(8, 8, 8))
print(np.round(inner_r(f, g), 10))
print(np.round(inner_g(to_g(f), to_g(g)), 10))











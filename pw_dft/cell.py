# grids and unit cell setup

import numpy as np



def make_grid(L: float, npts ):
    d_x = L/npts
    x = np.arange(0, npts)*d_x
    grid_array = np.stack(np.meshgrid(x,x,x, indexing='ij'), axis = -1)
    return grid_array


# fix the unit cell to be a cube of length L

def make_gvec(L: float, npts):
    freq = np.fft.fftfreq(npts, 1/npts)
    g = (2*np.pi/L)*freq
    G_vec = np.stack(np.meshgrid(g,g,g, indexing='ij'), axis = -1)
    return G_vec
    

def get_g2(L, npts):
    G_vec_sq = make_gvec(L, npts)**2 
    G_vec_sq = G_vec_sq[:,:,:].sum(axis=-1)
    return G_vec_sq


def to_g(f_r):
    c_g = np.fft.fftn(f_r)*(1/len(f_r))
    return c_g
    

def to_r(c_g):
    f_r = np.fft.ifftn(c_g)*(len(c_g))
    return f_r

def inner_r(f,g):
    inner_r = np.sum(np.conjugate(f) * g * (1/f.size))
    return inner_r
    
def inner_g(c,d):
    inner_g = np.sum(np.conjugate(c)* d)
    return inner_g
    

def gradient(f_r, L):
    G_vec = make_gvec(L, f_r.shape[0])
    G_vec = G_vec
    c_g = to_g(f_r)
    dr_f_r = [to_r(1j*c_g*G_vec[:,:,:,a] ) for a in range(3)]
    
    return np.stack(dr_f_r, axis=-1)

def laplacian(f_r, L):
    c_g = to_g(f_r)
    G_vec_sq = get_g2(L, f_r.shape[0])
    d2r2_f_r = to_r(-G_vec_sq*c_g).real
    return d2r2_f_r

def test_gaussian(L, N, sigma=0.8):
    """Gaussian centred in the box and its exact gradient / Laplacian."""
    r = make_grid(L, N) - L / 2
    r2 = (r ** 2).sum(axis=-1)
    f = np.exp(-r2 / (2 * sigma ** 2))
    grad = -r / sigma ** 2 * f[..., None]
    lap = (r2 / sigma ** 4 - 3 / sigma ** 2) * f
    return f, grad, lap

def make_ecut_mask(L, npts, e_cut):
    G_vec = make_gvec(L, npts)
    R = np.sqrt(2*e_cut)
    mask = [G_vec<R for a in range(3)]
    return np.stack(np.array(mask), axis = -1)


def suggest_npts(L, e_cut, npts):  
    pass






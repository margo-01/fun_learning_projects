# grids and unit cell setup

import numpy as np



def make_grid(L: float, npts:int ):
    d_x = L/npts
    x = np.arange(0, npts)*d_x
    grid_array = np.meshgrid(x,x,x, indexing='ij')
    return grid_array




























# grids and unit cell setup

import numpy as np



def make_grid(L: float, npts:int ):
    d_x = L/npts
    x = np.arange(0, npts)*d_x
    grid_array = np.stack(np.meshgrid(x,x,x, indexing='ij'), axis=-1)
    return grid_array


# fix the unit cell to be a cube of length L

























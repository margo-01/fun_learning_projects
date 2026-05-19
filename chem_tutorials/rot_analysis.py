# Rotational analysis
import numpy as np

from scipy import constants
from scipy.constants import physical_constants
from molmass import ELEMENTS


E_h = physical_constants["Hartree energy"][0]
a_0 = physical_constants["Bohr radius"][0]
amu = physical_constants["atomic mass constant"][0]
c_0 = physical_constants["speed of light in vacuum"][0]
h = physical_constants["Planck constant"][0]
kilo = constants.kilo
centi = constants.centi
angstrom = constants.angstrom
mega = constants.mega

class RotationalAnalysis:
    def __init__(self, molecule):
        self.molecule = molecule
        


    def center_of_mass(self):  
        m_x = np.sum(self.molecule.coord_at[:,0]*self.molecule.mol_mass)/self.molecule.m_total
        m_y = np.sum(self.molecule.coord_at[:,1]*self.molecule.mol_mass)/self.molecule.m_total
        m_z = np.sum(self.molecule.coord_at[:,2]*self.molecule.mol_mass)/self.molecule.m_total
        m_final = [m_x, m_y,m_z]
        return m_final
    
    def moment_of_inertia1(self):
        com = self.center_of_mass()
        coords = self.molecule.coord_at - com
        m = self.molecule.mol_mass
    
        x, y, z = coords[:,0], coords[:,1], coords[:,2]
    
        Ixx = np.sum(m * (y**2 + z**2))
        Iyy = np.sum(m * (x**2 + z**2))
        Izz = np.sum(m * (x**2 + y**2))
    
        Ixy = -np.sum(m * x * y)
        Ixz = -np.sum(m * x * z)
        Iyz = -np.sum(m * y * z)
    
        mat_i = np.array([
            [Ixx, Ixy, Ixz],
            [Ixy, Iyy, Iyz],
            [Ixz, Iyz, Izz]
        ])
        
        eps, eigvec = np.linalg.eigh(mat_i)
        geom = 'na'
        if abs(eps[0]-eps[1])<0.0001:
            if abs(eps[1]-eps[2])<0.0001:
                geom = 'spherical'
            if eps[1]<eps[2]:
                geom = 'oblate'
        if abs(eps[1]-eps[2])<0.0001 and eps[0]<eps[1]:
            geom = 'prolate'          
        if eps[0] < 0.0001:
            geom = 'linear'
        else:
            geom = 'asymmetric'
        
        print(f' Molecular geometry: {geom}')
    
        return eps, eigvec
    
    
    
    def moment_of_inertia(self):
        # Output: Principle of moments of intertia
        com = self.center_of_mass()
        atom_weights = np.array([ELEMENTS[c].mass for c in self.molecule.z_at])
        trans_coords = self.molecule.coord_at - com
        res = - np.einsum("i, ix, iy -> xy", atom_weights, trans_coords, trans_coords)
        np.fill_diagonal(res, res.diagonal() - res.diagonal().sum())
        print(res)
        return np.linalg.eigvalsh(res)
    
    
    
    def display_moment_of_interia(self):
        # Output: Print moments of inertia in amu bohr2, amu Å2, and g cm2
        moment_in_amu_bohr = self.moment_of_inertia1()
        moment_in_amu_bohr = moment_in_amu_bohr[0]
        moment_in_amu_a = [i* a_0**2 / angstrom**2 for i in moment_in_amu_bohr]
        moment = [i* amu * kilo * a_0**2 / centi**2 for i in moment_in_amu_bohr]
        print(f'[a.m.u, Bohr^2]{moment_in_amu_bohr}')
        print(f'[a.m.u. A^2]{moment_in_amu_a}')
        print(f'[g cm^2] {moment}')
        
        
    
    def rotational_constants(self):
        # Output: Rotational constant in cm^-1
        eps = self.moment_of_inertia1()
        eps = eps[0]
        return h / (8 * np.pi**2 * c_0 * eps) / amu / a_0**2 * centi
    
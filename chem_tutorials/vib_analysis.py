#Vibrational Analysis
import numpy as np
from scipy import constants
from scipy.constants import physical_constants


E_h = physical_constants["Hartree energy"][0]
a_0 = physical_constants["Bohr radius"][0]
amu = physical_constants["atomic mass constant"][0]
c_0 = physical_constants["speed of light in vacuum"][0]
h = physical_constants["Planck constant"][0]
kilo = constants.kilo
centi = constants.centi
angstrom = constants.angstrom
mega = constants.mega




class VibrationalAnalysis:
    def __init__(self, molecule):
        self.molecule = molecule
        
    def read_hessian(self, filename):
        hes = []
        with open(filename, 'r') as f:
            next(f)
            for line in f:
                l = line.strip().split()
                hes.append(l)
        hes = np.array(hes,dtype=float)
        hes = np.reshape(hes, (self.molecule.n_at*3, self.molecule.n_at*3))
        self.hes_data = hes 
                
    
    def mw_hessian(self):
        mw_hes = np.zeros((len(self.hes_data), len(self.hes_data)))
        m_list = [x for x in self.molecule.mol_mass for _ in range(3)]
        for i in range(len(self.hes_data)):
            for j in range(len(self.hes_data)):
                mw_hes[i,j] = self.hes_data[i,j]/np.sqrt(m_list[i]*m_list[j])
         
        self.mw_hes = mw_hes
        
    def eig_mw_hes(self):
        eps, eigvec = np.linalg.eigh(self.mw_hes)
        self.eps =eps
        self.eigvec = eigvec
        
    def vib_frec(self):
        eps_sqrt = [np.sqrt(x) for x in self.eps]
        freq = (centi/(2*np.pi*c_0))*np.sqrt((E_h)/(amu*a_0**2))*np.array(eps_sqrt)
        
        self.freq = freq
        



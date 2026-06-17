# Molecular geometry analysis project

# https://pycrawfordprogproj.readthedocs.io/en/latest/Project_01/Project_01.html


from molecule import Molecule
from rot_analysis import RotationalAnalysis
from vib_analysis import VibrationalAnalysis
from HF_analysis import HFAnalysis



if __name__ == '__main__':
    h2o = Molecule()
    h2o.open_structure_dat("h2o_geom.txt")
           
    #vib_results = VibrationalAnalysis(h2o)
    #vib_results.read_hessian('h2o_hessian.txt')
    #vib_results.mw_hessian()
    #vib_results.eig_mw_hes()
   # vib_results.vib_frec()
    hf_results = HFAnalysis(h2o, './hf_input', 7)
    hf_results.load_enuc('enuc.dat')
    hf_results.build_hcore()
    hf_results.SCF_loop()
    
    
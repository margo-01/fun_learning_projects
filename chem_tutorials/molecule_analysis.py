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

    test = hf_results.s_diag()
    
    D_tmp = [[ 3.5281047,  0.2488   ,  1.4226012,  2.8945118,  3.4003372, -0.8209289, -0.7561818],
   [ 0.2488   , -0.2064377,  0.7442728,  1.0084798,  2.9236323,  1.9913284,  2.0724504],
   [ 1.4226012,  0.7442728,  2.9881581, -0.9473233,  0.4680151,  0.3482841, -3.062642 ],
   [ 2.8945118,  1.0084798, -0.9473233,  4.5395092, -1.0762032, -0.3415683, -0.6252582],
   [ 3.4003372,  2.9236323,  0.4680151, -1.0762032, -1.7755715, -2.2830992, -1.6007075],
   [-0.8209289,  1.9913284,  0.3482841, -0.3415683, -2.2830992, -2.0971059, -0.6425276],
   [-0.7561818,  2.0724504, -3.062642 , -0.6252582, -1.6007075, -0.6425276, -3.2277957]]

    
    C_test = hf_results.fock_diag(D_tmp)
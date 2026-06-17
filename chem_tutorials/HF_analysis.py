# HF SCF Closed Shell
import numpy as np
from pathlib import Path

#this code assumes standard naming of input files (ie the names are hard-coded mb can improve)

class HFAnalysis:
    def __init__(self, molecule, data_path, basis_size):
        self.molecue = molecule
        self.data_path = Path(data_path)
        self.basis_size = basis_size
        
    def load_enuc(self, filename):
        with open(self.data_path/filename, 'r') as f:
            for line in f:
                    E_nuc = float(line.strip())
                    
        self.E_nuc = E_nuc

    
    def _load_1e_int(self,filename):
        one_e_mat = np.zeros((self.basis_size, self.basis_size))
        with open(self.data_path/filename, 'r') as f:
            for line in f:
                l = np.array(line.strip().split(), dtype = float)
                i,j = int(l[0]), int(l[1])
                one_e_mat[i-1,j-1] = l[2]
                one_e_mat[j-1,i-1] = l[2]
        return one_e_mat
    
    def build_hcore(self):
        self.s_mat = self._load_1e_int('s.dat')
        self.v_mat = self._load_1e_int('v.dat')
        self.t_mat = self._load_1e_int('t.dat')

        self.hcore_mat = self.t_mat + self.v_mat
        
        
    def _load_2d_int(self,filename):
        eri_mat = np.zeros((self.basis_size, self.basis_size, self.basis_size, self.basis_size ))
        with open(self.data_path/filename, 'r') as f:
            for line in f:
                l = np.array(line.strip().split(), dtype = float)
                mu, nu, kappa, lamda = int(l[0])-1, int(l[1])-1, int(l[2])-1, int(l[3])-1
                eri_mat[mu, nu, kappa, lamda] = l[4]
                eri_mat[mu, nu, lamda, kappa] = l[4]
                eri_mat[nu, mu, kappa, lamda] = l[4]
                eri_mat[nu, mu, lamda, kappa] = l[4]
                eri_mat[kappa, lamda, mu, nu] = l[4]
                eri_mat[lamda, kappa, mu, nu] = l[4]
                eri_mat[kappa, lamda, nu, mu] = l[4]
                eri_mat[lamda, kappa, nu, mu] = l[4]
        return eri_mat                
                
    def s_diag(self):
        LAM, U = np.linalg.eigh(self.s_mat)
        s_diag = U @ np.diagflat(LAM**(-0.5)) @ np.transpose(U)
        self.S_diag = s_diag
      
    def fock_mat(self):
        
        self.build_hcore()
 
        eri_mat = self._load_2d_int('eri.dat')
        J_mat = np.zeros((self.basis_size, self.basis_size))
        K_mat = np.zeros((self.basis_size, self.basis_size))
        
    
        for mu in range(self.basis_size):
            for nu in range(self.basis_size):
                J_mat[mu, nu] = (eri_mat[mu,nu] * self.D_mu_nu_mat).sum()
        for mu in range(self.basis_size):
            for nu in range(self.basis_size):
                K_mat[mu, nu] = (eri_mat[mu, :, nu, :]*self.D_mu_nu_mat).sum()
        self.J_mat = J_mat
        self.K_mat = K_mat     
        
        Fock_mat = self.hcore_mat + self.J_mat - 0.5*self.K_mat
        
        self.Fock_mat = Fock_mat
        
        
    def fock_diag(self):
        self.s_diag()
        self.fock_mat()
        
        Fock_diag = self.S_diag @ self.Fock_mat @ self.S_diag
        
        eps, eigvec = np.linalg.eigh(Fock_diag)
        C_mat = self.S_diag @ eigvec
         
        self.C_mat = C_mat
    
    def D_mat(self):
        D_mat = np.zeros((len(self.C_mat), len(self.C_mat)))
        for mu in range(len(self.C_mat)): #
            for nu in range(len(self.C_mat)):
                D_mat[mu,nu] += 2*(np.sum(self.C_mat[mu, 0:int(self.molecue.n_mo_occ)]*self.C_mat[nu, 0 :int(self.molecue.n_mo_occ)]))
        self.D_mu_nu_mat = D_mat
                
    
    def update_D_mu_nu_mat(self):
            self.fock_diag()
            self.D_mat()

    def E_total(self):
        E_e = 0
        
        for mu in range(len(self.D_mu_nu_mat)):
            for nu in range(len(self.D_mu_nu_mat)):
                E_e += 0.5*(self.D_mu_nu_mat[mu,nu]*(self.hcore_mat[mu,nu]+self.Fock_mat[mu,nu]))


        E_tot = E_e +self.E_nuc
        self.E_tot = E_tot
        return E_tot
                
    def SCF_loop(self):
        self.D_mu_nu_mat = np.zeros((self.basis_size, self.basis_size))
        E_tot = 0
        E_list = []
        E_conv = False
        E_rms_conv = False
        max_iter = 100
        e_conv_th = 1e-10
        rmse_conv_th = 1e-8
        iter_n = 0
        while E_conv == False and E_rms_conv == False:
            if iter_n < max_iter:
                self.update_D_mu_nu_mat()
                E = self.E_total() 
                E_list.append(E)
                E_dif = np.abs(E_tot - E)
                rms = np.linalg.norm(self.D_mu_nu_mat, 'fro')
                if E_dif < e_conv_th:
                    E_conv = True
                if rms < rmse_conv_th:
                    E_rms_conv = True
                print("______________________________________________________________________")
                print(f"SCF Cycle: {iter_n}, Total Energy: {E}, Delta E: {E_dif}")
                print(f"RMSE: {rms}, Energy Convergence: {E_conv}, RMS Convergence: {E_rms_conv}")
                print("______________________________________________________________________")
                E_tot = E
                iter_n += 1 
            else:
                print("######## MAXIMUM NUMBER OF ITERATIONS REACHED WITHOUT CONVERGENCE ########")
            
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        

        

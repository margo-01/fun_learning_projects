# Molecular geometry analysis project

# https://pycrawfordprogproj.readthedocs.io/en/latest/Project_01/Project_01.html

import numpy as np
from molmass import ELEMENTS


class Molecule: 
    
    def __init__(self):
        self.n_at = []
        self.z_at = []
        self.coord_at = []

    def open_structure_dat(self, filename):
        count = 0
        n_at = []
        z_at = []
        coords = []
        with open(filename, 'r') as f:
            for line in f:
                if count == 0:
                    n_at = line.strip()
                else:
                    l = line.strip().split()
                    z_at.append(int(float(l[0])))
                    coords.append(l[1:4])
                count += 1 


        self.n_at = int(n_at)
        self.z_at = np.array(z_at,dtype=int)
        mol_mass = []        
        for i in self.z_at:
            e = ELEMENTS[i]
            mol_mass.append(e.mass)
        m_total = np.sum(mol_mass)
        
        self.n_mo_occ = np.sum(z_at)/2 #valid only for closed shell systems        
        self.mol_mass = mol_mass
        self.m_total = m_total
        self.coord_at = np.array(coords,dtype=float)
        return 


    def bond_length(self, i, j):
        
        r_i = self.coord_at[i]
        r_j = self.coord_at[j]
    
        r_ij = np.linalg.norm(r_i - r_j)
        
        return r_ij
    
    def display_r_ij(self):
        print('__________Bond Lengths__________')
        for i in range(0, self.n_at):
            for j in range(1, self.n_at-i):
                r_ij = self.bond_length( i, j+i)
                print(f'Atom # {i} - #{j} - {r_ij}')
    
             
    def bond_unit_vector(self, i, j):
        r_i = self.coord_at[i]
        r_j = self.coord_at[j]
        R_ij = self.bond_length( i, j)
        e_ij = -(r_i-r_j)/R_ij
        return e_ij
    
    def bond_angle(self, i, j, k):
        e_ji = self.bond_unit_vector( j, i)
        e_jk = self.bond_unit_vector( j, k)
        phi = np.arccos(np.inner(e_ji, e_jk))  
        phi = phi*(180/np.pi)
        return phi
    
    
    def display_phi(self):
        seen = []
        print('__________Bond Angles__________')
        for i in range(self.n_at):
            for j in range(self.n_at):
                for k in range(self.n_at):
                    seq = [i, j, k]
                    seq_rev = seq[::-1] 
                    seen.append(seq)
                    rev = seq_rev in seen
                    if i!=j!= k and rev == False:
                      R_ij = self.bond_length( i, j)
                      R_jk = self.bond_length( j, k)
                      if R_ij < 3 and R_jk < 3:
                          phi = self.bond_angle( i, j, k)
                          if phi > 90:
                              print(f'Atom #{i} - #{j} - #{k} : {phi}')     

             
    
    
    def phi_valid(self, i,j,k):
        phi_valid = False
        phi = 'na'
        if i!=j!=k:
            R_ij = self.bond_length( i, j)
            R_jk = self.bond_length( j, k)
            if R_ij < 3 and R_jk <3:
                phi = self.bond_angle( i, j, k)
                if phi > 90:
                    phi_valid = True
        
        return phi_valid , phi
    
        
    
    def display_phi_og(self):
        seen = []
        print('________Bond Angles________')
        for i in range(self.n_at):
            for j in range(self.n_at):
                for k in range(self.n_at):
                    seq = [i, j, k]
                    seq_rev = seq[::-1] 
                    seen.append(seq)
                    rev = seq_rev in seen
                    if i!=j!= k and rev == False:
                      R_ij = self.bond_length( i, j)
                      R_jk = self.bond_length( j, k)
                      if R_ij < 3 and R_jk < 3:
                          phi = self.bond_angle( i, j, k)
                          if phi > 90:
                              print(f'Atom #{i} - #{j} - #{k} : {phi}')
                    
    
    def out_of_plane_angle(self, i,j,k,l):
        e_kj = self.bond_unit_vector( k, j)
        e_kl = self.bond_unit_vector( k, l)
        e_ki = self.bond_unit_vector( k, i)
        phi_jkl = self.bond_angle( j, k, l)/(180/np.pi) #check the fcking units
        stheta = np.dot(np.cross(e_kj, e_kl)/np.sin(phi_jkl),  e_ki)
     #   print(stheta)
        #assert(np.abs(stheta) < 1 + 1e-7)
        theta = np.arcsin(stheta)*(180/np.pi)
        return theta
    
    def theta_valid(self, i,j,k,l):
        theta_valid = False
        if len({i,j,k,l}) == 4:
        
            phi_data = self.phi_valid( j, k, l)
            phi_valid_val = phi_data[0]
            phi = phi_data[1]
            if phi_valid_val == True and phi < 180 :
                R_ik = self.bond_length( i, k)
                if R_ik < 3:
                    theta_valid = True
            
        return theta_valid
    
    def display_theta(self): 
        seen = []
        print('________Out of Plane Angles________')
        for i in range(self.n_at):
            for j in range(self.n_at):
                for k in range(self.n_at):
                    for l in range(self.n_at):
                        
                        seq = [i, j, k, l]
                        seen.append(seq)
                        seq_rev = [seq[0]] + seq[:0:-1]
                        #print(seq_rev)
                        rev = seq_rev in seen
                        theta_valid_val = self.theta_valid( i, j, k, l)
                        if theta_valid_val == True and rev == False:
                            theta = self.out_of_plane_angle( i, j, k, l)
                            print(f'Atom #{i} - #{j} - #{k} - #{l} : {theta}')
    
            
    
    
    def dihedral_angle(self, i,j,k,l):
        e_ji = self.bond_unit_vector( j, i)
        e_jk = self.bond_unit_vector( j, k)
        e_kj = self.bond_unit_vector( k, j)
        e_kl = self.bond_unit_vector( k, l)
        
        phi_ijk = self.bond_angle( i, j, k)/(180/np.pi)
        phi_jkl = self.bond_angle( j, k, l)/(180/np.pi)
        taus = np.dot(np.cross(e_ji, e_jk), np.cross(e_kj, e_kl))/(np.sin(phi_ijk)*np.sin(phi_jkl)) 
        taus = np.clip(taus, -1,1)
        tau = np.arccos(taus)*(180/np.pi)
        return tau
    
    def tau_valid(self, i,j,k,l):
        tau_valid = False
        if len({i,j,k,l}) == 4:
            phi_ijk_val = self.phi_valid( i, j, k)[0] 
            phi_ikj_val = self.phi_valid( i, k, j)[0]
            #print(phi_ijk_val)
            phi_jkl_val = self.phi_valid( j, k, l)[0]
            phi_kjl_val = self.phi_valid( k,j,l)[0]
            #print(phi_jkl_val)
            if (phi_ijk_val == True or phi_ikj_val == True) and (phi_jkl_val == True or phi_kjl_val == True):
                tau_valid = True
        
        return tau_valid
            
    
    
    def display_tau(self):
        print('________Dihedral Angles________')
        seen = []
    
        for i in range(self.n_at):
            for j in range(self.n_at):
                for k in range(self.n_at):
                    for l in range(self.n_at):
                        seq = [i, j, k, l]
                        seen.append(seq)
                        seq_rev = [seq[0]] + seq[:0:-1]
                        
                        seq_rev_1 = [seq[0]] + [seq[2]] + [seq[1]] + [seq[3]]
                        rev = seq_rev in seen
                        rev1 = seq_rev_1 in seen 
                        if rev == False and rev1 == False:
                            tau_val = self.tau_valid( i, j, k, l)
                            #print(tau_val)
                            if tau_val == True:
                                tau = self.dihedral_angle( i, j, k, l)
                                print(f'Atom #{i} - #{j} - #{k} - #{l} : {tau}')
    
    
    

    
    
    
    
        
   

#%%



#%%       


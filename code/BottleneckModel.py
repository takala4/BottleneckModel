# -*- coding: utf-8 -*-
"""Vickrey's bottleneck model

This is a numerical program of Vickrey's bottleneck model.
Departure time choice problem
DSO and DUE

"""

import numpy as np
import cvxpy as cp

class parameter:
    """parameter
    
    This is a parameter class.

    Attributes:
        
    Args:
        K (int) : Number of groups
        Q (np.array) : Total demand (vector)
        T (int) : Number of time steps
        s (np.array) : Schedule delay matrix
        mu (float) : capacity

    """
    def __init__(self, K, Q, T, s, mu):
        self.K = K 
        self.Q = Q 
        self.T = T 
        self.s = s
        self.mu = mu
        
    

class DSO_model:
    """DSO model 
    This is a DSO model class.

    Args:

    """
    def __init__(self, Parameter):
        self.Parameter = Parameter
        self.Create_Sigma()
        self.Create_A()
        self.Create_Q()
        self.Create_mu()
        self.Create_s()

        
    def Create_Sigma(self):
        """
        Create matrix Sigma (OD demand constraint)
        """
        self.Sigma = np.kron(np.ones(self.Parameter.T, dtype=np.float),\
                             np.identity(self.Parameter.K, dtype=np.float))
    def Create_A(self):
        """
        Create matrix A (Bottleneck capacity constraint)
        """
        A = np.eye(self.Parameter.T, self.Parameter.T)
        self.A = np.kron(A, np.ones(shape=(1, self.Parameter.K)))
        
    def Create_Q(self):
        """
        Create OD demand vector Q
        """
        self.Q = self.Parameter.Q
    

    def Create_mu(self):
        """
        Create capacity vector Q
        """
        self.mu = self.Parameter.mu * np.ones(self.Parameter.T)
        

    def Create_s(self):
        """
        Create schedule delay function
        """
        self.s = self.Parameter.s.flatten()
        
        
    def solve(self):
        """
        Method to solve DSO problem as LP
        """
        N = self.Parameter.T*self.Parameter.K
        x = cp.Variable(N)

        solver_list = cp.installed_solvers()
        
        objective   = cp.Minimize(self.s@x)
        constraints = [self.A@x <= self.mu, self.Sigma@x == self.Q, x >= 0]    #制約条件
        prob = cp.Problem(objective, constraints)
        prob.solve(solver=cp.GUROBI)
        
        self.solution = {}
        self.solution['q'] = x.value
        self.solution['p'] = prob.constraints[0].dual_value
        self.solution['rho'] = - prob.constraints[1].dual_value
    

class DUE_model:
    """DUE model 
    This is a DUE model class.

    Args:

    """
    def __init__(self, Parameter):
        self.Parameter = Parameter
        self.Create_Sigma()
        self.Create_A()
        self.Create_Q()
        self.Create_mu()
        self.Create_s()
        self.Create_M()
        self.Create_b()
        
    def Create_Sigma(self):
        """
        Create matrix Sigma (OD demand constraint)
        """
        self.Sigma = np.kron(np.ones(self.Parameter.T, dtype=np.float),\
                             np.identity(self.Parameter.K, dtype=np.float))
    def Create_A(self):
        """
        Create matrix A (Bottleneck capacity constraint)
        """
        A = np.eye(self.Parameter.T, self.Parameter.T)
        self.A = np.kron(A, np.ones(shape=(1, self.Parameter.K)))
        
    def Create_Q(self):
        """
        Create OD demand vector Q
        """
        self.Q = self.Parameter.Q
    

    def Create_mu(self):
        """
        Create capacity vector Q
        """
        self.mu = self.Parameter.mu * np.ones(self.Parameter.T)
        

    def Create_s(self):
        """
        Create schedule delay function
        """
        self.s = self.Parameter.s.flatten()
        
    def Create_M(self):
        """
        Create create matrix M
        """
        Num_ODTIME = self.Parameter.K*self.Parameter.T
        M11 = np.zeros(shape=(Num_ODTIME, Num_ODTIME))

        
        M22 = np.zeros(shape=(self.Parameter.T, self.Parameter.T))
        M23 = np.zeros(shape=(self.Parameter.T, self.Parameter.K))
        M33 = np.zeros(shape=(self.Parameter.K, self.Parameter.K))

        self.M = np.block([[M11   , self.A.T , -self.Sigma.T],\
                           [-self.A, M22     , M23],\
                           [self.Sigma, M23.T  , M33]])
        
    def Create_b(self):
        """
        Create create vector b
        """
        self.b = np.block([self.s, self.mu, -self.Q])



    def solve(self):
        """
        Method to solve DUE problem as QP
        """
        N = self.M.shape[0]
        x = cp.Variable(N)

        solver_list = cp.installed_solvers()
        
        objective   = cp.Minimize(self.b@x)
        constraints = [self.M@x >= - self.b  , x >= 0]    #制約条件[]
        prob = cp.Problem(objective, constraints)
        prob.solve(solver=cp.GUROBI)

        
        self.solution = {}
        T = self.Parameter.T
        K = self.Parameter.K

        self.solution['q'] = x.value[:T*K:]
        self.solution['w'] = x.value[T*K:T*K+T:]
        self.solution['rho'] = x.value[T*K+T:]
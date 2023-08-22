# -*- coding: utf-8 -*-
"""
Created on Fri Jul  1 11:36:34 2022

@author: guill
"""



import numpy as np
import matplotlib.pyplot as plt


# SHAMIR SECRET SHARING (K,N) SCHEME: GRADE K-1 POLYNOMIAL

def Shamir_Polynomial(x, secret, coefficients):
    
    # F(x) = y + m_1 * x + ... + m_(k-1) * x ^ (k-1)
    # y is the secret, m_i the randomized coefficients
    
    F = secret
    
    grade = 1
    
    for m_i in coefficients:
        
        F += m_i * x ** grade
        
        grade += 1

    return F


def randomize_coefficients(k):
    
    # With this function we create a set of k-1 coefficients to input in the
    # Shamir_Polynomial function
    
    return (2 * np.random.rand(k - 1)) - 1 # uniform [-1, 1)
    

def Shares_creation(n, k, secret, coefficients):
    
    # We will use the obtained F(x) to generate n shares of which only k are necessary
    
    if type(k) is not int or type(n) is not int:
    
        raise TypeError("n and k must be integers")
        
    x_i = np.linspace(1, n, n)
    
    Shares = Shamir_Polynomial(x_i, secret, coefficients)
    
    Shares_list = []  # We will introduce all the shares into a list of coordinates (arrays)
    
    for index in range(0, n):
    
        Shares_list.append(np.array([x_i[index], Shares[index]]))
        
    return Shares_list


def Secret_Reveal(k_shares):
    
    result = 0
    
    k = len(k_shares)
    
    for share in k_shares:
        
        x_i = share[0]
        F_i = share[1]
        
        multiplication = 1
        
        for j in k_shares:
            
            if j[0] != x_i:
                
                value = j[0] / (x_i - j[0])
            
            else:
            
                value = 1
                
            multiplication *= value
            
        result += F_i * multiplication 

    return round(result * (-1) ** (k - 1) , 8)


# INPUTS 

secret = 0.11223344
n = 10 # Number of shares created 
k = 7 # Threshold: minimum number of shares to decrypt the secret
u = 7 # Used shares for the reconstruction 

# SHARE CREATION

coef_test = randomize_coefficients(k)

shares = Shares_creation(n, k, secret, coefficients = coef_test)

# SECRET DECRYPTION

using_shares = shares[:u] 

recovered_secret = Secret_Reveal(k_shares = using_shares)

print('Recovered secret:', recovered_secret)

# POLYNOMIAL PLOT

x = np.linspace(0, 10, 1100)

plt.figure(0)
plt.plot(x, Shamir_Polynomial(x, secret, coefficients = coef_test))
plt.show()








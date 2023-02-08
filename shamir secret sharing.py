# -*- coding: utf-8 -*-
"""
Created on Fri Jul  1 11:36:34 2022

@author: guill
"""



import numpy as np
import matplotlib.pyplot as plt

secret_test = 0.11223344

# SHAMIR SECRET SHARING (K,N) SCHEME: GRADE K-1 POLYNOMIAL

def Shamir_Polynomial(x, coefficients, secret):
    
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
    
# =============================================================================
# 
# secret_test = 0
# 
# x = np.linspace(0, 10, 1100)
# plt.figure(0)
# for n in range(0,9):
#     plt.subplot(331 + n)
#     plt.plot(x, Shamir_Polynomial(x, coefficients = randomize_coefficients(k_shares = 7), secret = secret_test))
#     
# plt.show()
# 
# =============================================================================

def Shares_creation(n, k, secret, coefficients):
    
    # We will use the obtained F(x) to generate n shares of which only k are necessary
    if type(k) is not int or type(n) is not int:
        raise TypeError("n and k must be integers")
        
    x_i = np.linspace(1, n, n)
    Shares = Shamir_Polynomial(x = x_i, coefficients = coefficients, secret = secret)
    
    Shares_list = []  # We will introduce all the shares into a list of coordinates (arrays)
    for index in range(0, n):
        Shares_list.append(np.array([x_i[index], Shares[index]]))
        
    #return np.array([x_i, Shares])
    return Shares_list


# =============================================================================
# 
# def delta(share_i, x, k_shares):
#     
#     k_shares_copy = k_shares.copy()
#     i = np.where(k_shares_copy[:,0] == share_i[0])[0][0]
#     iterating_group = np.delete(k_shares_copy, i, 1)
#     result = 1
#     
#     for j in iterating_group[0,:]:
#         result *= (x - j) / (i + 1 - j)
# 
#     return result
# 
# test = delta(share_i = shares[:,0], x = 0, k_shares = using_shares)
# 
# =============================================================================

# =============================================================================
# def Secret_Reveal(k_shares):
#     
#     result = 0
#     k = len(k_shares[0,:])
#     
#     for F_i in k_shares[1,:]:
#         
#         index = k_shares[1,:].index(F_i)
#         x_i = k_shares[index]
#         multiplication = 1
#         
#         for j in k_shares[0,:]:
#             
#             if j != x_i:
#                 value = j / (x_i - j)
#             else:
#                 value = 1
#                 
#             multiplication *= value
#             
#         result += F_i * multiplication 
# 
#     return result * (-1) ** (k - 1)
# =============================================================================

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

coef_test = randomize_coefficients(k = 7)

shares = Shares_creation(n = 10, k = 7, secret = secret_test, coefficients = coef_test)

using_shares = shares[:-3]

recovered_secret = Secret_Reveal(k_shares = using_shares)

x = np.linspace(0, 10, 1100)
plt.figure(0)
# =============================================================================
# for n in range(0,9):
#     plt.subplot(331 + n)
# =============================================================================
plt.plot(x, Shamir_Polynomial(x, coefficients = coef_test, secret = secret_test))
plt.show()








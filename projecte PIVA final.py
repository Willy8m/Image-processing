# -*- coding: utf-8 -*-
"""
Created on Mon Aug 15 11:16:02 2022

@author: Oriol Juan Sabater & Guillem Barta Gonzalez
"""

import skimage.data as data
import numpy as np
import matplotlib.pyplot as plt

'''

IMPORTANT COMMENTARY:

As it is explained in this paper, this methodology isn't a full working k out 
of n scheme. So keep in mind that these are just the steps we could interpret 
from K.Shankar's and Dr.P.Eswaran's paper. 

When executing the program, you will find three figures. The first one 
contains the n encrypted shares handed to each user. The second one 
contains what the stacking of the decrypted shares would look like. The third 
one gives evidence that the method on step 7 doesn't even encrypt the shares 
before applying the XOR operation. Which means that any participant with his 
share and the key used for the XOR operation can reveal some information about 
the original image.

'''


#%% ENCRYPTING THE IMAGE

# STEP 1 : we start by proposing a k out of n sharing secret scheme, that means
# we will have to stack k of the n shares to get any info about the secret 
# image (referenced as I_hxw in the original paper)

image = data.astronaut()

n = 4 # This could be variable, but there is no interest to it, given there is
      # no k threshold. So keep it at n = 4 for the code to work

# STEPS 2,3,4,5 : We have to generate n-1 random numbers the sum of which is 1
# for every individual pixel and color channel. We will later project these
# numbers to the pixel values

# That means we need a matrix of dimensions (height, width, channels, 
# n-1 shares). The dirichlet function does exactly that.

dirichlet_matrix = np.random.dirichlet(np.ones(n - 1), (512,512,3))

# STEP 6 : We have to sort these numbers in ascending order for each pixel. The
# np.sort() method sorts the last axis of an array, which is convenient for
# our structure

dirichlet_matrix = np.sort(dirichlet_matrix)

# Now we will project (multiply) the dirichlet matrix on every pixel and store 
# it in the 'auxiliary_matrix'. We also have to add the original pixel value,
# which will and has to be the largest of every set.

auxiliary_matrix = np.zeros([512,512,3, n], dtype=np.uint8())

for i in range(0, n - 1): # (n-1) shares
    auxiliary_matrix[:,:,:,i] = np.uint8(dirichlet_matrix[:,:,:,i] * image)

auxiliary_matrix[:,:,:, n - 1] = image # Greatest value from every set is the 
                                       # image itself


# STEP 7 : Now we can start generating individual shares. 

# The scheme to generate these shares is as follows. The sorted numbers 
# corresponding to every pixel (4th dimension of auxiliary_matrix) are
# subtracted by its anterior position. This means that we will store the 
# values corresponding to: 1st - 0, 2nd - 1st, 3rd - 2nd, and so on (being 1st
# the lowest value of the ascending set). 

# These new values form what we call basic matrices

basic_matrices = np.zeros([512,512,3, n], dtype=np.uint8())

for j in range(0,3): # color channels (RGB)
    memory = 0 # restart the memory before operating the lowest number
    for i in range(0, n): # n shares 
        basic_matrices[:,:,j,i] = auxiliary_matrix[:,:,j,i] - memory
        memory = auxiliary_matrix[:,:,j,i]


# STEP 8 : To encrypt the shares we generate key matrices for each color

shares_store = np.zeros([512,512,3, n], dtype=np.uint8())
keys = np.uint8(np.random.rand(512,512,3) * 255)

# step 9 : We use basic XOR encryption between the basic matrices and the keys

for i in range(0, n): 
    share_i = np.bitwise_xor(basic_matrices[:,:,:,i], keys[:,:,:])
    shares_store[:,:,:,i] = np.uint8(share_i)

# STEP 10 : Now we can give each participant his/her share

plt.figure(1)
plt.suptitle('Shares given to each participant')

for share in range(0, n):
    
    subplot_iterator = 100 + n * 10 + share + 1
    
    text = 'share #' + str(share + 1)
    
    plt.subplot(subplot_iterator, title = text)
    plt.imshow(shares_store[:,:,:,share])
    plt.axis('off')


plt.tight_layout()
plt.show()



#%% RECOVERING THE IMAGE 

# steps 1,2 : We undo the XOR encryption by using the key matrices. In a real 
# case scenario we would have to collect the k shares and stack them, but we 
# already have all the shares stored in the 'shares_store' array.

basic_matrices_recovered = np.zeros((512, 512, 3, n), dtype=np.uint8())

for i in range(0, n):
    share_i = np.bitwise_xor(shares_store[:,:,:,i], keys[:,:,:])
    basic_matrices_recovered[:,:,:,i] = np.uint8(share_i)


# STEPS 3,4 : Now  we just have to stack them to reveal the secret image

plt.figure(2)
plt.suptitle('Example of the reconstruction of shares')

memory = 0

for share in range(1, n):
    
    subplot_iterator = 100 + (n - 1) * 10 + share
    
    text = str(share + 1) + ' stacked shares'
    
    image_recovered = basic_matrices_recovered[:,:,:,share] + memory
    memory = image_recovered
    
    plt.subplot(subplot_iterator, title = text)
    plt.imshow(image_recovered)
    plt.axis('off')


plt.show()



#%% PROOF OF THE ENCRYPTION FLAWS IN STEP 7

'''

We want to show the shares before encrypting them with the key matrices, 
because in a k out of n scheme (as the authors claim) the secret can only be
shown with the combination of shares, not with the help of a key.

So, if we show the content of 'basic_matrices', which are the shares before
encrypting them with the keys, we can see that they reveal most of the
original image information.

'''

plt.figure(3)
plt.suptitle('Unencrypted shares (Fig. 3)')

for unencrypted_share in range(0, n):
    
    subplot_iterator = 100 + n * 10 + unencrypted_share + 1
    
    text = '#' + str(unencrypted_share + 1)
    
    plt.subplot(subplot_iterator, title = text)
    plt.imshow(basic_matrices[:,:,:,unencrypted_share])
    plt.axis('off')


plt.show()

#%%

plt.figure(4)
plt.suptitle('Final results (Fig. 2)')

plt.subplot(241, title = '(a)')
plt.imshow(image)
plt.axis('off')

plt.subplot(242, title = '(b)')
plt.imshow(shares_store[:,:,:,0])
plt.axis('off')

plt.subplot(243, title = '(c)')
plt.imshow(shares_store[:,:,:,1])
plt.axis('off')

plt.subplot(244, title = '(d)')
plt.imshow(shares_store[:,:,:,2])
plt.axis('off')

plt.subplot(245, title = '(e)')
plt.imshow(shares_store[:,:,:,3])
plt.axis('off')

plt.subplot(246, title = '(f)')
plt.imshow(basic_matrices[:,:,:,0] + basic_matrices[:,:,:,1])
plt.axis('off')

plt.subplot(247, title = '(g)')
plt.imshow(basic_matrices[:,:,:,0] + basic_matrices[:,:,:,1] + basic_matrices[:,:,:,2])
plt.axis('off')

plt.subplot(248, title = '(h)')
plt.imshow(basic_matrices[:,:,:,0] + basic_matrices[:,:,:,1] + basic_matrices[:,:,:,2] + basic_matrices[:,:,:,3])
plt.axis('off')

plt.tight_layout()



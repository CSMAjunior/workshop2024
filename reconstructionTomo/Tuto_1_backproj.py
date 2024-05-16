'''
Tutorial CSMA Junior:
1. Back projection
-----
Created Date: Tuesday April 30th 2024
Author: Dufour John-Eric
-----
'''
#%%
import matplotlib.pyplot as plt
import numpy as np
import scipy as sp
from math import sin, cos, pi
from scipy.fft import fft, ifft
from skimage.transform import radon
from utilitiesCSMA import * 


# %% Parameters
Maxangle = 180 # Maximum angle (degrees) used for projection (can be >360°)
Nangles = 180 # Number of projections

tuto=True

# %% Tomography projection
# Definition of the phantom
obj = shepp_logan(256)
if tuto:
    plt.imshow(obj[:, :])
    plt.colorbar()
    plt.show()

# List of projection angles
angs = np.linspace(0, Maxangle, Nangles)
ang = angs[:]

# Projection of the phantom on the detector (using radon transform)
simr = radon(obj, theta=ang, preserve_range=True)


# %% Reconstruction

if tuto:
    plt.imshow(simr)
    plt.colorbar()
    plt.show()


# Reconstruction using backprojection (To be implemented)
recon = backp(ang, simr)


plt.imshow(recon)
plt.colorbar()
plt.title("Backprojection without filtering")
plt.show()
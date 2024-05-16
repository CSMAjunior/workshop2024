'''
Tutorial CSMA Junior:
Tomo Reconstruction using FBP
-----
Created Date: Tuesday April 30th 2024
Author: Dufour John-Eric
'''
#%%
import matplotlib.pyplot as plt
import numpy as np
import scipy as sp
from math import sin, cos, pi
from scipy.fft import fft, ifft
from skimage.transform import radon, rescale
from utilitiesCSMA import * 


# %% Parameters
Maxangle = 360  # Maximum angle (degrees) used for projection (can be >360°)
Nangles = 180  # Number of projections

tuto = True



# %% Tomography projection
# Definition of the phantom
obj = shepp_logan()
if tuto:
    plt.imshow(obj[:, :])
    plt.colorbar()
    plt.show()

# List of projection angles
angs = np.linspace(0, Maxangle, Nangles)
ang = angs[:]

# Projection of the phantom on the detector (using radon transform)
simr = radon(obj, theta=ang,preserve_range=True)

# Noise simulation (To be added)
noise_value = np.max(simr)*0.1
np_sinogram = simr + noise_value*np.random.random(size=simr.shape)
np_sinogram[100:102,:]=0

# %% Reconstruction
# FBP reconstruction (To be added):
# With filtering
# Ramp filter

recon_filtered_sinogram = FBP(ang, np_sinogram)

plt.imshow(recon_filtered_sinogram)
plt.title("FBP reconstruction with a ramp filter")
plt.colorbar()
plt.show()

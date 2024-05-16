'''
Tutorial CSMA Junior:
Tomo Reconstruction using FBP
-----
Created Date: Tuesday April 30th 2024
Author: Dufour John-Eric
-----
'''
# %%
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

# Noise simulation (To be added)
np_sinogram = simr


# %% Reconstruction

# Sinogram manipulation
sinogram_shape = np_sinogram.shape[0]

# Add padding
projection_size_padded = max(64, int(2 ** np.ceil(np.log2(2 * sinogram_shape))))
pad_width = ((0, projection_size_padded - sinogram_shape), (0, 0))
padded_sinogram = np.pad(np_sinogram, pad_width, mode="constant", constant_values=0)

if tuto:
    plt.imshow(padded_sinogram)
    plt.colorbar()
    plt.show()

# FBP reconstruction (To be added):
# Process:
#   - Perform FFT of the sinogram
#   - Filter in Fourier space
#   - Perform iFFT
#   - Backproject onto the volume

# With filtering
# Ramp filter
# To be implemented


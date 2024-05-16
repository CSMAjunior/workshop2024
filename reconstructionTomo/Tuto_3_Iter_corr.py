'''
Tutorial CSMA Junior:
Tomo Reconstruction using ART
-----
Created Date: Sunday May 12th 2024
Author: Dufour John-Eric
-----
'''
import matplotlib.pyplot as plt
import numpy as np
import scipy as sp
from math import sin, cos, pi
from scipy.fft import fft, ifft
from skimage.transform import radon, rescale
from utilitiesCSMA import * 


# %% Parameters
Maxangle = 90 # Maximum angle (degrees) used for projection (can be >360°)
Nangles = 180    # Number of projections

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

plt.imshow(simr)
plt.colorbar()
plt.show()

im = np.zeros_like(obj).astype(np.float64)

im_out = Recon_irt(im, ang, simr, 50) # To be implemented

plt.imshow(im_out)
plt.colorbar()
plt.show()
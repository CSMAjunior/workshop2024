'''
UtilitiesCSMA.py

Functions to be used during the practical sessions of the CSMA Junior workshop 
Author: Dufour John-Eric
-----
'''

import numpy as np
from math import cos, sin, pi
from scipy.fft import fft, ifft
from skimage.transform import radon, iradon, warp
import scipy as sp
import matplotlib.pyplot as plt


def shepp_logan(siz=512):
    '''
    Head phantom definition
    Returns:
    im (np.array of int): head phantom of siz: siz
    '''
    im = np.zeros((siz, siz))
    lin = np.linspace(-siz//2, siz//2,siz)
    ix, iy = np.meshgrid(lin, lin)
    ix.shape
    ell = lambda x,y,u,v,a,b,t : (((x-u)*cos(t)+(y-v)*sin(t))/a)**2+(((x-u)*sin(t)-(y-v)*cos(t))/b)**2
    im += np.where(ell(ix, iy, 0*siz//2, 0*siz//2, 0.69*siz//2, 0.92*siz//2, 0*pi/180) < 1, 1, 0)
    im += np.where(ell(ix, iy, 0*siz//2, 0.0184*siz//2, 0.6624*siz//2, 0.874*siz//2,0*pi/180) < 1, -0.8, 0)
    im += np.where(ell(ix, iy, 0.22*siz//2, 0.*siz//2, 0.11*siz//2, 0.31*siz//2,-18.*pi/180) < 1, -0.2, 0)
    im += np.where(ell(ix, iy, -0.22*siz//2, 0.*siz//2, 0.16*siz//2, 0.41*siz//2,18.*pi/180) < 1, -0.2, 0)
    im += np.where(ell(ix, iy, 0.*siz//2, 0.35*siz//2, 0.21*siz//2, 0.25*siz//2,0.*pi/180) < 1, 0.1, 0)
    im += np.where(ell(ix, iy, 0.*siz//2, 0.1*siz//2, 0.046*siz//2, 0.046*siz//2,0.*pi/180) < 1, 0.1, 0)
    im += np.where(ell(ix, iy, 0.*siz//2, -0.1*siz//2, 0.046*siz//2, 0.046*siz//2,0.*pi/180) < 1, 0.1, 0)
    im += np.where(ell(ix, iy, -0.08*siz//2, -0.605*siz//2, 0.046*siz//2, 0.023*siz//2,0.*pi/180) < 1, 0.1, 0)
    im += np.where(ell(ix, iy, 0.*siz//2, -0.605*siz//2, 0.023*siz//2, 0.023*siz//2,0.*pi/180) < 1, 0.1, 0)
    im += np.where(ell(ix, iy, 0.06*siz//2, -0.605*siz//2, 0.023*siz//2, 0.046*siz//2,0.*pi/180) < 1, 0.1, 0)
    return np.flipud(255*im).astype(int)


def ramp_filter(siz):
    '''
    Ramp filter from skimage.iradon
    returns:
    ramp (np.array): FFT of a ramp filter of size siz
    '''
    # Computing the ramp filter from the fourier transform of its
    # frequency domain representation lessens artifacts and removes a
    # small bias as explained in [1], Chap 3. Equation 61
    n = np.concatenate(
        (
            # increasing range from 1 to size/2, and again down to 1, step size 2
            np.arange(1, siz / 2 + 1, 2, dtype=int),
            np.arange(siz / 2 - 1, 0, -2, dtype=int),
        )
    )
    f = np.zeros(siz)
    f[0] = 0.25
    f[1::2] = -1 / (np.pi * n) ** 2

    # See "Principles of Computerized Tomographic Imaging" by Avinash C. Kak and Malcolm Slaney,
    # Chap 3. Equation 61, for a detailed description of these steps
    return 2 * np.real(fft(f))[:, np.newaxis]


def backp(angs, sinos):
    '''
    Performs backprojection
    To be implemented
    '''
    N, n_proj = sinos.shape
    im_recon = np.zeros((N, N))
    # add operations here
    return im_recon


def FBP(angs, sino):
    """
    Performs FBP reconstruction
    To be implemented
    """
    # add operations here
    return 0


def Recon_irt(initial_guess, angs, sino, Niter, relax=1, positivity=True):
    """
    Performs IRT reconstruction
    To be implemented
    """
    return initial_guess


def proj(x, angs):
    """
    Performs projection
    """
    out = np.zeros((x.shape[0], len(angs)))
    for i, angle in enumerate(np.deg2rad(angs)):
        cos_a, sin_a = np.cos(angle), np.sin(angle)
        R = np.array(
            [
                [cos_a, sin_a, -x.shape[0]//2 * (cos_a + sin_a - 1)],
                [-sin_a, cos_a, -x.shape[0]//2 * (cos_a - sin_a - 1)],
                [0, 0, 1],
            ]
        )
        rotated = warp(x, R, clip=False)
        out[:, i] = rotated.sum(0)
    return out


def A(x, angs):
    return radon(x, angs)


def AT(x, angs):
    return backp(angs, x)
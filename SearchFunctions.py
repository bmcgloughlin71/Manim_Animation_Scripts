#Import Things
import numpy as np
import matplotlib.pyplot as plt
import random
import argparse
import pycw as cw
#---

#--- fitting and statistics calculations
import scipy.integrate as integrate
from scipy.stats import chi2
from scipy.optimize import curve_fit
from scipy.stats import ks_2samp, anderson_ksamp
from scipy.stats import ncx2
#---

#--- dealing with large numbers, such as nTemplates
#--- things work slower if you set dps higher, and calculations break down if you set this lower
import mpmath
mpmath.mp.dps = 80
#---


## FUNCTIONS ##

def num_templates(dfreq, dfdot, num_skypoints, gamma, fband, f1band):
    templates = fband/dfreq * (f1band)/dfdot * num_skypoints * gamma 
    return templates

def normed2Fpdf(avg_2Fs, nTemplates, nSeg):
    total_2Fs = avg_2Fs * nSeg    # convert to total 2F values from all segments
    bin_width = avg_2Fs[1] - avg_2Fs[0]
    pdf_value = bin_width * nSeg * nTemplates * chi2.pdf(total_2Fs, 4*nSeg) * np.exp((nTemplates-1) * np.log(chi2.cdf(total_2Fs, 4*nSeg)))
    return pdf_value
    
def my_pdf(x,k):
    x,k = mpmath.mpf(x), mpmath.mpf(k)
    if x < 0: return 0
    return 1/(2**(k/2) * mpmath.gamma(k/2)) * (x**(k/2-1)) * mpmath.exp(-x/2)

def my_cdf(x,k): 
    x,k = mpmath.mpf(x), mpmath.mpf(k) 
    return mpmath.gammainc(k/2, 0, x/2, regularized=True)

def normed2Fpdf_bigN(xvals, nTemplates, nSeg):
    return nSeg * nTemplates * my_pdf(xvals*nSeg, 4*nSeg) * my_cdf(xvals*nSeg, 4*nSeg)**(nTemplates-1)

def expected2F_bigN(nTemplates, nSeg):    # calculate the expected value for max 2F given nTemplates
    intEnd=20 # careful
    mu, mu_err = integrate.quad(lambda x: x * normed2Fpdf_bigN(x, nTemplates, nSeg), 0, intEnd)
    return mu
    
    
## Pattern Functions from PyCW ##


def get_geom_factor(calls, reftime, Tsft, Tseg):
    catalog = cw.DataCatalog(timebase=Tsft, t_seg=Tseg, detectors="H1,L1", max_timespan=[1238166018,1238166018+15984000])
    search_space = cw.DopplerSpace(freq=[99.9,100.2], f1dot=[-2.6e-9, 0.3e-9], reftime=[ reftime ])
    fstat = cw.Fstatistic(catalog, search_space, inject_noise_asd=1, assume_noise_asd=1)
    values = []
    for i in range(calls):
        cos_Iota = np.random.uniform(-1, 1, 1)[0]
        Psi = np.random.uniform(-np.pi/4, np.pi/4, 1)[0]
        Alpha = np.random.uniform(0, 2*np.pi,1)[0]
        Delta = np.random.uniform(-np.pi/2, np.pi/2, 1)[0]

        alpha_1 = 1/4 * (((1 + cos_Iota**2)**2) * (np.cos(2*Psi)**2)) + (cos_Iota**2) * (np.sin(2*Psi)**2)
        alpha_2 = 1/4 * (((1 + cos_Iota**2)**2) * (np.sin(2*Psi)**2)) + (cos_Iota**2) * (np.cos(2*Psi)**2)
        alpha_3 = 1/4 * (((1 - cos_Iota**2)**2) * np.sin(2*Psi) * np.cos(2*Psi))

        antenna = fstat.get_antenna_patterns(sky_position={"alpha":Alpha,"delta":Delta})
        values.append(25/4*(alpha_1 * antenna.m_munu.A + alpha_2 * antenna.m_munu.B + 2 * alpha_3 * antenna.m_munu.C))
    return values
    
    
def quietPrint(msg, quiet):
  if not quiet:
    print(msg)


def Sig_2F(avg_2Fs, nSeg, rho):
    total_2Fs = avg_2Fs * nSeg    # convert to total 2F values from all segments
    #bin_width = avg_2Fs[1] - avg_2Fs[0]
    pdf_value = ncx2.pdf(total_2Fs, 4*nSeg, rho)
    return pdf_value

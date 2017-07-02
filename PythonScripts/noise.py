# Description: takes list of fits files containing 2D spectra. The variance in
#              the distribution of the pixels at each wavelength of a series of
#              2D spectra are outputted as FITS files with the same header
# Input:       text file of list of 2D spectra FITS file

import numpy as np
from astropy.io import fits
import sys
import pdb

#To do:
#1.) Check Poisson vs Gaussian variance
#2.) Check extension on the FITS file
#3.) Check that data is read in as 2D array
#_______________________________________________________________________________
# Calculates Poisson variance


# The follwoing function takes the spectral data as input and outputs the
# data with the "pillarboxing" on the sides cut off as well as the indices where
# it was cut off. These "pillarboxing" pixels all have a value of -1.
# **Note: the end_index is the index for the first pixel on the right pillar.
def cutPillars(olddata):
    #Remove left pillar
    leftcut = np.where(olddata>-1)[2]  #the data has 3 dimensions

    #Remove right pillar
    reversedata = np.flip(olddata, 2)[0][0][:]
    rightcut = np.where(reversedata>-1)[0]   #this is still the flipped array

    #Get endpoints of the data
    beginning_index = leftcut[0]
    end_index = rightcut[0]     #although not 0th indexed when coming from end,
                                #scope operator excludes endpoint anyways

    #Extract spectrum
    newdata = olddata[0][0][:]
    newdata = newdata[beginning_index: -end_index]

    return newdata, beginning_index, end_index
#_______________________________________________________________________________
#Input
filelist = sys.argv[1]

with open(filelist) as listobject:
    for filename in listobject:
        #Open things
        filename = filename.rstrip(' \n')
        hdulist = fits.open(filename)
        scidata = np.array([hdulist[0].data])

        #Remove pillarboxing one row at a time
        for rownumber in range(np.size(scidata,0)):
            cutPillars(scidata[rownumber, 0]

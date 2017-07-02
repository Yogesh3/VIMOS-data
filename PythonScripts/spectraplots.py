# Description: reads in list of 1D spectra files and plots them
# Input:       csv text file with names of the spectra and error files

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
from astropy.io import fits
import csv
import pdb
import math
import sys

# ________________________________________________________________________________
# The following function takes as input the header and length of a spectrum fits
# file as well as the points where the spectrum was cut to ignore the pillarboxing
# It maps the dispersion axis from pixels to wavelength.
def mapWavelength(header, length, top, bottom):
    # Data Dictionary
    # beginning  = beginning of pillarboxing
    # end        = end of pillarboxing
    # top/bottom = indices of the ends of the

    #Map whole strip, including pillarboxing
    beginning = header['CRVAL1']
    end = length + beginning
    strip = np.arange(beginning, end)

    #Cut the strip to line up with just the spectrum
    return strip[top: -bottom]

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

# The following functions bins spectra into bins of size dx Angstroms.
# Requires x-axis data so that the spectrum y-axis values are lined up with the
# beginning of the appropriate wavelength bin.
# **Note: 3rd argument is boolean telling the function if the data is error data.
#         If so, we bin the data via addition in quadrature.
def binSpectrum(xfull, yfull, isError):
    #Constants
    dx = 3                      #bin width in angstroms
    full_length = xfull.size    #length of the arrays containing unbinned data
    bin_index = 0           #index for binned arrays (as opposed to full_index)

    #Initialize binned arrays
    if full_length%dx == 0:
        xbin = np.zeros(int(full_length/dx))
        ybin = np.zeros(int(full_length/dx))
    else:
        xbin = np.zeros(math.floor(full_length/dx) + 1)
        ybin = np.zeros(math.floor(full_length/dx) + 1)

    #Bin the data
    for full_index in range(0, full_length, dx):
        #Create bins, or "buckets"
        if bin_index == (ybin.size-1):                        #last bin
            bucket = yfull[full_index:]
        else:                                                 #normal bins
            bucket = yfull[full_index : full_index+dx]

        #Add up the spectrum values in bucket
        if isError:            #if error spectrum
            ybin[bin_index] = np.sqrt(np.sum(bucket**2))
        else:                  #if science spectrum
            ybin[bin_index] = np.sum(bucket)

        #Set binned x-axis values
        xbin[bin_index] = xfull[full_index]

        bin_index += 1

    return xbin, ybin
# _______________________________________________________________________________
#Input (csv list of files)
filelist = sys.argv[1]

with open(filelist) as fileobject:
    reader = csv.reader(fileobject)
    for row in reader:
        #Open things
        fluxfilename = row[0]
        errorfilename = row[1]
        plotfilename = fluxfilename[0:-4]
        fluxhdulist = fits.open(fluxfilename)                   #hdulist
        errorhdulist = fits.open(errorfilename)
        fluxdata = np.array([fluxhdulist[0].data])          #data
        errordata = np.array([errorhdulist[0].data])
        fluxheader = fluxhdulist[0].header                  #header
        errorheader = errorhdulist[0].header

        #Extract Spectrum
        yflux, fluxtop, fluxbottom = cutPillars(fluxdata)
        yerror, errtop, errbottom = cutPillars(errordata)

        #Map Wavelengths
        xflux = mapWavelength(fluxheader, fluxdata.shape[2], fluxtop, fluxbottom)
        xerror = mapWavelength(errorheader, errordata.shape[2], errtop, errbottom)
        #If the x axis for the science and error aren't identical after the mapping...
        assert (np.array_equal(xflux,xerror)), ('The science and error spectra have different '
                                                'x values after mapping\nThe file was '
                                                + plotfilename)

        #Binning
        #If the science or error spectra have uneven y and x axes
        assert (yflux.size == xflux.size), ('The science y and x axes have differenct sizen\n'
                                            'The file was ' + plotfilename)
        assert (yerror.size == xflux.size), ('The error y and x axes have differenct sizen\n'
                                             'The file was ' + plotfilename)
        #Bin the science and error spectra
        xflux_binned, yflux_binned = binSpectrum(xflux, yflux, False)
        xerror_binned, yerror_binned = binSpectrum(xflux, yerror, True)
        #Check to make sure that the x axis for the science and error are still the same after binning
        assert (np.array_equal(xflux_binned,xerror_binned)), ('The science and error spectra have different '
                                                              'x values after binning\nThe file was '
                                                               + plotfilename)

        #Plot spectrum
        plt.figure(figsize = (30,6), dpi=120)
        plt.plot(xflux_binned, yflux_binned, 'b')              #plotting
        plt.plot(xerror_binned, yerror_binned, 'r')
        plt.grid(True, which='both')                   #grid
        plt.grid(which='minor', linewidth=0.5)
        plt.grid(which='major', linewidth=1)
        plt.minorticks_on()                             #tick marks
        ax = plt.gca()
        minorLocator = AutoMinorLocator(8)
        ax.xaxis.set_minor_locator(minorLocator)
        plt.xlabel('Wavelength (angstroms)')             #labels
        plt.ylabel('Flux [' + fluxheader['BUNIT'] + ']')
        plt.title(plotfilename[0:-1])
        plt.savefig(plotfilename+'pdf', bbox_inches = 'tight')

        #Close files
        plt.close()
        fluxhdulist.close()
        errorhdulist.close()

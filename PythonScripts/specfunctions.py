''' Functions for use with 1d and 2D spectra.
Due to laziness, documentation is brief, incomplete, and poorly formatted.'''

import numpy as np
from astropy.io import fits

#________________________________________________________________________________
def errorSpec(bigspec):
    '''Calculates 1D error spectrum from 2D spectrum as Poisson noise'''
    return np.sqrt(np.mean(bigspec, axis=0))
# _______________________________________________________________________________
def writeToFits(oldname, data, header, filenumber, quad):
    '''Takes an array and writes it to a fits file
    Inputs
        oldname = full name of the file containing multiple spectra
        data = the spectrum
        header = header of the extension from which data comes; also new header
        filenumber = number of the spectrum
        quad = quadrant number'''

    #New file name
    newname = oldname[19:]
    newname = 'Q' + str(quad) + '_' + str(filenumber) + '_' + newname

    #Write to file
    hdu = fits.PrimaryHDU(data, header=header)
    hdu.writeto(newname, overwrite=True)
#________________________________________________________________________________
def mapWavelength(header, length, top, bottom):
    '''The following function takes as input the header and length of a spectrum fits
    file as well as the points where the spectrum was cut to ignore the pillarboxing
    It maps the dispersion axis from pixels to wavelength.

    Data Dictionary:
        beginning  = beginning of pillarboxing
        end        = end of pillarboxing
        top/bottom = indices of the ends of the spectrum, without pillarboxing '''

    #Map whole strip, including pillarboxing
    beginning = header['CRVAL1']
    end = length + beginning
    strip = np.arange(beginning, end)

    #Cut the strip to line up with just the spectrum
    return strip[top: -bottom]
#_______________________________________________________________________________
def cutPillars(olddata):
    '''The following function takes the spectral data as input and outputs the
    data with the "pillarboxing" on the sides cut off as well as the indices where
    it was cut off. These "pillarboxing" pixels all have a value of -1.

    Input
        olddata = 1D array containing spectrum

    **Note: the end_index is the index for the first pixel on the right pillar.'''

    #Remove left pillar
    leftcut = np.where(olddata > -1)[0]  #the data has 1 dimension

    #Remove right pillar
    reversedata = np.flip(olddata, 0)     #the data has 1 dimension
    rightcut = np.where(reversedata > -1)[0]   #this is still the flipped array

    #Get endpoints of the data
    beginning_index = leftcut[0]     #these indices are for the element, not dim
    end_index = rightcut[0]     #although not 0th indexed when coming from end,
                                #scope operator excludes endpoint anyways

    #Extract spectrum
    newdata = olddata
    newdata = newdata[beginning_index: -end_index]

    return newdata, beginning_index, end_index
#_______________________________________________________________________________
def binSpectrum(xfull, yfull, isError, dx=2):
    '''The following functions bins spectra into bins of size dx Angstroms.
    Requires x-axis data so that the spectrum y-axis values are lined up with the
    beginning of the appropriate wavelength bin.
    **Note: 3rd argument is boolean telling the function if the data is error data.
            If so, we bin the data via addition in quadrature.'''

    #Constants
    full_length = xfull.size    #length of the arrays containing unbinned data
    bin_index = 0           #index for binned arrays (as opposed to full_index)

    #Initialize binned arrays
    if full_length%dx == 0:
        xbin = np.zeros(int(full_length/dx))
        ybin = np.zeros(int(full_length/dx))
    else:
        xbin = np.zeros(full_length//dx + 1)
        ybin = np.zeros(full_length//dx + 1)

    #Bin the data
    for full_index in range(0, full_length, dx):
        #Create bins, or "buckets"
        if bin_index == (ybin.size-1):                        #last bin
            bucket = yfull[full_index:]
        else:                                                 #normal bins
            bucket = yfull[full_index : full_index+dx]

        #Add up the spectrum values in bucket
        if isError:                                         #if error spectrum
            ybin[bin_index] = np.sqrt(np.sum(bucket**2))
        else:                                              #if science spectrum
            ybin[bin_index] = np.sum(bucket)

        #Set binned x-axis values
        xbin[bin_index] = xfull[full_index]

        bin_index += 1

    return xbin, ybin
# _______________________________________________________________________________

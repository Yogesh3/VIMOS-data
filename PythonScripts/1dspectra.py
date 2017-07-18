# Input:       list of files with multiple 1D spectra in each file
# Description: creates fits file for 1D spctra from file with a bunch of them
#              on each line. Each block of 1d spectra is in a fits fil with 3
#              extensions. The first just has a header. The other two have the
#              data, with the 2nd simply being an extension of the first.

import numpy as np
from astropy.io import fits
import sys
import pdb

#Extracts 1d spectra from block spectra and writes it to a new file
def extraction(specindex, scidata, nameofile, header, filenumber, quad):
    #Extract spectrum
    spectrum = scidata[:, specindex, :]

    #New file name for the 1D spectrum
    newname = filename[19:]
    newname = 'Q' + str(quad) + '_' + str(filenumber) + '_' + newname

    #Save file
    hdu = fits.PrimaryHDU(spectrum, header=header)
    hdu.writeto(newname, overwrite=True)

#_______________________________________________________________________________
#Input
fluxlist = sys.argv[1]
errorlist = sys.argv[2]

#Flux files
for filename in open(fluxlist):
    ctr = 0

    #Open things
    filename = filename.rstrip(' \n')
    hdulist = fits.open(filename)
    scidata1 = np.array([hdulist[1].data])
    header1 = hdulist[1].header
    quadrant1 = header1['hierarch_eso_ocs_con_quad']
    scidata2 = np.array([hdulist[2].data])
    header2 = hdulist[2].header
    quadrant2 = header2['hierarch_eso_ocs_con_quad']

    #First extension
    for specnum in range(0, scidata1.shape[1]):
        ctr = ctr+1
        extraction(specnum, scidata1, filename, header1, ctr, quadrant1)

    #Second extension
    for specnum in range(0, scidata2.shape[1]):
        ctr = ctr + 1
        extraction(specnum, scidata2, filename, header2, ctr, quadrant2)

#Error files
for filename in open(errorlist):
    ctr = 0

    #Open things
    filename = filename.rstrip(' \n')
    hdulist = fits.open(filename)
    scidata1 = np.array([hdulist[1].data])
    header1 = hdulist[1].header
    quadrant1 = header1['hierarch_eso_ocs_con_quad']
    scidata2 = np.array([hdulist[2].data])
    header2 = hdulist[2].header
    quadrant2 = header2['hierarch_eso_ocs_con_quad']

    #First extension
    for specnum in range(0, scidata1.shape[1]):
        ctr = ctr + 1
        extraction(specnum, scidata1, filename, header1, ctr, quadrant1)

    #Second extension
    for specnum in range(0, scidata2.shape[1]):
        ctr = ctr + 1
        extraction(specnum, scidata2, filename, header2, ctr, quadrant2)

# Description: takes list of fits files containing 2D spectra. The variance in
#              the distribution of the pixels at each wavelength of a series of
#              2D spectra are outputted as FITS files with the same header
# Input:       text file of list of 2D spectra FITS file

import numpy as np
from astropy.io import fits
import sys
import pdb
from specfunctions import cutPillars

#To do:
#1.) Check Poisson vs Gaussian variance

#Input
filelist = sys.argv[1]

#Constants
FLAG_LIMIT = -0.02       # limit below which everything is considered space
FLAG_VALUE = -15         # value to set the empty space to

with open(filelist) as listobject:
    for filename in listobject:
        #Open things
        filename = filename.rstrip(' \n')
        hdulist = fits.open(filename)

        for extension in range(1,3):
            #Get things from block FITS file
            scidata = np.array([hdulist[extension].data])
            header = hdulist[extension].header
            quadrant = header['hierarch_eso_ocs_con_quad']

            #Initializations
            top = 0
            cleandata = []
            move_top = False
            ctr = 0

            for row in range(scidata.shape[0]):
                ctr = ctr + 1
                move_top = False

                #Cut Pillars
                cleanrow = cutPillars(scidata[row, :])
                if cleandata == []:
                    cleandata = cleanrow
                else:
                    cleandata = np.stack((cleandata, cleanrow))

                #Flag the space between the spectra
                if (cleanrow <= FLAG_LIMIT).any():
                    cleanrow.fill(FLAG_VALUE)
                    move_top = True

                #Extract spectrum and Calculate Error
                if (cleanrow == FLAG_VALUE).all() and not (cleandata[row-1, :] == FLAG_VALUE).all():
                    if top == 0:
                        spectrum = cleandata[top:row, :]
                    else:
                        spectrum = cleandata[top+1:row, :]
                    writeToFits(filename, spectrum, header, ctr, quadrant)

                if move_top:
                    top = row

        hdulist.close()

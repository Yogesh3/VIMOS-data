# Input:       1.) text file list of the names of the 1D flux spectra
#              2.) text file list of the names of the 1D error spectra
# Description: Outputs a CSV file with the name of the 1D flux spectra on the
#              left and the name of the 1D error spectra on the right

import numpy as np
from astropy.io import fits
import sys
import pdb

#I/O
fluxlist = sys.argv[1]
errorlist = sys.argv[2]
outputfilename = '1dlist.txt'

#Get ID's from the error spectra
with open(errorlist) as errorobject:
    slit_to_error = {}    #dictionary with key = error file and value = slit id

    for errorfilename in errorobject:
        #Open file
        errorfilename = errorfilename.rstrip(' \n')
        errhdu = fits.open(errorfilename)
        errhdr = errhdu[0].header

        #Add error file's name and slit ID to dictionary
        slit_to_error[errorfilename] = errhdr['slit_id']

        #Close file
        errhdu.close()

#Match ID's to flux spectra
with open(fluxlist) as fluxobject, open(outputfilename, 'w') as outputfile:
    for fluxname in fluxobject:
        #Open file
        fluxfilename = fluxfilename.rstrip(' \n')
        fluxhdu = fits.open(fluxfilename)
        fluxhdr = fluxhdu[0].header

        #Match up flux spectra to error spectra via slit ID's
        slit = fluxhdr['slit_id']
        error_index = list(slit_to_error.values()).index(slit)
        matched_error = list(slit_to_error.keys())[error_index]

        #Output to file
        outputline = fluxfilename + ',' + errorfilename + '\n'
        outputfile.write(outputline)

        #Close file
        fluxhdu.close()

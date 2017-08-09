# Input:       list of table files and list of 2D MOS files
# Description: Extracts 2D spectra and writes to individual files. An extra
#              header card is also added containing the rows removed from
#              the spectrum when calculating the error. Then calculates error
#              spectra from each slit and writes to their own file. Both the 2D
#              and error spectra have their slit ID added to their headers to
#              be used to sync up the flux and error spectra later.

import numpy as np
from astropy.io import fits
import sys
import pdb
from specfunctions import *

#Input
tablelist = sys.argv[1]
blocklist = sys.argv[2]

#Constants
LOWER_FLAG = -0.02       # limit below which everything is considered space
#FLAG_VALUE = -15         # value to set the empty space to

with open(tablelist) as tableobject, open(blocklist) as blockobject:
    #Go through blockfile/table
    for tablename, blockname in zip(tableobject, blockobject):
        specnum = 0

        #Make HDU objects for table and blockfile
        tablename = tablename.rstrip(' \n')
        tablehdu = fits.open(tablename)
        blockname = blockname.rstrip(' \n')
        blockhdu = fits.open(blockname)

        #Go through extensions
        for extension in range(1,3):
            #Get data from blockfile and table
            image = blockhdu[extension].data
            header = hdulist[extension].header
            quadrant = header['hierarch_eso_ocs_con_quad']
            tabdata = tablehdu[extension].data
            col_position = np.flip(tabdata['position'], 0)
            col_length = np.flip(tabdata['length'], 0)
            col_slitID = np.flip(table['slit_id'], 0)

            #Go through 2D spectra
            for slitindex in range(table.size):
                #Extract spectrum
                top = col_position[slitindex]
                bottom = col_position[slitindex] + col_length[slitindex]
                spectrum = image[top:bottom]
                spectrum, dummy1, dummy2 = cutPillars(spectrum)

                specnum = specnum+1

                #Write 2D spectrum to filename
                newheader = blockhdu[extension].header
                newheader.set('slit_id', col_slitID[slitindex])
                quadrant = newheader['hierarch eso ocs con quad']
                writeToFits(blockname, spectrum, newheader, specnum, quadrant, '2d')

                #Remove bad rows
                badrows = np.where(spectrum < LOWER_FLAG)[0]
                cleanspec = np.delete(spectrum, badrows, 0)

                #Calculate error and Write to file
                errorspec = errorSpectrum(cleanspec)
                writeToFits(blockname, cleanspec, newheader, specnum, quadrant, 'error', badrows)

        #Close Files
        blockhdu.close()
        tablehdu.close()

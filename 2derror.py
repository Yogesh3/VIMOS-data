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
blocklist = sys.argv[1]
tablelist = sys.argv[2]
binsize = sys.argv[3]

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
            header = blockhdu[extension].header
            quadrant = header['HIERARCH ESO OCS CON QUAD']
            tabdata = tablehdu[extension].data
            col_position = np.flip(tabdata['position'], 0)
            col_length = np.flip(tabdata['length'], 0)
            col_slitID = np.flip(tabdata['slit_id'], 0)

            #Go through 2D spectra
            for slitindex in range(tabdata.size):
                #Extract spectrum
                top = col_position[slitindex]
                bottom = col_position[slitindex] + col_length[slitindex]
                spectrum = image[top:bottom]

                #Cut pillarboxing on spectrum
                dummy, leftend, rightend = cutPillars(spectrum[0,:])
                cleanspec = np.ones((spectrum.shape[0], dummy.size))
                for i in range(spectrum.shape[0]):
                    cleanspec[i,:], dummy1, dummy2 = cutPillars(spectrum[i,:])

                #Remove bad rows
                badrows = np.where(cleanspec < LOWER_FLAG)[0]
                badrows = np.unique(badrows)
                cleanerspec = np.delete(cleanspec, badrows, 0)
                badrows = badrows + top
                badrows_str = ''
                for row in badrows:
                    badrows_str = badrows_str + ' ' + str(row) + ' '

                specnum = specnum+1

                #Add to 2D slit header
                newheader = blockhdu[extension].header
                newheader.set('object sci table', tablename)
                newheader.set('sci extension', extension)
                newheader.set('slit id', col_slitID[slitindex])
                newheader.set('slit index', slitindex)
                newheader.set('2Dspectrum top', top)
                newheader.set('2Dspectrum bottom', bottom)
                header.set('badrows', badrows_str)
                quadrant = newheader['hierarch eso ocs con quad']

                #Write 2D spectrum to filename
                twoDname = writeToFits(blockname, cleanerspec, newheader, specnum, quadrant, '2d')

                #Calculate error and Write to file
                errorspec = errorSpectrum(cleanerspec)

                #Add the pillarboxing back
                leftpad = np.ones(leftend,) * -1
                rightpad = np.ones(rightend,) *-1
                errorspec_padded = np.concatenate([leftpad, errorspec, rightpad])

                #Write to file
                newheader.set('2D file name', twoDname)
                errorname = writeToFits(blockname, errorspec_padded, newheader, specnum, quadrant, 'error')

        #Close Files
        blockhdu.close()
        tablehdu.close()

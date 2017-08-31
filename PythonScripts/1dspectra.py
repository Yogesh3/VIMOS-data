# Input:       1.) text file list of the names of the block flux spectra
#              2.) text file list of the names of the sci tables
# Description: creates fits file for 1D spctra from file with a bunch of them
#              on each line. Each block of 1d spectra is in a fits file with 3
#              extensions. The first just has a header. The other two have the
#              data, with the 2nd simply being a continuation of the first. Also
#              adds a card with the slit number in the header of each 1D file.

import numpy as np
from astropy.io import fits
import sys
import pdb

#Extracts 1d spectra from block spectra and writes it to a new file
def extraction(scidata, nameofile, header, filenumber, quad):
    #Extract spectrum
    spectrum = scidata[:, specindex, :]

    #New file name for the 1D spectrum
    newname = nameofile[19:]
    newname = 'Q' + str(quad) + '_' + str(filenumber) + '_' + newname

    #Save file
    hdu = fits.PrimaryHDU(spectrum, header=header)
    hdu.writeto(newname, overwrite=True)

#_______________________________________________________________________________
#Input
fluxlist = sys.argv[1]
tablelist = sys.argv[2]

with open(fluxlist) as fluxobject, open(tablelist) as tableobject:
    for fluxname, tablename in zip(fluxobject, tableobject):
        specnum = 0

        #Open flux and table files
        fluxname = fluxname.rstrip(' \n')
        fluxhdu = fits.open(fluxname)
        tablename = tablename.rstrip(' \n')
        tablehdu = fits.open(tablename)

        for extension in range(1,3):
            #Get header and image info
            scidata = np.array([fluxhdu[extension].data])
            header = fluxhdu[extension].header
            quadrant = header['HIERARCH ESO OCS CON QUAD']

            #Get table info
            table = tablehdu[extension].data
            cols = table.columns.names     #names of all fields in table
            if 'row_3' in cols:
                rows = np.stack((table['row_1'], table['row_2'], table['row_3']), axis=1)
            else:                  #the second extension often doesn't have 3 objects in any slit
                rows = np.stack((table['row_1'], table['row_2']), axis=1)
            rows = np.flip(rows, axis=0)
            col_slitID = np.flip(table['slit_id'], axis=0)

            #Go through spectra in this extension
            for specindex in range(0, scidata.shape[1]):
                specnum = specnum+1

                #Get slit ID and Add to the header
                slitindex = np.where(rows == specindex)[0]
                try:
                    slit_id = col_slitID[slitindex[0]]
                except IndexError:
                    pdb.set_trace()
                header.set('slit id', slit_id)

                #Add science table name and extension to header
                header.set('object sci table', tablename)
                header.set('sci extension', extension)
                header.set('image row index', specindex)

                #Extract and Write spectrum to file
                extraction(scidata, fluxname, header, specnum, quadrant)

        #Close files
        fluxhdu.close()
        tablehdu.close()























            # #Second extension
            # for specnum in range(0, scidata2.shape[1]):
            #     ctr = ctr + 1
            #     extraction(specnum, scidata2, filename, header2, ctr, quadrant2)

# #Error files
# for filename in open(errorlist):
#     ctr = 0
#
#     #Open things
#     filename = filename.rstrip(' \n')
#     hdulist = fits.open(filename)
#     scidata1 = np.array([hdulist[1].data])
#     header1 = hdulist[1].header
#     quadrant1 = header1['hierarch_eso_ocs_con_quad']
#     scidata2 = np.array([hdulist[2].data])
#     header2 = hdulist[2].header
#     quadrant2 = header2['hierarch_eso_ocs_con_quad']
#
#     #First extension
#     for specnum in range(0, scidata1.shape[1]):
#         ctr = ctr + 1
#         extraction(specnum, scidata1, filename, header1, ctr, quadrant1)
#
#     #Second extension
#     for specnum in range(0, scidata2.shape[1]):
#         ctr = ctr + 1
#         extraction(specnum, scidata2, filename, header2, ctr, quadrant2)

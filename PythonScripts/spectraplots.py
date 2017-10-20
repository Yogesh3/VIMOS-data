# Description: reads in list of 1D spectra files and plots them
# Input:       csv text file with names of the spectra and error files

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
from matplotlib import gridspec
from astropy.io import fits
import specfunctions
import csv
import pdb
import sys

# ________________________________________________________________________________
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
def binSpectrum(xfull, yfull, isError, dx):
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
        if isError:                                          #if error spectrum
            ybin[bin_index] = np.sqrt(np.sum(bucket**2))
        else:                                               #if science spectrum
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
        errordata = np.array([[errorhdulist[0].data]])
        fluxheader = fluxhdulist[0].header                  #header
        errorheader = errorhdulist[0].header

        #Extract Spectrum
        yflux, fluxtop, fluxbottom = cutPillars(fluxdata)
        #pdb.set_trace()
        yerror, errtop, errbottom = cutPillars(errordata)

        #Map Wavelengths
        xflux = specfunctions.mapWavelength(fluxheader, fluxdata.shape[2], fluxtop, fluxbottom)
        xerror = specfunctions.mapWavelength(errorheader, errordata.shape[2], errtop, errbottom)
        #pdb.set_trace()
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
        binsize =
        xflux_binned, yflux_binned = binSpectrum(xflux, yflux, False, binsize)
        xerror_binned, yerror_binned = binSpectrum(xflux, yerror, True, binsize)
        #Check to make sure that the x axis for the science and error are still the same after binning
        assert (np.array_equal(xflux_binned,xerror_binned)), ('The science and error spectra have different '
                                                              'x values after binning\nThe file was '
                                                               + plotfilename)


        #Open up the table and 2D spectrum
        tablename = fluxheader['hierarch object sci table']
        tablehdu = fits.open(tablename)
        tabdata = tablehdu[fluxheader['sci extension']].data
        twoDfilename = errorheader['hierarch 2D file name']
        twoDhdu = fits.open(twoDfilename)
        twoDheader = twoDhdu[0].header
        twoDdata = twoDhdu[0].data

        #Get columns from table
        cols = tabdata.columns.names
        if 'row_3' in cols:        #at most, 3 objects per slit
            rows = np.stack((tabdata['row_1'], tabdata['row_2'], tabdata['row_3']), axis=1)
        elif 'row_2' in cols and not 'row_4' in cols:        #the second extension often doesn't have 3 objects in any slit
            rows = np.stack((tabdata['row_1'], tabdata['row_2']), axis=1)
        else:
            print('There\'s either only one object in the slit or more than 3')
            pdb.set_trace()
        rows = np.flip(rows, axis=0)
        col_slitID = np.flip(tabdata['slit_id'], axis=0)

        #Get stuff from spectra headers
        slit_index = errorheader['hierarch slit index']
        flux_index = fluxheader['hierarch image row index']
        spec_top = twoDheader['hierarch 2Dspectrum top']
        slitID = twoDheader['hierarch slit id']

        #Get boundaries on the 1D flux spectrum in the 2D slit image
        obj_num = np.where(rows[slit_index, :] == flux_index)[0][0] + 1
        col_start = np.flip(tabdata['start_' + str(obj_num)], axis=0)
        col_end = np.flip(tabdata['end_' + str(obj_num)], axis=0)
        lowerbound = col_start[slit_index] - spec_top
        upperbound = col_end[slit_index] - spec_top
#___________________________________________________________________________________________________________________________
        #Begin Plots
        fig = plt.figure(figsize = (30,12), dpi=120)
        gs = gridspec.GridSpec(2, 1, height_ratios=[5,1])

        #Plot 1d spectra
        axtop = plt.subplot(gs[0])
        plt.plot(xflux_binned, yflux_binned, 'b', label='Spectrum')              #plotting
        plt.plot(xerror_binned, yerror_binned, 'r', label='Error')            #axis limits
        plt.xlim(xflux_binned[0], xflux_binned[-1])
        plt.grid(True, which='both')                           #grid
        plt.grid(which='minor', linewidth=0.5)
        plt.grid(which='major', linewidth=1)
        plt.minorticks_on()                                    #tick marks
        minorLocator = AutoMinorLocator(8)
        axtop.xaxis.set_minor_locator(minorLocator)
        plt.xlabel('Wavelength (angstroms)', size=15)                   #labels
        plt.ylabel('Flux [' + fluxheader['BUNIT'] + ']', size=15)
        plt.title(plotfilename[0:-1], size=20)                          #title
        plt.legend()                                                    #legend

        #Add text box
        text = ('slit ID = ' + str(slitID) + '\n' +
                'bin size = ' + str(binsize) + ' Angstroms')
        axtop.text(0.05, 0.9, text, fontsize = 15, linespacing = 1.4, transform = axtop.transAxes, ha = 'left', va='top',
                      bbox = dict(facecolor='white', edgecolor = 'black', pad = 5.0) )

        #Plot 2D spectrum
        axbottom = plt.subplot(gs[1])
        axbottom.set_axis_off()
        mu = np.mean(twoDdata)
        sigma = np.std(twoDdata, ddof=1)
        plt.imshow(twoDdata, clim=(mu-2*sigma, mu+2*sigma), cmap='gray', aspect='auto')

        #Plot marker lines
        # these denote where Reflex thinks the spectra are
        axbottom.axhline(y= lowerbound, linestyle='--', color='lawngreen', dashes= (5,25))
        axbottom.axhline(y= upperbound, linestyle='--', color='lawngreen', dashes= (5,25))

        plt.savefig(plotfilename+'pdf', bbox_inches = 'tight')

        #Close files
        plt.close()
        fluxhdulist.close()
        tablehdu.close()
        errorhdulist.close()
        twoDhdu.close()

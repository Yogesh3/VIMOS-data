The code in this repository is divided into several small Python 3 scripts. Brief descriptions about them and their input files, as well as the order in which to use them are below. The line of code to run each script is also given. Note that the order of the arguments given to the scripts do matter.  
**Be warned**: while the comments throughout the scripts give more detailed and specific information, the comments at the beginning of the scripts may be out of date. The wiki is the most up to date version, so when in doubt, check here.  

## Text files
The text files contain the names of the files to be used in their respective python scripts. The order of the names of the files in these text files **do** matter, so make sure that all changes you make to one file are reflected appropriately across all of them. For instance, if you add another OB worth of data before the last line in 1dblock.txt, you must also add the 2D spectra before the last line in 2dblocklis.txt, etc.

The "core" text files (manually created) are as follows:  
* 1dblocklist.txt : list of the names of the "block" 1D science spectra. By "block" spectra, I mean the MOS files outputted by Reflex that have all of the spectra stacked on top of each other ("...REDUCED..." files).
* tablelist.txt :  list of the object science tables ("...OBJECT_SCI_TABLE..." file). See the *Reflex-Output* tab in the wiki for more information on the science table files.
* 2dblocklist.txt : list of the names of the block 2D science spectra ("...EXTRACTED..." files).


## Python Scripts
* *Script name*: `specfunctions.py`  
*Scripts that use it*: `2derror`, `spectraplots.py`  
*Description*: This file is simply an attempt to consolidate all of the user created functions into one file that can be accessed and used in the various scripts. However, only the above stated scripts actually use it. The other scripts use the functions written directly into them. This is largely due to a mistake that occurred when importing the data into a NumPy array. Instead of simply saying `np.array(some_data)`, I said `np.array([some_data])`. By encapsulating the data into a list and then converting that into a NumPy array, the data was given an extra dimension of size 1, throwing off the code in `specfunctions`. The functions in the specific scripts account for this mistake, and are thus used insead. See *Issues_to_Address* tab in the wiki.

The following scrips are to be run in the order given.
1. ` ipython 1dspectra.py 1dblocklist.txt tablelist.txt`  
Script name: `1dspectra.py`  
Input files: `1dblocklist.txt` and `tablelist.txt`  
Output files (sample): `Q1_1_M1_OB4_MOS_SCIENCE_FLUX_REDUCED.fits`  
Description: This script cuts out the 1D spectra from the block and saves them in individual FITS files. It also adds certain keywords to the headers of the new files, like the name and extension of the science table where the spectrum is found. The output files replace the "PILMOS_MACS2214-13" at the beginning of the block spectra file names with the quadrant number of the spectrum and a number of the spectrum corresponding to the order where it appears in the block spectrum file. This number is independent of the extension (i.e. the 4th spectrum in the second extension of the block spectra file may have the number 40 because it is still counting from the first extension). This gives a quick look at how many spectra exist in that particular OB.

2. `ipython 2derror.py 2dblocklist.txt tablelist.txt`
Script name: `2derror.py`  
Input files: `2dblocklist.txt` and `tablelist.txt`  
Output files (sample):   
Description:

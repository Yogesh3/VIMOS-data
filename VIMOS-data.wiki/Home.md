The code in this repository is divided into several small Python 3 scripts. Brief descriptions about them and their input files, as well as the order in which to use them are below. The line of code to run each script is also given, although if you don't want to keep typing `ipython `, you can make the scripts executables. Note that the order of the arguments given to the scripts do matter.  
**Be warned**: while the comments throughout the scripts give more detailed and specific information, the comments at the beginning of the scripts may be out of date. The wiki is the most up to date version, so when in doubt, check here.  

## Text files
The order of the names of the files in these text files **DO** matter, so make sure that all changes you make to one file are reflected appropriately across all of them. For instance, if you add another OB worth of data before the last line in 1dblock.txt, you must also add the 2D spectra before the last line in 2dblocklis.txt, etc.

The "core" text files are as follows:  
* 1dblocklist.txt : list of the names of the "block" 1D science spectra. By "block" spectra, I mean the MOS files outputted by Reflex that have all of the spectra stacked on top of each other ("...REDUCED..." files).
* tablelist.txt :  list of the object science tables ("...OBJECT_SCI_TABLE..." file).
* 2dblocklist.txt : list of the names of the block 2D science spectra. By "block" spectra, I mean the MOS files outputted by Reflex that have all of the spectra stacked on top of each other ("...REDUCED..." files).

1. ` ipython 1dspectra.py 1dblocklist.txt tablelist.txt`  
Script name: `1dspectra.py`  
Input files: `1dblocklist.txt` and `tablelist.txt`  
Output files (sample): `Q1_1_M1_OB4_MOS_SCIENCE_FLUX_REDUCED.fits`  
Description: This script takes as argument a  (`1dblocklist.txt`) and the list of the science tables (`tablelist.txt`).  It then cuts

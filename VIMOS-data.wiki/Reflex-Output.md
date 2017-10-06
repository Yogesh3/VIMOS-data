The output from Reflex can be complicated, so here is an attempt to clarify any ambiguities.

## From the manual
Sect. 4.4
> object_sci_table.fits: slit positions on the CCD, on the mapped images, and positions of the detected objects within the slits.

Sect. 6.14.2:  
> MOS_SCIENCE_REDUCED: image with extracted objects spectra. This image has the same x size of the image with the extracted slit spectra, MOS_SCIENCE_EXTRACTED, and as many rows as the detected and extracted object spectra. Extracted spectra are written to the image rows listed in the OBJECT_SCI_TABLE product.

> OBJECT_SCI_TABLE: This table is an expansion of the input MOS_SLIT_LOCATION table (see page 113), where the positions and the extraction spatial intervals of the detected objects are also included. This table is produced only if any kind of sky subtraction is requested, otherwise no object detection or extraction is attempted. The object table columns are the following:  

> slit_id: Slit identification number.  
xtop:  x CCD position of central wavelength from left end of slit.  
ytop: y CCD position of central wavelength from left end of slit.  
xbottom: x CCD position of central wavelength from right end of slit.  
ybottom: y CCD position of central wavelength from right end of slit.  
position: First row of the rectified images (such as MOS_SCIENCE_EXTRACTED)
containing the rectified slit spectrum. Image rows are counted from bottom,
starting from 0.  
length: Number of rows in rectified images including the slit spectrum.  
object_1, object_2, ...: Detected objects positions in the rectified images.  
start_1, start_2, ...: Start position of the extraction interval for each object.  
end_1, end_2, ...: End position of the extraction interval for each object.  
row_1, row_2, ...: Row number of the MOS_SCIENCE_REDUCED image containing the extracted object spectrum. Image rows are counted from bottom, starting from 0.

## Table columns
0. row  -- row of this table
1. slit_id  -- Identification of object/slit from ADP file
2. xtop [pixel]  -- pixel coordinates of slit on UNMAPPED_SCIENCE image
3. ytop [pixel]
4. xbottom [pixel]
5. ybottom [pixel]
6. xwidth [mm]  -- slit width and length in mm on mask
7. ywidth [mm]
8. curved
9. position [pixel]  -- first row of spectrum in MOS_SCIENCE_EXTRACTED image
0. length [pixel]  -- number of rows containing the spectrum
1. object_1  -- central pixel coordinates of object 1 within slit
2. start_1 [pixel]  -- start pixel of extraction region
3. end_1 [pixel] -- end pixel of extraction region
4. row_1 [pixel] -- row number of object 1 in SCIENCE_REDUCED image
5. object_2
6. start_2 [pixel]
7. end_2 [pixel]
8. row_2 [pixel]

## Simpler words
The `slit_id` comes from the ADP file of the respective quadrant. Also in the
headers of the science frames the slit_id can be found under the keywords
`HIERARCH ESO INS SLIT1 ID = ...`, etc. There also the RA,DEC coordinates of
your catalog targets are given.  

The columns `xtop`, `ytop`, `xbottom`, `ybottom`, `xwidth`, `ywidth` and
`curved` describe the positions and shape of the slits in the unmapped,
original science frames (with category MOS_UNMAPPED_SCIENCE). They are
ordered with increasing (spatial) x position (y-direction is wavelength in
this case).  

The rectified, wavelength calibrated frames (category MOS_SCIENCE_EXTRACTED)
order the spectra from top to bottom, i.e. the x-axis is the wavelength axis
now. The columns 'position' and 'length' refer to the y (now spatial) position
of the extracted slits for the individual objects. In sloppy words, the frame
was rotated clockwise by 90 degrees.  

Then, finally, the extracted 1-dimensional spectra are ordered in rows from
bottom to top in the image MOS_SCIENCE_REDUCED. The order is according
to the appearance of objects in the slits from bottom to top in the image
MOS_SCIENCE_EXTRACTED, independent of how many objects there were detected
per slit.  

The columns `object_1`, `start_1` and `end_1` describe the y-positions of the
first extraction/object in each slit in the MOS_SCIENCE_EXTRACTED image,
whereas the column `row_1` defines the row of the extracted 1D spectrum in the
MOS_SCIENCE_REDUCED image.  

If more than one object was extracted in one slit, further columns are added,
i.e. `object_2`, `start_2`, `end_2` and `row_2`, which describe the position
of the 2nd object in the MOS_SCIENCE_EXTRACTED and the corresponding row in
the MOS_SCIENCE_REDUCED images.

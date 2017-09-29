The output from Reflex can be complicated, so here is an attempt to clarify any ambiguities.

#From the manual
Sect. 4.4:
:  object_sci_table.fits: slit positions on the CCD, on the mapped images, and positions of the detected objects within the slits.

Sect. 6.14.2:
:  MOS_SCIENCE_REDUCED: image with extracted objects spectra. This image has the same x size of the image with the extracted slit spectra, MOS_SCIENCE_EXTRACTED, and as many rows as the detected and extracted object spectra. Extracted spectra are written to the image rows listed in the OBJECT_SCI_TABLE product.

   OBJECT_SCI_TABLE: This table is an expansion of the input MOS_SLIT_LOCATION table (see page 113), where the positions and the extraction spatial intervals of the detected objects are also included. This table is produced only if any kind of sky subtraction is requested, otherwise no object detection or extraction is attempted. The object table columns are the following:

   slit_id: Slit identification number.
   xtop: x CCD position of central wavelength from left end of slit.
   ytop: y CCD position of central wavelength from left end of slit.
   xbottom: x CCD position of central wavelength from right end of slit.
   ybottom: y CCD position of central wavelength from right end of slit.
   position: First row of the rectified images (such as MOS_SCIENCE_EXTRACTED)
   containing the rectified slit spectrum. Image rows are counted from bottom,
   starting from 0.
   length: Number of rows in rectified images including the slit spectrum.
   object_1, object_2, ...: Detected objects positions in the rectified images.
   start_1, start_2, ...: Start position of the extraction interval for each
     object.
   end_1, end_2, ...: End position of the extraction interval for each object.
   row_1, row_2, ...: Row number of the MOS_SCIENCE_REDUCED image containing
     the extracted object spectrum. Image rows are counted from bottom, starting
     from 0.

    0) row  -- row of this table
    1) slit_id  -- Identification of object/slit from ADP file
    2) xtop [pixel]  -- pixel coordinates of slit on UNMAPPED_SCIENCE image
    3) ytop [pixel]
    4) xbottom [pixel]
    5) ybottom [pixel]
    6) xwidth [mm]  -- slit width and length in mm on mask
    7) ywidth [mm]
    8) curved
    9) position [pixel]  -- first row of spectrum in MOS_SCIENCE_EXTRACTED image
   10) length [pixel]  -- number of rows containing the spectrum
   11) object_1  -- central pixel coordinates of object 1 within slit
   12) start_1 [pixel]  -- start pixel of extraction region
   13) end_1 [pixel] -- end pixel of extraction region
   14) row_1 [pixel] -- row number of object 1 in SCIENCE_REDUCED image
   15) object_2
   16) start_2 [pixel]
   17) end_2 [pixel]
   18) row_2 [pixel]

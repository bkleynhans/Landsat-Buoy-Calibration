# Landsat Buoy Calibration
This branch is a variation on the original program that only calculated Top of Atmosphere Radiance using NOAA buoy data.

It adds functionality to the original program by adding both a GUI as well as additional algorithms.  The program has also been largely rewritten to implement Object Oriented Design principles in many areas.  Some of the original modules used (especially those in the buoycalib directory) have not been refactored due to the ad-hoc way in which they were originally implemented.  The process of refractoring all these files would be an extensive one and is planned for a future release since it would require a rewrite of most of the original science modules.

The current version of the program:

<ol>
    <li>Calculates and compares the radiance of a thermal LANDSAT scene to the "ground truth" radiance as measured by a NOAA buoy using the Single Channel process. Based on work in theses by Frank Padula and Monica Cook at RIT (Rochester Institute of Technology).</li>
    <li>Calculates Top of Atmosphere radiance using user-entered parameters and LANDSAT scenes using the Single Channel proces. Based on work in theses by Frank Padula and Monica Cook at RIT (Rochester Institute of Technology).</li>
    <li>Calculates Land Surface Temperature using user-entered parameters and LANDSAT scenes  using the Split Window process.  Based on research currently in progress by Aaron Gerace at RIT (Rochester Institute of Technology).</li>
</ol>

Frank Pedulas Thesis: <a href="https://www.cis.rit.edu/~cnspci/references/theses/masters/padula2008.pdf">Historic Thermal Calibration of Landsat 5 TM through an Improved Physics Based Approach</a>

There are two help documents included in this repository.

<ol>
    <li>User Manual</li>
    <li>Design Document</li>
</ol>

# Installation
It is highly recommended that the software is run on one of the RIT CIS linux servers. There are a number of prerequisites required, some of which are challenging to install and others (like <a href="http://modtran.spectral.com/modtran_order">MODTRAN</a>) are quite expensive for individual use.

To download a copy of the program, enter the following command while in your home directory in a ssh session on the server.

For detailed instructions on how to launch and use the program, please refer to the user manual.

```
git clone https://github.com/bkleynhans/Landsat-Buoy-Calibration.git
```

This will download a copy of the program in a directory named 'Landsat-Buoy-Calibration' in your home directory on the server.

# User Manual
The User Manual is a basic manual containing all the data required by users to use the program.  There is no information pertaining to the design in this document.  For design information please refer to the design document located in the same directory.  No Python knowledge is required for program usage.

`UserManual.md` : https://github.com/bkleynhans/Landsat-Buoy-Calibration/blob/cis-tarca_v2.0/UserManual.md

# Design Document 
The Design Document is a fully detailed document containing all the information pertaining to the design and implementation of modules.  Any developer who wants to make changes or amendments to the program should reference the design document before making major changes.  A Basic to Intermediate level of Object Oriented Design and Python programming is suggested for anyone who wants to make changes to the program.

This program was designed to be used on the RIT CIS linux servers as multiple programs and modules are included in the processing of data.

`DesignDocument.md` : https://github.com/bkleynhans/Landsat-Buoy-Calibration/blob/cis-tarca_v2.0/DesignDocument.md

`cis-tarca_design_UML.pdf` : https://github.com/bkleynhans/Landsat-Buoy-Calibration/blob/cis-tarca_v2.0/cis-tarca_design_UML.pdf

`cis-tarca_activity_diagram.pdf`: https://github.com/bkleynhans/Landsat-Buoy-Calibration/blob/cis-tarca_v2.0/cis-tarca_activity_diagram.pdf
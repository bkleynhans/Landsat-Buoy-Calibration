# Landsat Buoy Calibration
This branch is a variation on the original program that only calculated Top of Atmosphere Radiance using NOAA buoy data.

This branch adds functionality to the original program by implementing both a GUI as well as additional algorithms.  The program has also been largely rewritten to implement Object Oriented Design principles in many areas.  Some of the original modules used (especially those in the buoycalib directory) have not been refactored due to the ad-hoc way in which they were originally implemented since it would require a rewrite of most of the original science modules.  This option will be investigated in future versions.

The current version of the program:

1) Calculates and compares the radiance of a thermal LANDSAT scene to the "ground truth"
radiance as measured by a NOAA buoy using the Single Channel process. Based on work in theses by Frank Padula and Monica Cook at RIT (Rochester Institute of Technology).  
2) Calculates Top of Atmosphere radiance using user-entered parameters and LANDSAT scenes using the Single Channel proces. Based on work in theses by Frank Padula and Monica Cook at RIT (Rochester Institute of Technology).
3) Calculates Land Surface Temperature using user-entered parameters and LANDSAT scenes  using the Split Window process.  Based on research currently in progress by Aaron Gerace at RIT (Rochester Institute of Technology).

There are two documents included in this repository.

# User Manual
The User Manual is a basic manual containing all the data required by users to use the program.  There is no information pertaining to the design in this document.  For design information please refer to the design document located in the same directory.  No Python knowledge is required for program usage.

UserManual.md : https://github.com/bkleynhans/Landsat-Buoy-Calibration/blob/cis-tarca_v2.0/UserManual.md

# Design Document
The Design Document is a fully detailed document containing all the information pertaining to the design and implementation of modules.  Any developer who wants to make changes or amendments to the program should reference the design document before making major changes.  A Basic to Intermediate level of Object Oriented Design and Python programming is suggested for anyone who wants to make changes to the program.

This program was designed to be used on the RIT CIS linux servers as multiple programs and modules are included in the processing of data.

DesignDocument.md : https://github.com/bkleynhans/Landsat-Buoy-Calibration/blob/cis-tarca_v2.0/DesignDocument.md


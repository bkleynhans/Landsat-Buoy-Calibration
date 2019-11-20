# Landsat Buoy Calibration - Technical Design Document
## Project Summary
This is a Python 3.7 based program with a Tcl/Tk GUI.  The program uses an extensive set of libraries, all of which are listed in the requirements.txt file located in the root of the project.  The program has a detailed UML document (WIP), also located in the root of this project.

This program consists of two main sets of components.

## First Component
The original code that was created as part of a capstone project by Nathan Dileas.  This code was created as a set of scripts that could be run from the command line.  The original version of the program is available at the provided locations.

* [Original Code](https://github.com/natedileas/Landsat-Buoy-Calibration).
* [Original Readme](https://github.com/natedileas/Landsat-Buoy-Calibration/blob/master/README.md).

## Second Component
The second component was designed and implemented using OOP concepts.  It is both an enhancement as well an expansion of the original version of the program.  The current version of the program runs as a full program with both a text-based as well as GUI-based interface.  Many of the original modules were also rewritten using OOP principles.

Most of the modules located within the ./buoycalib directory were carried over from the original project.  Many of the modules were modified to improve or correct calculations, however there was insufficient time to rewrite all of the modules using OOP principles.  All the modules within the ./modules directory are part of the new version of the program.

### Operational base classes
All the operational base classes (not GUI base classes) are located in ./modules/core/ and ./modules/core/landsat/.  The file ./modules/core/model.py located in ./modules/core/ is the entry point to the actual processing that happens in the program.  Both the GUI as well as the text-based interface utilizes this file to perform the required operations.  The file ./modules/core/menu.py is the text-based menu interface for the program.

### GUI classes
The entire GUI including all of its base and derived classes is located in ./modules/gui/.  All the processing done within the GUI actually happens within the operational base classes.  The base classes get triggered from the GUI classes.

### DB classes
One of the elements of the program which is still in progress, is the possibility of uploading data to a SQL database.  The modules in ./modules/db/ are a fully operational and functional, they just haven't been implemented within the production system.

### STP classes (Surface Temperature Products)
After the original project was completed in both the text-based and gui-based implementations, a request was made to add additional algorithms to the program.  The ./modules/stp/ directory was created as a container for the new, and all future STP algorithms.  Currently the STP only contains the SW(Split Window) algorithm while the TOA (Top of Atmosphere) algorithm is still embedded in the original program.  Future product enhancement will include the move of the TOA product to the STP directory

> Each of the elements of the program mentioned above, are described in more detail below.  Please refer to the Table of Contents to jump to your required section of interest.

# Table of Contents

<!--ts-->
* [Table of Contents](#table-of-contents)
* [Project Overview](#project-overview)
* [Scripts and Classes](#scripts-and-classes)
  * [Original Code](#original-code-(classes-and-scripts))
  * [New Code](#new-code)
    * [Classes](#classes)
    * [Scripts](#scripts)
      * [display_image.py](#display_image.py)
<!--te-->

# Project Overview
The software is used in the calibration of NASA/USGS Landsat satellite thermal infrared image data.  The calibration of the instrument involves converting the raw signal output from each pixel into an accurate radiance (energy or Watts) for the pixel so that the measured energy can in turn be related the temperature of the Earth’s surface.  As the satellite sensors age on-orbit, the calibration is constantly checked to ensure that it still meets accuracy requirements.  This process involves comparing the output of the sensor to a known Earth temperature (“ground reference”) and adjusting the sensor’s calibration so that the output matches the ground reference data.

The calibration procedure involves the manual assembly of Landsat image data, atmospheric profile data, and ground temperature data (water temperatures from buoys).  Physics modeling software is then used to propagate the ground reference measurement through the atmosphere and predict the radiance that the sensor should see (known as “top-of-atmosphere”, TOA, radiance).  Any discrepancy between the modeled TOA radiance and the measured image radiance from the sensor is reported to NASA and USGS so the calibration may be adjusted.

This software streamlines the process.  The user simply specifies an image (Earth scene) of interest and the software will automatically:

- search the NOAA database for known ground reference data (buoys) within the geographic confines of the scene,
- import atmospheric pressure, temperature, and humidity profile data from the NASA database and execute the US Air Force atmosphere propagation model (known as MODTRAN) to generate transmission values through the atmosphere,
- calculate the TOA radiance from the bulk water measurement below the water surface to the skin temperature of the water and finally through the atmosphere,
- download and ingest the Landsat scene image from USGS, determine the pixel containing the ground reference measurement, and compare it to the calculated TOA radiance to derive the delta between the two.

The software also has a “bulk process” feature that allows one to specify a list of desired Landsat scenes to run in series.  This software also allows one to manually input a known ground temperature (instead of importing a buoy temperature) to calculate the TOA radiance.  This allows one to compare the Landsat calibration to ground targets other than the traditional water target.

The software also includes a reverse calibration process.  Instead of propagating a known ground temperature to the top of atmosphere, the code can start with only the Landsat image data and calculate the ground temperature through an already established algorithm.  This algorithm will eventually be implemented into the Landsat ground system to generate a standard Earth temperature product for users.  Having this algorithm implemented in the software allows one to quickly test its accuracy on many different scenes and ground types so one can report to NASA and USGS on the effectiveness of the algorithm before it goes operational.

This software is used on an almost daily basis to help us generate the datasets that are used to provide NASA and USGS with quality assessments of the image products from their satellite sensors.

# Scripts and Classes
## Original Code (classes and scripts)
The `./buoycalib/` and `./tools/` directories contain combinations of classes and scripts and were copied from the original version of the program that was created by Nate Dileas.  Please refer to the [first component](#first-component) for details pertaining to these directories.

Some repairs were made to the code, however these are documented in detail (with references) in the associated files.

## New Code
### Classes
All classes pertaining to the current version of the program are located in `./modules/`.  These are explained in detail below.



### Scripts
Some utility scripts were created in `./tools/` and are explained in detail below.

#### display_image.py


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
* [Project Background](#project-background)
<!--te-->

# Project Background

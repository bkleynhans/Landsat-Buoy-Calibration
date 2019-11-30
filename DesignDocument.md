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

#### `cis-tarca.py` of type: script
The file contains a she-bang and is the expected launch file for the project and accepts a single parameter  *-i* which is used to specify the interface preferred and as the following options

- **`cis-tarca.py` *`-i terminal`*** which launches the non-Gui version, and
- **`cis-tarca.py` *`-i gui`*** which launches the Gui version of the program.

If no option is specified, the system will determine whether the X-Window system is supported and then start either the Gui or the terminal based on the support of the session.

Once the program launch has commenced, the system executes in the following order.

1. Determine the relative path to the project and update the path variables for the specified user accordingly.
2. Determines whether the online data sources (specified in `./buoycalib/settings.py`) are available.  If they are not, the program performs a graceful exit and informs the user which source is unavailable.
3. Depending on the parameter passed and the X-Window capability of the system, the program launches either the text-based menu (`./modules/core/menu.py`) or the Tcl/Tk (Tkinter) based Gui (`./modules/gui/tarca_gui.py`).

#### `menu.py` of type: script
_This is the first file I ever created in python and it has expanded extensively.  There are some repetitions in the menu management that will be cleaned up in future versions._

The menu is opened providing the user with five options.  Each of these options instantiates an object of the Model base class, which in turn creates an instance of one of the derived classes based on passed parameters..  The model class and derived classes are explained in the `model.py` section.

Each of the menu options have multiple sub-options of which the most unconventional ones are explained blow.  For more information about each option please refer to the code-based comments in the relevant files.

##### 1. Single Scene - Single Channel using Buoys (`model_single_sc_buoy(project_root)`)

1. Ask the user if they want to see each satellite image after the data has been processed.
2. Ask for a Scene ID for the image to analyze.
3. Test the Scene ID to ensure it is valid (for landsat) using regular expressions in the function: `is_valid_id(scene)`.  The regex is explained in detail in the function.

Create an instance of the Model class with the following command.  Details are explained in the `model.py` section.

`Model('menu', 'single', 'sc', 'buoy', sceneId, 'merra', display_images, project_root, False, None)`

##### 2. Single Scene - Single Channel using Supplied Surface Temp (`model_single_sc_toa(project_root)`)

1. Ask the user to provide a Scene ID for the image to analyze.
2. Test the Scene ID to ensure it is valid (for landsat) using regular expressions in the function: `is_valid_id(scene)`.  The regex is explained in detail in the function.
3. Ask for a skin temperature and validate with `is_valid_temp(skin_temp)`.
4. Ask for a latitude and validate with `is_valid_latitude(lat)`.
5. Ask for a longitude and validate with `is_valid_longitude(lon)`.
6. Ask for a band 10 emissivity value and validate with `is_valid_emissivity(emis_b10)`.
7. Ask for a band 11 emissivity value and validate with `is_valid_emissivity(emis_b11)`.

Create an instance of the Model class with the following command.  Details are explained in the `model.py` section.

`Model('menu', 'single', 'sc', 'toa', sceneId, 'merra', display_images, project_root, False, partial_data)`

##### 3. Single Scene - Split Window using Supplied values (`model_single_sw_lst(project_root)`)

1. Ask the user to provide a Scene ID for the image to analyze.
2. Test the Scene ID to ensure it is valid (for landsat) using regular expressions in the function: `is_valid_id(scene)`.  The regex is explained in detail in the function.
3. Ask for a skin temperature and validate with `is_valid_temp(skin_temp)`.
4. Ask for a latitude and validate with `is_valid_latitude(lat)`.
5. Ask for a longitude and validate with `is_valid_longitude(lon)`.
6. Ask for a band 10 emissivity value and validate with `is_valid_emissivity(emis_b10)`.
7. Ask for a band 11 emissivity value and validate with `is_valid_emissivity(emis_b11)`.
8. Ask for a band 10 gain and bias. These can be any values and cannot be validated.
9. Ask for a band 11 gain and bias. These can be any values and cannot be validated.

Create an instance of the Model class with the following command.  Details are explained in the `model.py` section.

`Model('menu', 'single', 'sw', 'lst', sceneId, 'merra', display_images, project_root, False, partial_data)`

##### 5. Batch Scenes - Single Channel using Buoys (`model_batch_sc_buoy(project_root)`)

1. Import the `./tools/test_paths.py` module which is used to test the availability of files and directories.
2. Ask the user if they want to see the images after they are processed.
3. Ask for a batch file filename. (batch files are read from `./input/batches/`).
4. Test if the specified batch file exists.
5. Read the text file and test each scene id with `is_valid_id(scene)` which validates the Scene ID with regular expressions.  The regex is explained in detail in the function.
6. If an error is found, the user receives output specifying which Scene ID in which line of the file needs to be reviewed.

Create an instance of the Model class with the following command.  Details are explained in the `model.py` section.

`Model('menu', 'batch', 'sc', 'buoy', batchFile, 'merra', display_images, project_root, False, None)`

##### X. Exit
The exit option takes the user back to the terminal

##### _There is menu option D which creates SQL database tables on a remove server for data storage.  This feature is however still in development and is commented out even though the calling functions are present inside this file._

#### `model.py` of type: class
The `Model` class is the point-of-entry class for all processing in the program.  Both the terminal and the Gui create an instance of this class with the relevant parameters, which in turn fires any other object creation that is required.  All algorithmic processing classes are instantiated from this class.

##### Class Constructor
`def __init__(self, caller, qty, algorithm, process, source, atmo_source, display_image, project_root, verbose, partial_data=None, status_log=None, output_log=None):`

###### `__init__`
Default initialization method for constructor
###### `self`
This object (`self` in Python has the same significance as `this` in other languages)
###### `caller`
Is `Model` being called from the `menu` or the `gui`
###### `qty`
Is this a `single` or a `batch` process
###### `algorithm`
Are we performing a _single channel (`sc`)_ or a _split window (`sw`)_ operation?  These are the only two algorithms implemented currently, but there are plans for additional algorithms.
###### `process`
Is this a `buoy`, **_Top of Atmosphere (`toa`)_** or **_Land Surface Temperature (`lst`)_** process?
###### `source`
Depending on whether we are performing a single or a batch process, the **_source_** would be either a **_scene id_** or a **_batch filename_**.
###### `atmo_source`
Are we getting our atmospheric data from `merra` or `narr`
###### `display_image`
Are we going to display the image to the user after processing `true` or `false`
###### `project_root`
This is the absolute path to the root of the project.  It is determined in `cis-tarca.py` and brought forward.  It is found with:

`PROJECT_ROOT = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))`
###### `verbose`
Provide additional terminal-based output `true` or `false`.  The default is `false`.
###### `partial_data`
This is a dictionary used to transfer the information gathered during the _menu phase of many quesitons_ to the rest of the program.  It is not required for the _single channel_ operation and therefore has a default value of `none`.
###### `status_log`
This is not used by the terminal-based program and has default value of `none`.  It is used by the Gui to provide status update information back to the user.
###### `output_log`
This is not used by the terminal-based program and has default value of `none`.  It is used by the Gui to provide output information back to the user.

During the constructor phase the variables are assigned to the object into a dictionary called `args` which is passed to the subsections of the program.  After the variables have been created:

1. A logger instance is created (see `./tools/process_logger.py` for details), and
2. The passed-in arguments are processed.


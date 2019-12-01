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
    * [Scripts](#scripts)
    * [Classes](#classes)
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
### Scripts
The following files are detailed in this section:

- `cis-tarca.py`
- `menu.py`

Some utility scripts were created in `./tools/` and are explained in detail below.

- `test_paths.py`

#### `cis-tarca.py`
The file contains a she-bang and is the expected launch file for the project and accepts a single parameter  *-i* which is used to specify the interface preferred and as the following options

- **`cis-tarca.py` *`-i terminal`*** which launches the non-Gui version, and
- **`cis-tarca.py` *`-i gui`*** which launches the Gui version of the program.

If no option is specified, the system will determine whether the X-Window system is supported and then start either the Gui or the terminal based on the support of the session.

Once the program launch has commenced, the system executes in the following order.

1. Determine the relative path to the project and update the path variables for the specified user accordingly.
2. Determines whether the online data sources (specified in `./buoycalib/settings.py`) are available.  If they are not, the program performs a graceful exit and informs the user which source is unavailable.
3. Depending on the parameter passed and the X-Window capability of the system, the program launches either the text-based menu (`./modules/core/menu.py`) or the Tcl/Tk (Tkinter) based Gui (`./modules/gui/tarca_gui.py`).

#### `menu.py`
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

#### `test_paths.py`
This script tests whether _directories_, _files_ or _servers_ are available and returns either `true` or `false`.  It can be called from within another function, or from the command line.  For application options, please execute `python test_paths.py --help`.  The file contains detailed comments for further information.

### Classes
All classes pertaining to the current version of the program are located in `./modules/`.  These are explained in detail below.

The following files are detailed in this section:

- `model.py`
- `landsat_base.py`
- `landsat_single_sc_buoy.py`
- `landsat_single_sc_toa.py`
- `landsat_single_sw_lst.py`
- `landsat_batch_sc_buoy.py`
- `targa_gui.py`

Some utility classes were created in `./tools/` and are explained in detail below.

- `display_image.py`
- `process_logger.py`
- `spinner.py`

#### `model.py`
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
Are we performing a **single channel** (`sc`) or a **split window** (`sw`) operation?  These are the only two algorithms implemented currently, but there are plans for additional algorithms.
###### `process`
Is this a `buoy`, **Top of Atmosphere** (`toa`) or **Land Surface Temperature** (`lst`) process.
###### `source`
Depending on whether we are performing a single or a batch process, the **source** would be either a **scene id** or a **batch filename**.
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

1. A logger instance is created (see `process_logger.py` for details), and
2. The passed-in arguments are processed.

##### Processing input arguments (`process_arguments(self)`)
The `process_arguments(self)` method analyzes the input parameters and instantiates the appropriate algorithmic class.

#### `landsat_base.py`
The **Landsat_Base** class is the base class for:
- `landsat_single_sc_buoy.py`
- `landsat_single_sc_toa.py`, and
- `landsat_single_sw_lst.py`

**Landsat_Base** has many methods but they are all either initiated from a derived class, or form part of a processing change, which would have been launched from a derived class.  The file is well documented, please refer to the actual code for detailed information.

#### `landsat_single_sc_buoy` launched with (`Landsat_Single_Sc_Buoy(self.args)`)
**Landsat_Single_Sc_Buoy** is the base class for:
- `landsat_batch_sc_buoy.py`

**Landsat_Single_Sc_Buoy** executes as follows:

1. Call the base class constructor: `super(Landsat_Single_Sc_Buoy, self).__init__(args)`.  The base class is `./modules/core/landsat/landsat_base.py`.  Please refer to `landsat_base.py` for details.
2. Set class variables in `landsat_base.py`.
3. Download image file `download_image()` --> base class method.
4. Analyze the image `analyze_image()` --> local method.
5. Print the report headings to terminal `print_report_headings()` --> local method.
6. Process scene data `process_scene()` --> local method.
7. Finalize the output `finalize()` --> base class method.
8. Return to caller (`menu` or `tarca_gui`)

#### `landsat_single_sc_toa.py` launched with (`Landsat_Single_Sc_Toa(self.args)`)

**Landsat_Single_Sc_Toa** executes as follows:

1. Call the base class constructor: `super(Landsat_Single_Sc_Toa, self).__init__(args)`.  The base class is `./modules/core/landsat/landsat_base.py`.  Please refer to `landsat_base.py` for details.
2. Set class variables in `landsat_base.py`.
3. Download image file `download_image()` --> base class method.
4. Calculate atmospheric data `get_atmosphere()` --> local method.
5. Print the report headings to terminal `print_report_headings()` --> local method.
6. Print the output to the screen and save the output file `print_and_save_output()` --> local method.
7. Finalize the output `finalize()` --> base class method.
8. Return to caller (`menu` or `tarca_gui`)

#### `landsat_single_sw_lst.py` launched with (`Landsat_Single_Sw_Lst(self.args)`)

**Landsat_Single_Sw_Lst** executes as follows:

1. Call the base class constructor: `super(Landsat_Single_Sw_Lst, self).__init__(args)`.  The base class is `./modules/core/landsat/landsat_base.py`.  Please refer to `landsat_base.py` for details.
2. Set class variables in `landsat_base.py`.
3. Download image file `download_image()` --> base class method.
4. Get Top of Atmosphere Radiance from image data (**ltoa**) `get_image_ltoa()` --> local method.
5.  Add user provided gain and bias values `add_gain_bias()` --> local method.
6.  Perform _split window_ calculation `claculate_split_window()` --> local method.
7.  Print the report headings to terminal `print_report_headings()` --> local method.
8.  Print the output to the screen and save the output file `print_and_save_output()` --> local method.
9.  Finalize the output `finalize()` --> base class method.
10.  Return to caller (`menu` or `tarca_gui`)

#### `landsat_batch_sc_buoy.py` launched from within (`analyze_batch(self)`)

_You'll notice that the batch processing does not call the algorithm class directly.  This is because any leading or trailing whitespace, line feed or carriage returns could interfere with the batch process.  It also splits the _landsat_ and _modis_ scenes into seperate files since their processing would be different. Once the batch file data base been cleaned and separated the constructor is called: `Landsat_Batch_Sc_Buoy(self.args)` **PLEASE NOTE: modis processing has not yet been implemented**._

**Landsat_Batch_Sc_Buoy** executes as follows:

1. Call the base class constructor: `super(Landsat_Batch_Sc_Buoy, self).__init__(args)`.  The base class is `./modules/core/landsat/landsat_single_sc_buoy.py`.  Please refer to `landsat_single_sc_buoy.py` for details.
2. Set class variables in landsat_base.py`.
3. Loop through the provided list of scenes, and for each:
	1. Download image file `download_image()` --> base class method.
	2. Analyze the image `analyze_image()` --> base class method.
	3. Print the report headings to terminal `print_report_headings()` --> local method.
	4. Process scene data `process_scene()` --> local method.
	5. Finalize the output `finalize()` --> base class method.
	6. Return to caller (`menu` or `tarca_gui`)

#### `tarca_gui.py`
The `Tarca_Gui` class is the base class for the entire Gui.  As per Tcl/Tk (TkInter) guidelines, it is the base class from which all other graphical elements are instantiated.

The base class contains both a _frames_ and _windows_ dictionary, which is used to gain access to all of its direct descendents.

`Tarca_Gui` was designed using a _window_-->_frame_-->_notebook_-->_widget_ format.  Each new window is created within a _window_ object.  Thereafter you can have a _frame_ containing a _notebook_ containing a _frame_ containing a _notebook_ etc.  Widgets generally represent a button.

The base classes for the four main elements are located within `./gui/forms/base_classes` and are labelled accordingly:
- `gui_window.py`
- `gui_frame.py`
- `gui_label_frame.py`
- `gui_notebook.py`

Each of the base classes contain a dictionary for _frames_, _notebooks_ and _widgets_.  Whenever a new element is added as the child of another, the child is automatically added to the container within its parent, thereby building a hierarchy of dictionaries to allow easy access from any element to its child elements.

The error module has its own window and frame and is located in `./gui/forms/general/error_module`.  It is instantiated whenever the main application runs into a runtime error.

There is also a progress bar in the `./gui/forms/general` folder.  The progress bar is an animated progress bar that runs in its own thread.

The settings window has not been completed and is located in `./gui/forms/settings`.  The _window_, _frame_ and _notebook_ derived classes have been created, but they have not been fully implemented or linked to the settings file located in `./buoycalib/`.

The entire application (currently a single window with tabs) is located within `./gui/forms/main_window`.  The structure follow the stacking nature of implementation for Tcl/Tk Gui's.

#### `display_image.py`
This class is used specifically to display an image on the screen through the use of threading and `cv2.impshow`.  This implementation allows the user to display in image on the screen while the code continues to run in the background.

#### `process_logger.py`
The process logger creates logger output paths and then creates text files with log data.  It can both create a new file or append to an existing file.

#### `spinner.py`
The **spinner** class is used to provide the traditional linux _busy_ indicator (the spinning asterisk).  The spinner class runs using threading which allows the user to have the spinner running while the code continues to process in the background.
# Landsat Buoy Calibration
Calculates and compares the radiance of a thermal LANSAT scene to the "ground truth"
radiance as measured by a NOAA buoy. Based on work by Frank Padula and Monica Cook at RIT.  

If you want to use this code, you should have a basic knowledge of python and/or basic coding. No warranty. Use it on one of the RIT CIS linux servers for best results.

# Table of contents
=================

<!--ts-->
   * [Landsat Buoy Calibration](#landsat-buoy-calibration)
   * [Table of contents](#table-of-contents)
<!--te-->

## Current Version
Current version contains multiple enhancements of the Landsat and Buoy processing implementation and was done by Benjamin Kleynhans (bxk8027@g.rit.edu).  The MODIS implementation remains original and unchanged.  The enchancements are described in the sections below.

## Original Version
The original version of this software was developed on Fedora x64 by Nathan Dileas (nid4986@g.rit.edu).  His original work is available at the links provided below.  

Repository: https://github.com/natedileas/Landsat-Buoy-Calibration.  
README: https://github.com/natedileas/Landsat-Buoy-Calibration/blob/master/README.md  

Copyright RIT 2015-2018

## Overview:
This code essentially has two funtions: calculating the radiance from the landsat image 
provided, and calculating the corresponding ground truth radiance from outside data,
atmospheric (NARR or MERRA-2), NOAA buoy data, and MODTRAN. If atmospheric
data or landsat images need to be downloaded, it will take between 5-7 minutes
for NARR, and 2-3 for MERRA. 

### Enhancements

-  The program is now used by launching a menu
-  Previously, if a data source wasn't available the program would fail without providing adequate information.  The system now checks data sources during launch and informs the user if a source is not available while gracefully returning them to the terminal prompt.
-  A menu has been implemented to replace the original command line interface
- The original software could not run without a X-Window enabled terminal.  This service has now been integrated and will run regardles of X-Window availability while informing the user if the system does not have X-Window support.  It can also be enabled or disabled during runtime by the user if the service is available.
- No more issues related to path variables, this is now calculated automatically.
- Batch processing which was originally implemented but problematic has been improved and errors resolved.
- The output files have been enhanced to provide additional information.  Previously if information could not be calculated a buoy was omitted from the output file.  The current version adds an entry into the file to indicate why the buoy was omitted.
- Problems relating to landsat scenes prior to 2017 as described in notes have been resolved (any landsat 8 ID should work).  Landsat 8 data are only available from 2014.
- The system tests both Landsat Product Identifiers as well as SceneID's during entry to ensure a valid ID is supplied.
- Whenever a batch is processed, a graph is generated which displayes the difference between landsat and buoy data over time.
- Input and output directories have been implemented as follows:

#### Input (Batches)
  input/batches
  
#### Output
  output/single/  - a comma delimited text output file when running individual scenes  
  output/processed_images/  - all processed images for single and batch runs  
  output/batches/  - all information relating to batch runs  
  output/batches/data/  - a comma delimed text output file per batch containing the data for all scenes in the batch file  
  output/batches/graphs/  - all graphs (one per batch) dsplaying the variance with error between landsat and buoy data  

- Downloaded data is no longer stored indefinately by default.  At the top of the forward_data.py file there is a contstant named CLEAN_FOLDER_ON_COMPLETION.
```
# Constants for use in directory cleanup
CLEAN_FOLDER_ON_COMPLETION = True
```
 When this value is True, the downloaded_data folder is cleared after each SceneID is processed.  If the value is set to False, the data is kept until it is manually deleted OR the value is set to True.  
 
!!! WHEN THE VALUE IS SET TO TRUE, EVERYTHING IN THE downloaded_data FOLDER WILL BE DELETED, REGARDLESS OF WHICH BATCH IT BELONGS TO!!!


### Installation
It is highly recommended that the software is run on one of the RIT CIS linux servers.  There are a number of prerequisites required, some of which are challenging to install.  Additional details relating to installation of the software on any other platform than the RIT CIS servers can be found in the original installation file provided by the original developer at:  

INSTALL.txt : https://github.com/natedileas/Landsat-Buoy-Calibration/blob/master/INSTALL.txt  

If however you are planning to use the system on one of the RIT CIS servers, please follow these simple instructions:  
  
-  From the terminal on a RIT-CIS server, go to your home directory
```
cd ~
```
-  Create a local clone of the repository
```
git clone https://github.com/bkleynhans/Landsat-Buoy-Calibration.git
```
- The program is now installed and you can continue to the next section.

### Launching the program
-  Change into the Landsat-Buoy-Calibration directory
```
cd ~/Landsat-Buoy-Calibration
```
-  Launch the program
```
./menu
```
-  The system will ensure all required data sources are available
```
 Please be patient while we test if the required data sources are available

     --> All data sources are accounted for <--

```
-  After which you will be presented with a menu
```
 ***************************************************
 *                                                 *
 *           Landsat Buoy Calibration              *
 *                                                 *
 ***************************************************
 *                                                 *
 * Please select from one of the following options *
 *                                                 *
 *                                                 *
 *              ***  SINGLE JOB  ***               *
 *                                                 *
 * 1. Forward model calculation (MERRA2 / MODIS)   *
 *                                                 *
 *                                                 *
 *              ***  BATCH JOBS  ***               *
 *                                                 *
 * 5. Forward model calculation (MERRA2)           *
 *                                                 *
 *                                                 *
 * X. Exit                                         *
 *                                                 *
 ***************************************************

  Selection : 
```

### Running a single scene
-  Launch the program as indicated in the "Launching the program" section.  
-  Enter the number 1 and press enter
```
  Selection : 1
```
-  Depending on whether your terminal has X-Window support, you will receive one of two options to choose from, please follow the appropriate instructions  
-- Without X-Window support
```
Your terminal session does not support the display of images.  If you want to see processed images please launch the program from a terminal that has X display support.

 Please enter the Scene ID to continue or 'X' to exit : 
```
-  Now enter the sceneID at the prompt and press enter, or enter the letter 'x' (without the apostrophes) to be returned to the menu  

-- With X-Window support
```
Do you want to display the image after it has been processed? (Y/N): y
```
-  If your terminal has X-Window support, you can choose either 'y' for yes, or 'n' for no (without the apostaphes).  If you choose yes, each image will be displayed while it is being processed.  If you choose no, no images will be dispayed.
```
 Please enter the Scene ID to continue or 'X' to exit : 

```
-  Now enter the sceneID at the prompt and press enter, or enter the letter 'x' (without the apostrophes) to be returned to the menu

#### Test Scenes
The system supports both Scene ID's as well as Landsat Product Identifiers.  These two are both valid ID's than can be used.
-  Scene ID  : LC80130322017332LGN00
-  Landsat Product Identifier  : LC08_L1TP_017030_20160614_20170220_01_T1    

These ID's are checked before processing to ensure they are valid.

### Running a batch job
Batch processing has been enhanced in this revision to be very simple.  

-  Copy a file containing Product ID's or Landsat Product Identifiers, with one entry per line into the /input/batches directory.  These can be files containing either one of the formats, or a mixture of the two formats.  The system determines the ID and processes it accordingly.  
-  Launch the program as indicated in the "Launching the program" section.  
-  When presented with the menu, press 5 and enter  
```
  Selection : 5
```
-  Depending on whether your terminal has X-Window support, you will receive one of two options to choose from, please follow the appropriate instructions  
-- Without X-Window support
```
Your terminal session does not support the display of images.  If you want to see processed images please launch the program from a terminal that has X display support.

 Please enter the name of the batch file or 'X' to exit : 
```
-  Now enter the name of the batch file, including the file extension and press enter.
```
 Please enter the name of the batch file or 'X' to exit : test.batch
```

-- With X-Window support
```
Do you want to display the image after it has been processed? (Y/N): y
```
-  If your terminal has X-Window support, you can choose either 'y' for yes, or 'n' for no (without the apostaphes).  If you choose yes, each image will be displayed while it is being processed.  If you choose no, no images will be dispayed.
```
 Please enter the name of the batch file or 'X' to exit : 

```
-  Now enter the name of the batch file, including the file extension and press enter.
```
 Please enter the name of the batch file or 'X' to exit : test.batch
```

#### Test Batches
A number of batch files are included in the repository and can be used as required.  

### Output
Output for both the single as well as batch jobs are stored in the 'output' directory within the 'Landsat-Buoy-Calibration' directory.

-  Single data output locations are:  
  Data - /output/single  
  Images - /output/processed_images  
    
-  Batch data output locations are:  
  Data - /output/batches/data  
  Images - /output/processed_images  
  Graphs - /output/batches/graphs  

### Notes



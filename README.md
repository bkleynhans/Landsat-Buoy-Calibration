# Landsat Buoy Calibration
Calculates and compares the radiance of a thermal LANSAT scene to the "ground truth"
radiance as measured by a NOAA buoy. Based on work by Frank Padula and Monica Cook at RIT.

If you want to use this code, you should have a basic knowledge of python and/or basic coding. No warranty. Use it on one of the RIT CIS linux servers for best results.

## Current Version
Current version contains multiple enhancements of the Landsat and Buoy processing implementation and was done by Benjamin Kleynhans (bxk8027@g.rit.edu).  The MODIS implementation remains original and unchanged.  The enchancements are described in the sections below.

## Original Version
The original version of this software was developed on Fedora x64 by Nathan Dileas (nid4986@g.rit.edu).  His original work is available at the links provided below.

Repository: https://github.com/natedileas/Landsat-Buoy-Calibration.  
README: https://github.com/natedileas/Landsat-Buoy-Calibration/blob/master/README.md  
Copyright RIT 2015-2018

## OVERVIEW:
This code essentially has two funtions: calculating the radiance from the landsat image 
provided, and calculating the corresponding ground truth radiance from outside data,
atmospheric (NARR or MERRA-2), NOAA buoy data, and MODTRAN. If atmospheric
data or landsat images need to be downloaded, it will take between 5-7 minutes
for NARR, and 2-3 for MERRA. 

### Enhancements

-  The program is now used by launching a menu
```
$ ./menu
```

-  Previously, if a data source wasn't available the program would fail without providing adequate information.  The system now checks data sources during launch and informs the user if a source is not available while gracefully returning them to the terminal prompt.
```
 Please be patient while we test if the required data sources are available

     --> All data sources are accounted for <--
```

-  A menu has been implemented to replace the original command line interface:
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

- The original software could not run without a X-Window enabled terminal.  This service has now been integrated and will run regardles of X-Window availability while informing the user if the system does not have X-Window support.  It can also be enabled or disabled during runtime by the user if the service is available.

-- Without X-Window support
```
Your terminal session does not support the display of images.  If you want to see processed images please launch the program from a terminal that has X display support.

 Please enter the Scene ID to continue or 'X' to exit : 
```
-- With X-Window support
```
Do you want to display the image after it has been processed? (Y/N): y

 Please enter the Scene ID to continue or 'X' to exit : 
```
- No more issues related to path variables, this is now calculated automatically.
- Batch processing which was originally implemented but problematic has been improved and errors resolved.
- Problems relating to landsat scenes prior to 2017 as described in notes have been resolved (any landsat 8 ID should work).  Landsat 8 data are only available from 2014.
- Input and output directories have been implemented as follows:

#### Batch Input
  input/batches
  
#### Output
  output/single/  - a comma delimited text output file when running individual scenes
  output/processed_images/  - all processed images for single and batch runs
  output/batches/  - all information relating to batch runs
  output/batches/data/  - a comma delimed text output file per batch containing the data for all scenes in the batch file
  output/batches/graphs/  - all graphs (one per batch) dsplaying the variance with error between landsat and buoy data

### Installing
See INSTALL.txt

### Test Scenes
- landsat test scene `python forward_model.py LC08_L1TP_017030_20170703_20170715_01_T1 45012`
- modis test scene `python forward_model.py MOD021KM.A2011154.1650.006.2014224075807.hdf 45012`

### Notes
- all the downloaded data will be in a directory: buoy_calib/Landsat-Buoy-Calibration/downloaded_data/
- the settings and paths can be changed in: buoy_calib/Landsat-Buoy-Calibration/buoycalib/settings.py
- these websites will help you search to find your own scenes / buoys
  - for buoys: http://www.ndbc.noaa.gov/
  - for landsat scenes: https://earthexplorer.usgs.gov/,  Collection 1 Level 1 - Landsat 8 OLI/TIRS C1 Level 1
  - for modis scenes: https://ladsweb.modaps.eosdis.nasa.gov/search/, look for Terra-MODIS, then MOD021KM
- landsat scenes before 2017 do not work currently

### Sources:
 - http://scholarworks.rit.edu/theses/2961/ - Padula 08 Thesis
 - http://scholarworks.rit.edu/theses/8513/ - Cook 14 Thesis

### Tools:
 - tools/to_csv.py: used to compile results quickly and easily.
 - tools/generate_atmo_figure.py : generate a figure using information from a already processed scene.
 - test/functional/run_all_scenes.bash: run a batch of scenes. Move it to this directory before use.


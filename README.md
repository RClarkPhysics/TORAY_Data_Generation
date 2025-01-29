# TORAY_Data_Generation
This Repository serves as a guide for running TORAY in OMFIT over many iterations to generate data for a surrogate model. Each script is written such that only one gyroton is running at a time. This gyrotron can have it's location, launch angle, frequency, and power customized. The scripts are focussed on doing sweeps of the launch angle (poloidal and toroidal) and scaling the temperature and density profiles of the plasma.

# Getting started:

* Have access to General Atomics Servers to access OMFIT.
* Before running extensive programs in the Omega cluster, it is proper ettiquite to connect to a worker node to run projects. Fortunately, OMFIT is wrapped in an srun command that automatically runs OMFIT projects on one of four worker nodes. More info: https://fusionga.sharepoint.com/sites/Computing/SitePages/Omega.aspx
* Boot up OMFIT with the following commands:
  * module load omfit
  * omfit
* Loading an OMFIT Project
  * Once in OMFIT, load the TORAY_Data_Generation zip file attached in this repo (click through the OMFIT popup, then go to File > Open Project). This will boot up the OMFIT project created to run TORAY through many iterations. Go to the treename SCRIPTS, open the drop down menu and click on the "TORAY_Angle_Sweep_1Gyrotron".
* Loading the Scripts 
  * Highlight one of the designated "USER" scripts by left clicking on it, then right click in the command box and select "load from tree".
* Running iterations of TORAY
  * With the chosen script loaded in the command box, there is a designated area at the top of each script for users to select sweeping parameters. Hit "execute" to begin the script.
* Accessing Results
  * The Data gets stored in the "DATA_STORAGE" tree, with the naming convention TORAY_ShotNumber_Time_PoloidalAngle(In degrees)_ToroidalAngle(In degrees)
  * Note that the Time will be the used time, not the requested time (if the time had to be shifted do to closest data, the title will reflect that and list the used time over the requested one).

# Script Descriptions
* Test_angle.py
* Time_Fitting.py
* TORAY_Angle_Sweep_1Gyrotron.py
* USER_TORAY_Angle_TimeSlice_Sweep
* USER_TORAY_Shot_Time_Angle_Sweeper

-General Script
-Plotting Script


# Parameter Descriptions
* Poloidal Angle
  * Physical Meaning: 
* Toroidal Angle
  * Physical Meaning: 
* Density Scalar
  * Physical Meaning: 
* Temperature Scalar
  * Physical Meaning: 
* Time Slice
  * The times that are available in ZIPFIT will vary from shot to shot. This creates an issue where a user could request TORAY runs at a time, say 500 ms, for one shot, but data only exists at 490 ms and 510 ms in another resulting in an error ending data generation. The implemented solution is for the user to request an array of times and the script will find the closest avialable time to those requested times (rounding down when equidistant) (times outside of the ZIPFIT bounds will be discarded as well).
* Shot Number
  * The DIII-D shot that the desnity and temperature profiles will be taken from. Note that TORAY will throw a fit with certain shot numbers if data isn't available for it.

# TORAY Output Description

# How TORAY Works (A Small Introduction)

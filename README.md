# TORAY_Data_Generation
(Work in Progress!)

This Repository serves as a guide for running TORAY in OMFIT over many iterations to generate data for a surrogate model.

Works in Progress:
* Automation of time slice (this is shot dependent, need to find the source so user input isn't required)
* ne and te sweeping script
* Output description
* Description of how TORAY works

# Getting started:

* Have access to General Atomics Servers to access OMFIT.
* Don't run endless iterations of TORAY in the login node, use a worker node with the following command:
  * Looking for This
* Boot up OMFIT with the following commands:
  * module load omfit
  * omfit
* Once in OMFIT, load the TORAY_Data_Generation zip file attached in this repo (click through the OMFIT popup, then go to File > Open Project). This will boot up the OMFIT project created to run TORAY through many iterations. Go to the treename SCRIPTS, open the drop down menu and click on the "TORAY_Angle_Sweep_1Gyrotron", then right click in the command box and select "load from tree. This will populate the command box with the script that can run many iterations of TORAY.
* At the moment, the script is limited to iterations over angles, choose a shot number, a time slice (these can be found in the GUI; double click TORAY to access the GUI), and an array of angles, then click "Execute". Your Data can be found in the DATA_STORAGE tree.

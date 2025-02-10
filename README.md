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
  * Note that each TORAY loop takes roughly 10 seconds.
* Accessing Results
  * The Data gets stored in the "DATA_STORAGE" tree, with the naming convention TORAY_ShotNumber_Time_PoloidalAngle(In degrees)_ToroidalAngle(In degrees)_ne scalar_te scalar (ne and te scaling labels are not included in the save file produced in the general script since it doesn't sweep over ne and te)
  * Note that the Time will be the used time, not the requested time (if the time had to be shifted do to closest data, the title will reflect that and list the used time over the requested one).

# Script Descriptions
The scripts can be seen in the SCRIPTS folder of this repo for visibility, but are already in the zip file.
* USER_General_Sweep.py
  * This is the script users will generate data with the most, it is a general purpose sweeper across a set of shots, time slices, poloidal angles, and toroidal angles.
* USER_Profile_Sweeper.py
  * This script is the same as the general, but it includes additional sweeping tools for the scale ne profile and te profile. The ne_scalar and te_scalar are multiplied to every value in the temperatur and density profile allowing some limited flexibility to modify these profiles.
* USER_Single_Angle_Test.py
  * This script is to run single simulations of TORAY for different shots, times, and angles.
* Time_Fitting.py
  * This script isn't meant for users to edit. It's purpose is to take the requested times for a sweep and find their closest matching time in the ZIPFIT files. It's best to know beforehand what time slices you want, but this isn't practical when sweeping across a large number of shots with different time slice intervals.



# Parameter Descriptions
* Poloidal Angle
  * Physical Meaning: The poloidal angle determines if the waves will hit the top, midplane, or bottom of the plasma (up/down direction).An input of 90 degrees launches rays straight into the plasma, in a direction parallel to ground.
* Toroidal Angle
  * Physical Meaning: The toroidal angle determines how the waves will enter the plasma (left/right direction). An input of 180 degrees sends the waves straight into the plasma, pointing directly at the inner wall. Lowing the toroidal angle below 180 degrees causes the launcher to send waves in a clockwise direction, rotating about the gyrotron launch point.
* Density Scalar
  * Physical Meaning: It simply multiplies every value in the density profile, scaling the whole thing by a multiple of the chosen scalar (defaults to 1.0).
* Temperature Scalar
  * Physical Meaning: It simply multiplies every value in the temperature profile, scaling the whole thing by a multiple of the chosen scalar (defaults to 1.0).
* Time Slice
  * The times that are available in ZIPFIT will vary from shot to shot. This creates an issue where a user could request TORAY runs at a time, say 500 ms, for one shot, but data only exists at 490 ms and 510 ms in another resulting in an error ending data generation. The implemented solution is for the user to request an array of times and the script will find the closest avialable time to those requested times (rounding down when equidistant) (times outside of the ZIPFIT bounds will be discarded as well).
* Shot Number
  * The DIII-D shot that the desnity and temperature profiles will be taken from. Note that TORAY will throw a fit with certain shot numbers if data isn't available for it.

# TORAY Output Description
TORAY will output a folder for each active gyrotron, in our case just 1, and in that folder is the TORAY result (toray.nc) and the TORBEAM result (torbeam). Our interests are primarily focused on the 'weecrh' and 'currf' items in toray.nc.
* 'weecrh'
  * It's described as the RF power density in each bin, per increment power, in other words the amount of power deposited in a defined bin. It has units Watts/cm^3/(incident Watt). The power deposition is caluted by multiplying this data by the power injected into the plasma from the gryotron.
* 'currf'
  * This is the generated current drive resulting from the EC wave injection. It has units A/cm^2/(incident Watt). It shares the same binning that 'weecrh' has and can be used to calculate the current drive at the location of each bin by multiplying the 'currf' value by the power injected into the plasma from the gryotron.
* 'xmrho'
  * The location of the bins is defined by 'xmrho'.

# TORAY Background
TORAY is a ray tracing code that was developed to study electron-cyclotron heating and current drive in torodial geometry. The energy that the rays deposit there energy is in the resonance zone and is largely independent of edge conditions allowing for control over which part of the plasma profile the scientist whishes to deposit the energy. TORAY is able to make these predictions by integrating the ray equations of geomtetric optics, which can be used because of how the electron cycolotron wave energy is nearly optical. There are important factors that go into how EC wave energy is deposited into the plasma. The resonant layer location is a significantly important part of ECH and ECCD, in some cases, the refraction of the EC wave due to the density gradient and magnitude of the plasma can lead it out to the plasma edge before reaching the resonant layer, resulting in little to no power being deposited in the plasma. Density itself impacts how much energy gets deposited in the resonance layer. Other important factors that affect the energy deposition is the temperautre of the plasma, the launch angle, the q profile, and tokamak size. For a more detailed analysis, see reference [1].

Here are some results from running TORAY:

<img width="559" alt="Screenshot 2025-01-30 at 11 20 15 AM" src="https://github.com/user-attachments/assets/c4eea4a8-7ee6-4ea2-87ef-0ccfd45db6f1" />
<img width="560" alt="Screenshot 2025-01-30 at 11 20 05 AM" src="https://github.com/user-attachments/assets/02ba11f1-32c7-4459-ab4a-9cc391bfa108" />
<img width="670" alt="Screenshot 2025-01-30 at 11 18 28 AM" src="https://github.com/user-attachments/assets/8596d6a7-7a10-42ba-a7e8-4e9d22ca79da" />



Rerences:
[1] Kritz, A. H., et al. "Ray tracing study of electron cyclotron heating in toroidal geometry." Heating in Toroidal Plasmas 1982. Pergamon, 1982. 707-723.






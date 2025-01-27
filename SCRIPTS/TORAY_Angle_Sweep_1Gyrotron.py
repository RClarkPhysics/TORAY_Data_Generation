## Angle Sweep
import numpy as np

#Choose a Shot Number and Time
ShotNum = 161414
Time = 3000

#Choose an array of poloidal and toroidal angles
pol_angle = np.linspace(90,130,2)
tor_angle = np.linspace(180,220,2)


#----------NO USER Input Required Below--------------------


#Create DATA_STORAGE Folder if it doesn't already exist
if 'DATA_STORAGE' not in OMFIT.keys():
    OMFIT['DATA_STORAGE'] = OMFITtree()

#Stepup the standard TORAY conditions
OMFIT['TORAY']['SETTINGS']['SETUP']['runType'] = 'Standard toray run'
OMFIT['TORAY']['SETTINGS']['EXPERIMENT']['device'] = 'DIII-D'
OMFIT['TORAY']['SETTINGS']['EXPERIMENT']['shot'] = ShotNum
OMFIT['TORAY']['SETTINGS']['PHYSICS']['inputDATA'] = 'ZIPFITs'
OMFIT['TORAY']['SETTINGS']['PHYSICS']['EFIT_type'] = 'EFIT01'
OMFIT['TORAY']['SETTINGS']['EXPERIMENT']['time'] = Time

OMFIT['TORAY']['SCRIPTS']['generate_profiles'].run()
OMFIT['TORAY']['SCRIPTS']['fetchGyrotronsData'].run()


#Gyrotrons
GYROTRONS = OMFIT['TORAY']['INPUTS']['ods']['ec_launchers.code.parameters']['beam']

#Turn on and off the GyroTrons (1 on, 0 off)
#Run only 1 gyrotron, Leia
GYROTRONS[0]['ON'] = 1  #Leia
GYROTRONS[1]['ON'] = 0  #Luke
GYROTRONS[2]['ON'] = 0  #Scarecrow
GYROTRONS[3]['ON'] = 0  #Tinman
GYROTRONS[4]['ON'] = 0  #Chewbacca
GYROTRONS[5]['ON'] = 0  #NASA

#Convert the angles to radian and apply
POLS = np.radians(pol_angle - 90)
TORS = np.radians(tor_angle - 180)

#Loop through all sets of angles
STEERING = OMFIT['TORAY']['INPUTS']['ods']['ec_launchers']['beam']
for p in POLS:
    for t in TORS:
        p_degree = np.degrees(p) + 90
        t_degree = np.degrees(t) + 180

        #Set the Angles
        STEERING['0']['steering_angle_pol'] = np.array([p])
        STEERING['0']['steering_angle_tor'] = np.array([t])
        
        #Create a Folder to store the TORAY OUTPUTS
        if 'TORAY_'+str(ShotNum)+'_'+str(Time)+'_'+str(p_degree)+'_'+str(t_degree) not in OMFIT['DATA_STORAGE'].keys():
            OMFIT['DATA_STORAGE']['TORAY_'+str(ShotNum)+'_'+str(Time)+'_'+str(p_degree)+'_'+str(t_degree)] = OMFITtree()
        
        #Clear the OUTPUTS of the previous run
        OMFIT['TORAY']['OUTPUTS'].clear()

        #Run TORAY
        OMFIT['TORAY']['SCRIPTS']['run_toray_all_gyrotrons'].run()

        #Save the Result
        OMFIT['DATA_STORAGE']['TORAY_'+str(ShotNum)+'_'+str(Time)+'_'+str(p_degree)+'_'+str(t_degree)] = OMFIT['TORAY']['OUTPUTS'].duplicate()



        
        
        




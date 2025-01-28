## Angle and Time Slice Sweep
import numpy as np

#Choose a Shots
ShotList = np.array([161414,196082])

#Choose Time Slices for the Shot (times outside of the ZIP fit range will be discarded,
#and ties within the range will be chosen to be the nearest time with avaialable data)
Times = np.arange(500,4001,2000)

#Choose an array of poloidal and toroidal angles
pol_angle = np.linspace(90,130,2)
tor_angle = np.linspace(180,220,2)


#----------NO USER Input Required Below------------------------


#--------------------Setup---------------------------------
#Create DATA_STORAGE Folder if it doesn't already exist
if 'DATA_STORAGE' not in OMFIT.keys():
    OMFIT['DATA_STORAGE'] = OMFITtree()

#Create a Variables Folder if it doesn't already exist
if 'Variables' not in OMFIT.keys():
    OMFIT['Variables'] = OMFITtree()

#---------------loop over Shots--------------------------------
for ShotNum in ShotList:
    #Prepare Run Time Data
    OMFIT['Variables']['ShotNum'] = ShotNum
    OMFIT['Variables']['times'] = Times
    OMFIT['SCRIPTS']['Time_Fitting'].run()
    #The Time_Fitting Script has prepared our run times in this tree
    Run_Times = OMFIT['Variables']['Run_times']

    #Stepup the standard TORAY conditions
    OMFIT['TORAY']['SETTINGS']['SETUP']['runType'] = 'Standard toray run'
    OMFIT['TORAY']['SETTINGS']['EXPERIMENT']['device'] = 'DIII-D'
    OMFIT['TORAY']['SETTINGS']['EXPERIMENT']['shot'] = ShotNum
    OMFIT['TORAY']['SETTINGS']['PHYSICS']['inputDATA'] = 'ZIPFITs'
    OMFIT['TORAY']['SETTINGS']['PHYSICS']['EFIT_type'] = 'EFIT01'

    #Convert the angles to radian
    POLS = np.radians(pol_angle - 90)
    TORS = np.radians(tor_angle - 180)
    STEERING = OMFIT['TORAY']['INPUTS']['ods']['ec_launchers']['beam']
    #--------------------Begin Looping through Time and angle runs of TORAY---------------------------
    for r in Run_Times:
        #Setup the simulation
        OMFIT['TORAY']['SETTINGS']['EXPERIMENT']['time'] = r
        OMFIT['TORAY']['SCRIPTS']['generate_profiles'].run()
        OMFIT['TORAY']['SCRIPTS']['fetchGyrotronsData'].run()

        #Gyrotrons Name
        GYROTRONS = OMFIT['TORAY']['INPUTS']['ods']['ec_launchers.code.parameters']['beam']
        #Turn on and off the GyroTrons (1 on, 0 off)
        #Run only 1 gyrotron, Leia
        GYROTRONS[0]['ON'] = 1  #Leia
        GYROTRONS[1]['ON'] = 0  #Luke
        GYROTRONS[2]['ON'] = 0  #Scarecrow
        GYROTRONS[3]['ON'] = 0  #Tinman
        GYROTRONS[4]['ON'] = 0  #Chewbacca
        GYROTRONS[5]['ON'] = 0  #NASA

        for p in POLS:
            for t in TORS:
                p_degree = np.degrees(p) + 90
                t_degree = np.degrees(t) + 180

                #Set the Angles
                STEERING['0']['steering_angle_pol'] = np.array([p])
                STEERING['0']['steering_angle_tor'] = np.array([t])

                #Create a Folder to store the TORAY OUTPUTS
                if 'TORAY_'+str(ShotNum)+'_'+str(r)+'_'+str(p_degree)+'_'+str(t_degree) not in OMFIT['DATA_STORAGE'].keys():
                    OMFIT['DATA_STORAGE']['TORAY_'+str(ShotNum)+'_'+str(r)+'_'+str(p_degree)+'_'+str(t_degree)] = OMFITtree()

                #Clear the OUTPUTS of the previous run
                OMFIT['TORAY']['OUTPUTS'].clear()

                #Run TORAY
                OMFIT['TORAY']['SCRIPTS']['run_toray_all_gyrotrons'].run()

                #Save the Result
                OMFIT['DATA_STORAGE']['TORAY_'+str(ShotNum)+'_'+str(r)+'_'+str(p_degree)+'_'+str(t_degree)] = OMFIT['TORAY']['OUTPUTS'].duplicate()

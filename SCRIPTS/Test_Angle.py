## Test Angle
ShotNum = 161414
Time = 3000

pol_angle = 115
tor_angle = 212

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
GYROTRONS[0]['ON'] = 1  #Leia
GYROTRONS[1]['ON'] = 0  #Luke
GYROTRONS[2]['ON'] = 0  #Scarecrow
GYROTRONS[3]['ON'] = 0  #Tinman
GYROTRONS[4]['ON'] = 0  #Chewbacca
GYROTRONS[5]['ON'] = 0  #NASA

#Convert the angles to radian and apply
POLS = np.radians(pol_angle - 90)
TORS = np.radians(tor_angle - 180)
LAUNCHER = OMFIT['TORAY']['INPUTS']['ods']['ec_launchers']['beam']
LAUNCHER['0']['steering_angle_pol'] = np.array([POLS])
LAUNCHER['0']['steering_angle_tor'] = np.array([TORS])

#Run TORAY
OMFIT['TORAY']['SCRIPTS']['run_toray_all_gyrotrons'].run()











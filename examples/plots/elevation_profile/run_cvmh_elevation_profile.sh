#!/usr/bin/sh  
CWD=`pwd`
LABEL=cvmh_elevation_profile
LAT=34
LON=-115
STEP=-10
START_elevation=1000
END_elevation=-3000
MODEL=cvmh 

cd ${UCVM_INSTALL_PATH}/utilities

./plot_elevation_profile.py -s ${LAT},${LON} -b ${START_elevation} -e ${END_elevation} -d vs,vp,density -v ${STEP} -c ${MODEL} -o ${CWD}/${LABEL}.png

./plot_elevation_profile.py -s ${LAT},${LON} -b ${START_elevation} -e ${END_elevation} -d vs -v ${STEP} -c ${MODEL} -f ${CWD}/${LABEL}_matprops.json -o ${CWD}/${LABEL}_vs.png

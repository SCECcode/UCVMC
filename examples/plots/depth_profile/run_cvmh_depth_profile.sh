#!/usr/bin/sh  

if [ -z "$UCVM_INSTALL_PATH" ]; then
  echo "Need to set UCVM_INSTALL_PATH to run >" ${0##*/} 
  exit
fi

CWD=`pwd`
LABEL=cvmh_depth_profile
LAT=34
LON=-118
STEP=500
START_depth=0
END_depth=50000
MODEL=cvmh 

cd ${UCVM_INSTALL_PATH}/utilities

./plot_depth_profile.py -s ${LAT},${LON} -b ${START_depth} -e ${END_depth} -d vs,vp,density -v ${STEP} -c ${MODEL} -o ${CWD}/${LABEL}.png

./plot_depth_profile.py -s ${LAT},${LON} -b ${START_depth} -e ${END_depth} -d vs -v ${STEP} -c ${MODEL} -f ${CWD}/${LABEL}_matprops.json -o ${CWD}/${LABEL}_vs.png


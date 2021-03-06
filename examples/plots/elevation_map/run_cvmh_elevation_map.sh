#!/usr/bin/sh  

if [ -z "$UCVM_INSTALL_PATH" ]; then
  echo "Need to set UCVM_INSTALL_PATH to run >" ${0##*/} 
  exit
fi

CWD=`pwd`
LABEL=cvmh_elevation_map
LAT1=33.35
LON1=-118
LAT2=34.35
LON2=-117
SPACING=0.01
MODEL=cvmh 

## outside of installdir
${UCVM_INSTALL_PATH}/utilities/plot_elevation_map.py -b ${LAT1},${LON1} -u ${LAT2},${LON2} -c ${MODEL} -a s -s ${SPACING} -o ${CWD}/${LABEL}_o.png -i ${UCVM_INSTALL_PATH}

cd ${UCVM_INSTALL_PATH}/utilities

./plot_elevation_map.py -b ${LAT1},${LON1} -u ${LAT2},${LON2} -c ${MODEL} -a s -s ${SPACING} -o ${CWD}/${LABEL}.png

./plot_elevation_map.py -b ${LAT1},${LON1} -u ${LAT2},${LON2} -c ${MODEL} -a d -s ${SPACING} -f ${CWD}/${LABEL}_data.bin -o ${CWD}/${LABEL}_d.png

./plot_elevation_map.py -H


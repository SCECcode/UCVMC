#!/usr/bin/sh  

if [ -z "$UCVM_INSTALL_PATH" ]; then
  echo "Need to set UCVM_INSTALL_PATH to run >" ${0##*/} 
  exit
fi

LABEL=cvmh_elevation_cross_section_vs
LAT1=35
LON1=-121
LAT2=35
LON2=-118
START_elevation=2000
END_elevation=-8000
MODEL=cvmh 

${UCVM_INSTALL_PATH}/utilities/plot_elevation_cross_section.py -b ${LAT1},${LON1} -u ${LAT2},${LON2} -h 1000 -v -100 -d vs -c ${MODEL} -a s -s ${START_elevation} -e ${END_elevation} -i ${UCVM_INSTALL_PATH} -o ${LABEL}.png

${UCVM_INSTALL_PATH}/utilities/plot_elevation_cross_section.py -b ${LAT1},${LON1} -u ${LAT2},${LON2} -h 1000 -v -100 -d vs -c ${MODEL} -a d -s ${START_elevation} -e ${END_elevation} -f ${LABEL}_data.bin -i ${UCVM_INSTALL_PATH} -o ${LABEL}_d.png


#!/usr/bin/sh  
#LongBeach4, 33.7,-118.21,33.90,-118.22, 0.0,1000,100,-900
CWD=`pwd`
LABEL=cvmh_cross_section_vs
LAT1=35
LON1=-121
LAT2=35
LON2=-118
START_elevation=2000
END_elevation=-8000
MODEL=cvmh 

cd ${UCVM_INSTALL_PATH}/utilities

./plot_elevation_cross_section.py -b ${LAT1},${LON1} -u ${LAT2},${LON2} -h 1000 -v 100 -d vs -c ${MODEL} -a s -s ${START_elevation} -e ${END_elevation} -o ${CWD}/${LABEL}.png

cd ${CWD}

#${UCVM_INSTALL_PATH}/utilities/plot_cross_section.py -b ${LAT1},${LON1} -u ${LAT2},${LON2} -h 1000 -v 100 -d vs -c ${MODEL} -a s -s ${START_depth} -e ${END_depth} -i ${UCVM_INSTALL_PATH} -o ${LABEL}.png

#${UCVM_INSTALL_PATH}/utilities/plot_cross_section.py -b ${LAT1},${LON1} -u ${LAT2},${LON2} -h 10 -v 2 -d vs -c ${MODEL} -a d -s ${START_depth} -e ${END_depth} -f ${LABEL}_data.bin -i ${UCVM_INSTALL_PATH} -o ${LABEL}_d.png




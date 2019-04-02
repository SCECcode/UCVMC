#!/usr/bin/sh  
LABEL=cvmh_cross_section_vs
LAT1=33.7
LON1=-118.21
LAT2=33.9
LON2=-118.22
START_depth=0.0
END_depth=1000
MODEL=cvmh 

${UCVM_INSTALL_PATH}/utilities/plot_cross_section.py -b ${LAT1},${LON1} -u ${LAT2},${LON2} -h 10 -v 2 -d vs -c ${MODEL} -a s -s ${START_depth} -e ${END_depth} -i ${UCVM_INSTALL_PATH} -o ${LABEL}.png

${UCVM_INSTALL_PATH}/utilities/plot_cross_section.py -b ${LAT1},${LON1} -u ${LAT2},${LON2} -h 10 -v 2 -d vs -c ${MODEL} -a d -s ${START_depth} -e ${END_depth} -f ${LABEL}_data.bin -i ${UCVM_INSTALL_PATH} -o ${LABEL}_d.png




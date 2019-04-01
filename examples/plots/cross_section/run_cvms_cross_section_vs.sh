#!/usr/bin/sh  
#LongBeach4, 33.7,-118.21,33.90,-118.22, 0.0,1000,100,-900
DIR=${UCVM_INSTALL_PATH}/utilities
LABEL=cvms_cross_section_vs
LAT1=33.7
LON1=-118.21
LAT2=33.9
LON2=-118.22
START_depth=0.0
END_depth=1000
MODEL=cvms 

${DIR}/plot_cross_section.py -b ${LAT1},${LON1} -u ${LAT2},${LON2} -h 10 -v 2 -d vs -c ${MODEL} -a s -s ${START_depth} -e ${END_depth} -o ${LABEL}.png

#${DIR}/plot_cross_section.py -b ${LAT1},${LON1} -u ${LAT2},${LON2} -h 10 -v 2 -d vs -c ${MODEL} -a d -s ${START_depth} -e ${END_depth} -f ${LABEL}_data.bin -o ${LABEL}_d.png




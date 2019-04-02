#!/usr/bin/sh  
CWD=`pwd`
LABEL=cvmh_vs30_etree_map
LAT1=33.35
LON1=-118
LAT2=34.35
LON2=-117
SPACING=0.01
MODEL=cvmh 


cd ${UCVM_INSTALL_PATH}/utilities

./plot_vs30_etree_map.py -b ${LAT1},${LON1} -u ${LAT2},${LON2} -c ${MODEL} -a s -s ${SPACING} -o ${CWD}/${LABEL}.png

./plot_vs30_etree_map.py -b ${LAT1},${LON1} -u ${LAT2},${LON2} -c ${MODEL} -a d -s ${SPACING} -f ${CWD}/${LABEL}_data.bin -o ${CWD}/${LABEL}_d.png

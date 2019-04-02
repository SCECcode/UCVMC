#!/usr/bin/sh  
## comparing data input of two plots
CWD=`pwd`
LABEL=cvmh_compare_plot
LAT1=33.35
LON1=-118
LAT2=34.35
LON2=-117
SPACING=0.01
MODEL=cvmh 

XLABEL=cvmh_vs30_map
YLABEL=cvmh_vs30_etree_map


cd ${UCVM_INSTALL_PATH}/utilities

./plot_vs30_map.py -b ${LAT1},${LON1} -u ${LAT2},${LON2} -c ${MODEL} -a s -s ${SPACING} -o ${CWD}/${XLABEL}.png

./plot_vs30_etree_map.py -b ${LAT1},${LON1} -u ${LAT2},${LON2} -c ${MODEL} -a s -s ${SPACING} -o ${CWD}/${YLABEL}.png

./plot_compare_plot.py -x ${CWD}/${XLABEL}_data.bin -y ${CWD}/${YLABEL}_data.bin -o ${CWD}/${LABEL}.png

./plot_compare_plot.py -x ${CWD}/${XLABEL}_data.bin -y ${CWD}/${XLABEL}_data.bin -o ${CWD}/${LABEL}_x.png

./plot_compare_plot.py -x ${CWD}/${YLABEL}_data.bin -y ${CWD}/${YLABEL}_data.bin -o ${CWD}/${LABEL}_y.png

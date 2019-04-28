#!/usr/bin/sh  

if [ -z "$UCVM_INSTALL_PATH" ]; then
  echo "Need to set UCVM_INSTALL_PATH to run >" ${0##*/} 
  exit
fi

CWD=`pwd`
LABEL=cvmh_vp_versus_density_0km
LAT1=30.5
LON1=-126
LAT2=42.5
LON2=-120.51
SPACING=1
DEPTH=0
MODEL=cvmh


cd ${UCVM_INSTALL_PATH}/utilities

# 0 depth
./make_map_grid.py -b ${LAT1},${LON1} -u ${LAT2},${LON2} -s ${SPACING} -e ${DEPTH} -c ${MODEL}  -o ${CWD}/${LABEL}_map_grid.txt

./plot_scatter_plot.py -i ${CWD}/${LABEL}_map_grid.txt  -e ${DEPTH} -o ${CWD}/${LABEL}.png -n "CVMH Vp Density Scatter Plot 0k"

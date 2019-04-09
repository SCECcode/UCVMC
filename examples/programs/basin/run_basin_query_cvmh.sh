#!/usr/bin/sh

if [ -z "$UCVM_INSTALL_PATH" ]; then
  echo "Need to set UCVM_INSTALL_PATH to run >" ${0##*/} 
  exit
fi

BIN_DIR=${UCVM_INSTALL_PATH}/bin
CONF_DIR=${UCVM_INSTALL_PATH}/conf
TEST_DIR=${UCVM_INSTALL_PATH}/tests/inputs
MODEL=cvmh

${BIN_DIR}/basin_query -m ${MODEL} -f ${CONF_DIR}/ucvm.conf -v 2500.0 < ${TEST_DIR}/test_latlonsonly.txt > cvmh_z2500_basin_query.txt

${BIN_DIR}/basin_query -m ${MODEL} -f ${CONF_DIR}/ucvm.conf -v 1000.0 < ${TEST_DIR}/test_latlonsonly.txt > cvmh_z1000_basin_query.txt

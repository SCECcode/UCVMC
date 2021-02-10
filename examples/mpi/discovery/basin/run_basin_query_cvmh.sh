#!/bin/bash

if [ -z "$UCVM_INSTALL_PATH" ]; then
  echo "Need to set UCVM_INSTALL_PATH to run >" ${0##*/} 
  exit
fi

BIN_DIR=${UCVM_INSTALL_PATH}/bin
CONF_DIR=${UCVM_INSTALL_PATH}/conf
TEST_DIR=${UCVM_INSTALL_PATH}/tests/inputs
MODEL=cvmh

expect=$(mktemp) || exit 1
result=$(mktemp) || (trap 'rm -f "$expect"'; exit 1)

${BIN_DIR}/basin_query -m ${MODEL} -f ${CONF_DIR}/ucvm.conf -v 2500.0 < ${TEST_DIR}/test_latlonsonly.txt > $result 2>&1

cat > $expect << EOF_EXPECTED_RESULT_Z2500
 -118.0000    34.0000   3000.000   3000.000   3000.000
 -118.5000    34.5000    200.000    200.000    200.000
 -119.0000    33.0000      0.000      0.000      0.000
 -120.0000    33.0000      0.000      0.000      0.000
EOF_EXPECTED_RESULT_Z2500

echo "Running examples_programs_basin z2500 basin_query_cvmh"
if diff $result $expect > /dev/null 2>&1
then
  echo [SUCCESS]
else
  echo [FAILURE]
fi

trap 'rm -f "$expect" "$result"' exit

expect=$(mktemp) || exit 1
result=$(mktemp) || (trap 'rm -f "$expect"'; exit 1)

${BIN_DIR}/basin_query -m ${MODEL} -f ${CONF_DIR}/ucvm.conf -v 1000.0 < ${TEST_DIR}/test_latlonsonly.txt > $result 2>&1

cat > $expect << EOF_EXPECTED_RESULT_Z1000
 -118.0000    34.0000    400.000    400.000    400.000
 -118.5000    34.5000      0.000      0.000      0.000
 -119.0000    33.0000      0.000      0.000      0.000
 -120.0000    33.0000      0.000      0.000      0.000
EOF_EXPECTED_RESULT_Z1000

echo "Running examples_programs_basin z1000 basin_query_cvmh"
if diff $result $expect > /dev/null 2>&1
then
  echo [SUCCESS]
else
  echo [FAILURE]
fi

trap 'rm -f "$expect" "$result"' exit


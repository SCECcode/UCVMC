#!/bin/bash

if [ -z "$UCVM_INSTALL_PATH" ]; then
  echo "Need to set UCVM_INSTALL_PATH to run >" ${0##*/} 
  exit
fi
source $UCVM_INSTALL_PATH/conf/ucvm_env.sh

expect=$(mktemp) || exit 1
result=$(mktemp) || (trap 'rm -f "$expect"'; exit 1) 

./query_1d_gtl > $result 2>&1

cat > $expect << EOF_EXPECTED_RESULT
Init
Query Mode
Add Crustal Model 1D
Add GTL Model Ely
Create point
Query Model
Results:
	source=crust, vp=5125.000000, vs=2958.920130, rho=2674.237500
EOF_EXPECTED_RESULT

echo "Running examples_api query_1d_gtl"
if diff $result $expect > /dev/null 2>&1
then
  echo [SUCCESS]
else
  echo [FAILURE]
fi

trap 'rm -f "$expect" "$result"' exit

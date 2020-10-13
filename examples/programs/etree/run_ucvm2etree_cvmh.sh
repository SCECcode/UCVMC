#!/bin/bash

if [ -z "$UCVM_INSTALL_PATH" ]; then
  echo "Need to set UCVM_INSTALL_PATH to run >" ${0##*/} 
  exit
fi

BIN_DIR=${UCVM_INSTALL_PATH}/bin
CONF_DIR=${UCVM_INSTALL_PATH}/conf

expect=$(mktemp) || exit 1
result=$(mktemp) || (trap 'rm -f "$expect"'; exit 1)

sed 's ${CONF_DIR} '$CONF_DIR' ' garnervalley_cvmh.conf_template > garnervalley_cvmh.conf

${BIN_DIR}/ucvm2etree -f ./garnervalley_cvmh.conf > $result 2>&1


cat > $expect << EOF_EXPECTED_RESULT
[0] Using config file ./garnervalley_cvmh.conf
[0] Configuration:
	[0] Column Dims: 6, 8
	[0] Projection: geo-bilinear
		[0] Bilinear xi/yi 0: -116.859300 deg, 33.640300 deg
		[0] Bilinear xi/yi 1: -116.645700 deg, 33.795800 deg
		[0] Bilinear xi/yi 2: -116.398400 deg, 33.557200 deg
		[0] Bilinear xi/yi 3: -116.611900 deg, 33.402200 deg
		[0] Bilinear Dims: 26250.000000 m, 35000.000000 m
	[0] Region Dims: 26250.000000 m, 35000.000000 m, 4375.000000 m
	[0] Max Freq: 0.500000 Hz
	[0] Points/Wavelength: 10.000000
	[0] Max Cell Size: 10000.000000 m
	[0] Author: Elnza
	[0] Title: GarnerValley_0.5hz_10pts_1000ms
	[0] Date: 02/27/2019
	[0] Output File: ./garnervalley_cvmh_nogtl_0.5hz_10pts_1000ms.e
	[0] UCVM String: cvmh
	[0] UCVM Interp: 0.000000 m - 350.000000 m
	[0] UCVM Conf: /project/maechlin_162/mei/ucvm_19_4/UCVM_TARGET/conf/ucvm.conf
	[0] Vs Min: 1000.000000 m/s
	[0] Scratch Dir: ./scratch

[0] Buffers:
	[0] Etree Cache: 128 MB
	[0] Extract Mem Max Oct: 4194304
	[0] Extract FF Max Oct: 16000000
	[0] Sort FF Max Oct: 20000000
	[0] Merge Report Min Oct: 10000000
	[0] Merge SendRecv Buf Oct: 4096
	[0] Merge IO Buf Oct: 4194304

[0] Calculated for 0.500000 Hz, 1000.000000 m/s, 10.000000 ppwl:
	[0] Min Edge Size To Support Vs Min: 200.000000 m
	[0] Max Edge Size To Allow: 4375.000000 m
	[0] Max Level: 8 (136.718750 m)
	[0] Min Level: 3 (4375.000000 m)
	[0] Tick Size: 1.629815e-05 m
	[0] Col X,Y,Z Tics: 268435456, 268435456, 268435456

Setting up UCVM
Opening etree ./garnervalley_cvmh_nogtl_0.5hz_10pts_1000ms.e
Registering schema
Allocating buffers to hold 1024 points
Extracting col 0,0
Extracting col 1,0
Extracting col 2,0
Extracting col 3,0
Extracting col 4,0
Extracting col 5,0
Extracting col 0,1
Extracting col 1,1
Extracting col 2,1
Extracting col 3,1
Extracting col 4,1
Extracting col 5,1
Extracting col 0,2
Extracting col 1,2
Extracting col 2,2
Extracting col 3,2
Extracting col 4,2
Extracting col 5,2
Extracting col 0,3
Extracting col 1,3
Extracting col 2,3
Extracting col 3,3
Extracting col 4,3
Extracting col 5,3
Extracting col 0,4
Extracting col 1,4
Extracting col 2,4
Extracting col 3,4
Extracting col 4,4
Extracting col 5,4
Extracting col 0,5
Extracting col 1,5
Extracting col 2,5
Extracting col 3,5
Extracting col 4,5
Extracting col 5,5
Extracting col 0,6
Extracting col 1,6
Extracting col 2,6
Extracting col 3,6
Extracting col 4,6
Extracting col 5,6
Extracting col 0,7
Extracting col 1,7
Extracting col 2,7
Extracting col 3,7
Extracting col 4,7
Extracting col 5,7
Total of 61312 octants extracted
Setting application metadata
Saving metadata: Title:GarnerValley_0.5hz_10pts_1000ms Author:Elnza Date:02/27/2019 3 Vp(float);Vs(float);density(float) 33.640300 -116.859300 26250.000000 35000.000000 0.000000 4375.000000 1610612736 2147483648 268435456
Closing etree
EOF_EXPECTED_RESULT

echo "Running examples_programs_ucvm2etree ucvm2etree_cvmh"
if diff $result $expect > /dev/null 2>&1
then
  echo [SUCCESS]
else
  echo [FAILURE]
fi

trap 'rm -f "$expect" "$result"' exit


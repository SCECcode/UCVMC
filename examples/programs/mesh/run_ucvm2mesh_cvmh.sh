#!/usr/bin/env sh

if [ -z "$UCVM_INSTALL_PATH" ]; then
  echo "Need to set UCVM_INSTALL_PATH to run >" ${0##*/} 
  exit
fi

BIN_DIR=${UCVM_INSTALL_PATH}/bin
CONF_DIR=${UCVM_INSTALL_PATH}/conf
SCRATCH=./scratch

sed 's ${CONF_DIR} '$CONF_DIR' ' small_cvmh.conf_template | sed 's ${SCRATCH} '$SCRATCH' ' > small_cvmh.conf

expect=$(mktemp) || exit 1
result=$(mktemp) || (trap 'rm -f "$expect"'; exit 1)

${BIN_DIR}/ucvm2mesh -f small_cvmh.conf |sed 's/in .* pps/in ABC/' > $result 2>&1 

cat > $expect << EOF_EXPECTED_RESULT
[0] Using config file small_cvmh.conf
[0] Configuration:
	[0] UCVM Model List: cvmh,1d
	[0] UCVM Conf file: /project/maechlin_162/mei/ucvm_19_4/UCVM_TARGET/conf/ucvm.conf
	[0] Gridtype: 0
	[0] Querymode: 0
	[0] Spacing: 10.000000
	[0] Projection: +proj=utm +datum=WGS84 +zone=11
		[0] Rotation Angle: -39.900000
		[0] Origin x0,y0,z0: -121.000000, 32.000000, 0.000000
		[0] Dimensions: 6, 5, 11
	[0] Proc Dimensions: 2, 1, 1
	[0] Vp Min: 0.000000, Vs Min: 0.000000
	[0] Mesh File: ./small_cvmh.media
	[0] Grid File: ./small_cvmh.grid
	[0] Mesh Type: 1
	[0] Scratch Dir: ./scratch
Setting up UCVM
Generating 2D grid
Converting grid to latlong
Grid generation complete
Allocating 30 grid points
Mesh dimensions: 6 x 5 x 11
Reading grid points
Extracted slice 0 (30 pnts) in ABC
Wrote slice 0 (30 pnts) in ABC
Extracted slice 1 (30 pnts) in ABC
Wrote slice 1 (30 pnts) in 0.00 ms
Extracted slice 2 (30 pnts) in ABC
Wrote slice 2 (30 pnts) in 0.00 ms
Extracted slice 3 (30 pnts) in ABC
Wrote slice 3 (30 pnts) in 0.00 ms
Extracted slice 4 (30 pnts) in ABC
Wrote slice 4 (30 pnts) in 0.00 ms
Extracted slice 5 (30 pnts) in ABC
Wrote slice 5 (30 pnts) in 0.00 ms
Extracted slice 6 (30 pnts) in ABC
Wrote slice 6 (30 pnts) in 0.00 ms
Extracted slice 7 (30 pnts) in ABC
Wrote slice 7 (30 pnts) in 0.00 ms
Extracted slice 8 (30 pnts) in ABC
Wrote slice 8 (30 pnts) in 0.00 ms
Extracted slice 9 (30 pnts) in ABC
Wrote slice 9 (30 pnts) in 0.00 ms
Extracted slice 10 (30 pnts) in ABC
Wrote slice 10 (30 pnts) in 0.00 ms
Extracted 330 points
Max Vp: 5000.000000 at
	i,j,k : 0, 0, 0
Max Vs: 2886.751465 at
	i,j,k : 0, 0, 0
Max Rho: 2654.500000 at
	i,j,k : 0, 0, 0
Min Vp: 5000.000000 at
	i,j,k : 0, 0, 0
Min Vs: 2886.751465 at
	i,j,k : 0, 0, 0
Min Rho: 2654.500000 at
	i,j,k : 0, 0, 0
Min Ratio: 1.732051 at
	i,j,k : 0, 0, 0
Done.
EOF_EXPECTED_RESULT

echo "Running examples_programs_ucvm2mesh ucvm2mesh_cvmh"
if diff $result $expect > /dev/null 2>&1
then
  echo [SUCCESS]
else
  echo [FAILURE]
fi

trap 'rm -f "$expect" "$result"' exit



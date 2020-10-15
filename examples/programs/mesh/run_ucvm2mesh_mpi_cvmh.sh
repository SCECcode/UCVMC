#!/bin/bash

if [ -z "$UCVM_INSTALL_PATH" ]; then
  echo "Need to set UCVM_INSTALL_PATH to run >" ${0##*/} 
  exit
fi

if ! [ -f "/usr/usc/openmpi/default/setup.sh" ]; then
## setup hpc mpi environment
  source /usr/usc/openmpi/default/setup.sh
  echo "Running on usc hpc cluster >" ${0##*/}             
fi

rm -rf ucvm2mesh_mpi ucvm.conf small_cvmh.conf

BIN_DIR=${UCVM_INSTALL_PATH}/bin
CONF_DIR=${UCVM_INSTALL_PATH}/conf
SCRATCH=./scratch
TEST=ucvm2mesh_mpi_cvmh

cp ${BIN_DIR}/ucvm2mesh_mpi .
cp ${CONF_DIR}/ucvm.conf .

sed 's ${CONF_DIR} '$CONF_DIR' ' small_cvmh.conf_template | sed 's ${SCRATCH} '$SCRATCH' ' > small_cvmh.conf

salloc -N 2 --ntasks=2 --time=00:20:00 srun --ntasks=2  -o ${TEST}.srun.out -v ./ucvm2mesh_mpi -f small_cvmh.conf




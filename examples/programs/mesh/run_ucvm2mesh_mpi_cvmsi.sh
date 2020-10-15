#!/bin/bash

if [ -z "$UCVM_INSTALL_PATH" ]; then
  echo "Need to set UCVM_INSTALL_PATH to run >" ${0##*/} 
  exit
fi

if [ -f "/usr/usc/openmpi/default/setup.sh" ]; then
  source /usr/usc/openmpi/default/setup.sh
  echo "Running on usc hpc cluster >" ${0##*/}             
fi

rm -rf ucvm2mesh_mpi ucvm.conf small-cvmsi.conf small_cvmsi.grid small_cvmsi.media

BIN_DIR=${UCVM_INSTALL_PATH}/bin
CONF_DIR=${UCVM_INSTALL_PATH}/conf
SCRATCH=./scratch
TEST=ucvm2mesh_mpi_cvmsi

cp ${BIN_DIR}/ucvm2mesh_mpi .
cp ${CONF_DIR}/ucvm.conf .

sed 's ${CONF_DIR} '$CONF_DIR' ' small_cvmsi.conf_template | sed 's ${SCRATCH} '$SCRATCH' ' > small_cvmsi.conf


salloc -N 4 --ntasks=8 --time=00:30:00 srun --ntasks=8 -o ${TEST}.srun.out -v ${BIN_DIR}/ucvm2mesh_mpi -f small_cvmsi.conf



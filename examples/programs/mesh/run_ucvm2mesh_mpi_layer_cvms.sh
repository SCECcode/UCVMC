#!/bin/bash

if [ -z "$UCVM_INSTALL_PATH" ]; then
  echo "Need to set UCVM_INSTALL_PATH to run >" ${0##*/} 
  exit
fi

if [ -f "/usr/usc/openmpi/default/setup.sh" ]; then
  source /usr/usc/openmpi/default/setup.sh
  echo "Running on usc hpc cluster >" ${0##*/}             
fi

BIN_DIR=${UCVM_INSTALL_PATH}/bin
CONF_DIR=${UCVM_INSTALL_PATH}/conf
SCRATCH=./scratch
TEST=ucvm2mesh_mpi_layer_cvms

rm -rf la_habra_cvms.grid la_habra_cvms.media la_habra_cvms.conf ucvm2mesh_mpi_layer ucvm.conf

cp ${BIN_DIR}/ucvm2mesh_mpi_layer .
cp ${CONF_DIR}/ucvm.conf .

sed 's ${CONF_DIR} '$CONF_DIR' ' la_habra_cvms.conf_template | sed 's ${SCRATCH} '$SCRATCH' '  > la_habra_cvms.conf

salloc -N 2 --ntasks=4 --time=00:30:00 srun --ntasks=4 -o ${TEST}_1.srun.out -v ./ucvm2mesh_mpi_layer -f la_habra_cvms.conf -l 1 -c 3
salloc --ntasks=4 --time=00:30:00 srun --ntasks=4 -o ${TEST}_2.srun.out -v ./ucvm2mesh_mpi_layer -f la_habra_cvms.conf -l 4 -c 3 
salloc --ntasks=4 --time=00:30:00 srun --ntasks=4 -o ${TEST}_3.srun.out -v ./ucvm2mesh_mpi_layer -f la_habra_cvms.conf -l 7 -c 4 
## or
##salloc -N 2 --ntasks=4 --time=00:30:00 srun --ntasks=4 -v ./ucvm2mesh_mpi_layer -f la_habra_cvms.conf -l 1 -c 10

echo "DONE"

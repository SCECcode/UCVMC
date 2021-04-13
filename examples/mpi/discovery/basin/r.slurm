#!/bin/bash
#SBATCH --ntasks=2
#SBATCH -N 1 
#SBATCH --mem 0 # Set to unlimited memory
#SBATCH --time=01:00:00 
#SBATCH -o discovery_cvms5_gtl_z1.0_complete.out
#SBATCH -e discovery_cvms5_gtl_z1.0_complete.err
#SBATCH --export=NONE 
#SBATCH --mail-user=mei@usc.edu
#SBATCH --mail-type=END


source /home1/mei/setup_env_proj.sh

export TEST_TOP_PATH=/project/scec_608/mei/ucvm_19_4/UCVM/examples/mpi/discovery/basin

###############################################################################

cd $SLURM_SUBMIT_DIR
cp ${UCVM_INSTALL_PATH}/bin/basin_query_mpi_complete .
cp ${UCVM_INSTALL_PATH}/conf/ucvm.conf .
cp ${UCVM_INSTALL_PATH}/conf/ucvm_bash.sh .

source ./ucvm_bash.sh


#minLat = 31
#minLon = -121
#nx = 1701
#ny = 1101
#gridSpacing = 0.005 

#env |grep LD_LIBRARY_PATH
#which ldd
#srun -v ldd ${SLURM_SUBMIT_DIR}/basin_query_mpi_complete 

mpirun ${SLURM_SUBMIT_DIR}/basin_query_mpi_complete -b ${TEST_TOP_PATH}/RESULT/hpc_cvms5_z1.0_complete.first,${TEST_TOP_PATH}/RESULT/hpc_cvms5_z1.0_complete.firstOrSecond,${TEST_TOP_PATH}/RESULT/hpc_cvms5_z1.0_complete.last,${TEST_TOP_PATH}/RESULT/hpc_cvms5_z1.0_complete.secondOnly,${TEST_TOP_PATH}/RESULT/hpc_cvms5_z1.0_complete.threeLast -o ${TEST_TOP_PATH}/RESULT/hpc_cvms5_z1.0_complete.result,${TEST_TOP_PATH}/RESULT/hpc_cvms5_z1.0_complete.meta.json -f ${SLURM_SUBMIT_DIR}/ucvm.conf -m cvms5  -i 20 -v 1000 -l 31,-121 -s 0.005 -x 1701 -y 1101


ret=$?

echo "Slurm Jobs done" `date`
exit $ret

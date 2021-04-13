#!/bin/bash
#SBATCH --ntasks=40 
#SBATCH -N 20
#SBATCH --mem 0 # Set to unlimited memory
#SBATCH --time=01:00:00 
#SBATCH -o /home/scec-00/mei/UCVM_REVIEW/RESULT/hpc_cvmsi_z1.0_proj.out
#SBATCH -e /home/scec-00/mei/UCVM_REVIEW/RESULT/hpc_cvmsi_z1.0_proj.err
#SBATCH --export=NONE 
#SBATCH --mail-user=mei@usc.edu
#SBATCH --mail-type=END


source /home/scec-00/mei/setup_env_proj.sh

export TEST_TOP_PATH=/home/scec-00/mei/UCVM_REVIEW
export TEST_SRC_PATH=${TEST_TOP_PATH}/UCVMC_TEST/hpc/reviewStudy

###############################################################################

cd $SLURM_SUBMIT_DIR
cp ${UCVM_INSTALL_PATH}/bin/basin_query_mpi_complete .
cp ${UCVM_INSTALL_PATH}/conf/ucvm.conf .


#minLat = 31
#minLon = -121
#nx = 1701
#ny = 1101
#gridSpacing = 0.005 

srun -v --mpi=pmi2 ${SLURM_SUBMIT_DIR}/basin_query_mpi_complete -b ${TEST_TOP_PATH}/RESULT/hpc_cvmsi_z1.0_proj.first,${TEST_TOP_PATH}/RESULT/hpc_cvmsi_z1.0_proj.firstOrSecond,${TEST_TOP_PATH}/RESULT/hpc_cvmsi_z1.0_proj.last,${TEST_TOP_PATH}/RESULT/hpc_cvmsi_z1.0_proj.secondOnly,${TEST_TOP_PATH}/RESULT/hpc_cvmsi_z1.0_proj.threeLast -o ${TEST_TOP_PATH}/RESULT/hpc_cvmsi_z1.0_proj.result,${TEST_TOP_PATH}/RESULT/hpc_cvmsi_z1.0_proj.meta.json -f ${SLURM_SUBMIT_DIR}/ucvm.conf -m cvmsi -i 20 -v 1000 -l 31,-121 -s 0.005 -x 1701 -y 1101


ret=$?

echo "Slurm Jobs done" `date`
exit $ret

#!/bin/bash

sudo apt-get install gfortran

pwd=`pwd`
export UCVM_SRC_PATH=$pwd
export UCVM_INSTALL_PATH=$pwd/TARGET_UCVMC
export LD_LIBRARY_PATH=$UCVM_INSTALL_PATH/lib/euclid3/lib:$UCVM_INSTALL_PATH/lib/proj-5/lib:$UCVM_INSTALL_PATH/model/cvms/lib:$UCVM_INSTALL_PATH/model/cvms5/lib:$UCVM_INSTALL_PATH/model/cvmh1511/lib 


mkdir $UCVM_INSTALL_PATH

cd $UCVM_SRC_PATH/largefiles
./get_large_files.py << EOF
n
n
n
n
y
n
n
y
n
EOF

cd $UCVM_SRC_PATH/largefiles; ./check_largefiles_md5.py
cd $UCVM_SRC_PATH/largefiles; ./stage_large_files.py

cd $UCVM_SRC_PATH
./ucvm_setup.py -d -a << EOF &> ucvm_setup_install.log
$UCVM_INSTALL_PATH
EOF

if [ -e $UCVM_SRC_PATH/bash_ucvm.sh ] 
then
  cp $UCVM_SRC_PATH/bash_ucvm.sh $UCVM_INSTALL_PATH/config
fi


#!/bin/bash

rm -rf $UCVM_SRC_PATH
source $UCVM_INSTALL_PATH/conf/ucvm_env.sh
cd $UCVM_INSTALL_PATH/tests
./run-testing

#!/usr/bin/sh

if [ -z "$UCVM_INSTALL_PATH" ]; then
  echo "Need to set UCVM_INSTALL_PATH to run >" ${0##*/} 
  exit
fi

BIN_DIR=${UCVM_INSTALL_PATH}/bin
CONF_DIR=${UCVM_INSTALL_PATH}/conf
SCRATCH=./scratch

echo $CONF_DIR

sed 's ${CONF_DIR} '$CONF_DIR' ' small_cvmh.conf_template 

#sed 's ${CONF_DIR} '$CONF_DIR' ' small_cvmh.conf_template | sed 's ${SCRATCH} '$SCRATCH' ' > small_cvmh.conf

#${BIN_DIR}/ucvm2mesh -f small_cvmh.conf



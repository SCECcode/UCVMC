#!/usr/bin/sh

if [ -z "$UCVM_INSTALL_PATH" ]; then
  echo "Need to set UCVM_INSTALL_PATH to run >" ${0##*/} 
  exit
fi

BIN_DIR=${UCVM_INSTALL_PATH}/bin
CONF_DIR=${UCVM_INSTALL_PATH}/conf

sed 's ${CONF_DIR} '$CONF_DIR' ' garnervalley_cvmh.conf_template > garnervalley_cvmh.conf

${BIN_DIR}/ucvm2etree -f ./garnervalley_cvmh.conf


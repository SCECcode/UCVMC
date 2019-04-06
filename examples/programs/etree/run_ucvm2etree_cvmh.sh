#!/usr/bin/sh
BIN_DIR=${UCVM_INSTALL_PATH}/bin
CONF_DIR=${UCVM_INSTALL_PATH}/conf

sed 's ${CONF_DIR} '$CONF_DIR' ' garnervalley_cvmh.conf_template > garnervalley_cvmh.conf

${BIN_DIR}/ucvm2etree -f ./garnervalley_cvmh.conf


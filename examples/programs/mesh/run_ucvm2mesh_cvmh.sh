#!/usr/bin/sh
BIN_DIR=${UCVM_INSTALL_PATH}/bin
CONF_DIR=${UCVM_INSTALL_PATH}/conf
SCRATCH=./scratch

sed 's ${CONF_DIR} '$CONF_DIR' ' small_cvmh.conf_template | sed 's ${SCRATCH} '$SCRATCH' ' > small_cvmh.conf

${BIN_DIR}/ucvm2mesh -f small_cvmh.conf



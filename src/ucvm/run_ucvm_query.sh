#!/bin/bash

## this is to run the ucvm_query with proper LD_LIBRARY_PATH and
## DYLD_LIBRARY_PATH that mac os seems to like to eliminate under
## SIP mode

# Process options
FLAGS=""

# Pass along any arguments to UCVM
while getopts 'm:p:c:f:z:bl:I:O:' OPTION
do
  if [ "$OPTION" == "O" ]; then
      OUT=$OPTARG
  elif [ "$OPTION" == "I" ]; then
      IN=$OPTARG
  elif [ "$OPTARG" != "" ]; then
      FLAGS="${FLAGS} -$OPTION $OPTARG"
  else
      FLAGS="${FLAGS} -$OPTION"
  fi
done
shift $(($OPTIND - 1))

SCRIPT_DIR="$( cd "$( dirname "$0" )" && pwd )"

## need to add path to cvmsi(cvms426)
export LD_LIBRARY_PATH=${SCRIPT_DIR}/../lib/euclid3/lib:${SCRIPT_DIR}/../lib/proj-5/lib:${SCRIPT_DIR}/../model/cvms426/lib
export DYLD_LIBRARY_PATH=${SCRIPT_DIR}/../lib/euclid3/lib:${SCRIPT_DIR}/../lib/proj-5/lib:${SCRIPT_DIR}/../model/cvms426/lib

if [ "$IN" != "" ]; then
  if [ "$OUT" != "" ]; then
      ${SCRIPT_DIR}/ucvm_query ${FLAGS} < $IN 1 >> $OUT 2>/dev/null 
  else
      ${SCRIPT_DIR}/ucvm_query ${FLAGS} < $IN
  fi
else
      ${SCRIPT_DIR}/ucvm_query ${FLAGS} 
fi


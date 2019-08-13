#!/bin/bash

## this is to run the ucvm_query with proper LD_LIBRARY_PATH and
## DYLD_LIBRARY_PATH that mac os seems to like to eliminate under
## SIP mode

# Process options
FLAGS=""

# Pass along any arguments to UCVM
while getopts 'm:p:c:f:z:bl:' OPTION
do
  if [ "$OPTARG" != "" ]; then
      FLAGS="${FLAGS} -$OPTION $OPTARG"
  else
      FLAGS="${FLAGS} -$OPTION"
  fi
done
shift $(($OPTIND - 1))

SCRIPT_DIR="$( cd "$( dirname "$0" )" && pwd )"

export LD_LIBRARY_PATH=${SCRIPT_DIR}/../lib/euclid3/lib:${SCRIPT_DIR}/../lib/proj-5/lib
export DYLD_LIBRARY_PATH=${SCRIPT_DIR}/../lib/euclid3/lib:${SCRIPT_DIR}/../lib/proj-5/lib

${SCRIPT_DIR}/ucvm_query ${FLAGS} 
if [ $? -ne 0 ]; then
    exit 1
fi

exit 0

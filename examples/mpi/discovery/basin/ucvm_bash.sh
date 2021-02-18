## 
##  models: [ CVM-S4 CVM-S4.26 CVM-S4.26.M01 CVM-H CenCalVM ]
##  libraries: [ Euclid3 Proj4 FFTW ]
## 

export UCVM_SRC_PATH=/project/scec_608/mei/ucvm_19_4/UCVM
export UCVM_INSTALL_PATH=/project/scec_608/mei/ucvm_19_4/UCVM_TARGET

function _add2PATH() {
  if [ "$PATH" ] ; then
    if ! echo "$PATH" | /usr/bin/grep -Eq "(^|:)$1($|:)" ; then
      if [ "$2" = "after" ] ; then
        export PATH="$PATH:$1"
      else
          export PATH="$1:$PATH"
      fi
    fi
    else
       export PATH="$1"
  fi
}

function _add2LD_LIBRARY_PATH() {
  if [ "$LD_LIBRARY_PATH" ] ; then
    if ! echo "$LD_LIBRARY_PATH" | /usr/bin/grep -Eq "(^|:)$1($|:)" ; then
      if [ "$2" = "after" ] ; then
        export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:$1"
      else
          export LD_LIBRARY_PATH="$1:$LD_LIBRARY_PATH"
      fi
    fi
    else
       export LD_LIBRARY_PATH="$1"
  fi
}

function _add2DYLD_LIBRARY_PATH() {
  if [ "$DYLD_LIBRARY_PATH" ] ; then
    if ! echo "$DYLD_LIBRARY_PATH" | /usr/bin/grep -Eq "(^|:)$1($|:)" ; then
      if [ "$2" = "after" ] ; then
        export DYLD_LIBRARY_PATH="$DYLD_LIBRARY_PATH:$1"
      else
          export DYLD_LIBRARY_PATH="$1:$DYLD_LIBRARY_PATH"
      fi
    fi
    else
       export DYLD_LIBRARY_PATH="$1"
  fi
}

function _add2PYTHONPATH() {
  if [ "$PYTHONPATH" ] ; then
    if ! echo "$PYTHONPATH" | /usr/bin/grep -Eq "(^|:)$1($|:)" ; then
      if [ "$2" = "after" ] ; then
        export PYTHONPATH="$PYTHONPATH:$1"
      else
          export PYTHONPATH="$1:$PYTHONPATH"
      fi
    fi
    else
       export PYTHONPATH="$1"
  fi
}

_add2LD_LIBRARY_PATH ${UCVM_INSTALL_PATH}/lib/euclid3/lib
_add2DYLD_LIBRARY_PATH ${UCVM_INSTALL_PATH}/lib/euclid3/lib
_add2LD_LIBRARY_PATH ${UCVM_INSTALL_PATH}/lib/proj-5/lib
_add2DYLD_LIBRARY_PATH ${UCVM_INSTALL_PATH}/lib/proj-5/lib
_add2LD_LIBRARY_PATH ${UCVM_INSTALL_PATH}/model/cvmh1511/lib
_add2DYLD_LIBRARY_PATH ${UCVM_INSTALL_PATH}/model/cvmh1511/lib
_add2LD_LIBRARY_PATH ${UCVM_INSTALL_PATH}/model/cvms/lib
_add2DYLD_LIBRARY_PATH ${UCVM_INSTALL_PATH}/model/cvms/lib
_add2LD_LIBRARY_PATH ${UCVM_INSTALL_PATH}/model/cvms5/lib
_add2DYLD_LIBRARY_PATH ${UCVM_INSTALL_PATH}/model/cvms5/lib
_add2LD_LIBRARY_PATH ${UCVM_INSTALL_PATH}/model/cvms426/lib
_add2DYLD_LIBRARY_PATH ${UCVM_INSTALL_PATH}/model/cvms426/lib
_add2LD_LIBRARY_PATH ${UCVM_INSTALL_PATH}/model/cencal/lib
_add2DYLD_LIBRARY_PATH ${UCVM_INSTALL_PATH}/model/cencal/lib
_add2PYTHONPATH ${UCVM_INSTALL_PATH}/utilities/pycvm
_add2PATH ${UCVM_INSTALL_PATH}/bin
_add2PATH ${UCVM_INSTALL_PATH}/utilities

# GNU Automake config

# Customizes ucvm.conf with configured models.

EXTRA_DIST = ucvm_template.conf

CHANGE_LIST=ucvm.conf

# USGS CenCalVM config
if UCVM_AM_ENABLE_CENCAL
CHANGE_LIST += cencal_model cencal_extmodel
endif

# CVM-H config
if UCVM_AM_ENABLE_CVMH
CHANGE_LIST += cvmh_model
endif

# CVM-S config
if UCVM_AM_ENABLE_CVMS
CHANGE_LIST += cvms_model
endif

# CVM-SI config
if UCVM_AM_ENABLE_CVMSI
CHANGE_LIST += cvmsi_model
endif

# SED Command
if USER_MAC
SED = sed -i ''
endif

if USER_LINUX
SED = sed -i''
endif

.PHONY=cencal_model cencal_extmodel cvmh_model \
	cvms_model cvmsi_model cvmnci_model \
	wfcvm_model cvmlt_model cmrg_model

all: ${CHANGE_LIST}

ucvm.conf: ucvm_template.conf
	cp $^ $@
	${SED} "s,PREFIX,${prefix},g" $@

cencal_model: ucvm.conf
	${SED} "s,#cencal_modelpath,cencal_modelpath,g" $^
	${SED} "s,CENCAL_MODEL,${CENCAL_MODEL},g" $^

cencal_extmodel: ucvm.conf
	${SED} "s,#cencal_extmodelpath,cencal_extmodelpath,g" $^
	${SED} "s,CENCAL_EXTMODEL,${CENCAL_EXTMODEL},g" $^

cvmh_model: ucvm.conf
	${SED} "s,#cvmh_modelpath,cvmh_modelpath,g" $^
	${SED} "s,CVMH_MODEL,${CVMH_MODEL},g" $^

cvms_model: ucvm.conf
	${SED} "s,#cvms_modelpath,cvms_modelpath,g" $^
	${SED} "s,CVMS_MODEL,${CVMS_MODEL},g" $^

cvmsi_model: ucvm.conf
	${SED} "s,#cvmsi_modelpath,cvmsi_modelpath,g" $^
	${SED} "s,CVMSI_MODEL,${CVMSI_MODEL},g" $^

install:
	mkdir -p ${prefix}/conf
	if ! test . -ef ${prefix}/conf; then \
                cp ucvm.conf ${prefix}/conf; \
        fi

clean:
	rm -rf ucvm.conf

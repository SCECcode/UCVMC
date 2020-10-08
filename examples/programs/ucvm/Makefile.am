# Autoconf/Automake binaries and headers
#
#
bin_PROGRAMS=

if UCVM_AM_ENABLE_CVMH
bin_PROGRAMS += run_ucvm_query_cvmh.sh
run_ucvm_query_cvmh_sh_SOURCES = run_ucvm_query_cvmh.sh
endif

if UCVM_AM_ENABLE_CENCAL && UCVM_AM_ENABLE_CVMS5
bin_PROGRAMS += run_ucvm_query_cencal_cvms5.sh
run_ucvm_query_cencal_cvms5_sh_SOURCES = run_ucvm_query_cencal_cvms5.sh
endif

if UCVM_AM_ENABLE_CENCAL && UCVM_AM_ENABLE_CVMS
bin_PROGRAMS += run_ucvm_query_cencal_cvms.sh
run_ucvm_query_cencal_cvms_sh_SOURCES = run_ucvm_query_cencal_cvms.sh
endif

run_ucvm_query_cvmh.sh:
run_ucvm_query_cencal_cvms5.sh:
run_ucvm_query_cencal_cvms.sh:

all: $(bin_PROGRAMS)
############################################
# Special build targets
############################################
check: $(bin_PROGRAMS)
	@for i in $(bin_PROGRAMS); do \
	  ./$${i}; \
	done

clean: 
	rm -f *.o *~



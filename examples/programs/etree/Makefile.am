# Autoconf/Automake binaries and headers
#
#
bin_PROGRAMS=

if UCVM_AM_ENABLE_CVMH
bin_PROGRAMS += run_ucvm2etree_cvmh.sh
run_ucvm2etree_cvmh_sh_SOURCES = run_ucvm2etree_cvmh.sh
endif

run_ucvm2etree_cvmh.sh:

all: $(bin_PROGRAMS)
############################################
# Special build targets
############################################
check: $(bin_PROGRAMS)
	@for i in $(bin_PROGRAMS); do \
		${prefix}/examples/programs/etree/$${i}; \
	done

clean: 
	rm -f *.o *~ *.conf *.e *.conf *.out



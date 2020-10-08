# Autoconf/Automake binaries and headers
#
#
bin_PROGRAMS=

# CVM-H includes
if UCVM_AM_ENABLE_CVMH
bin_PROGRAMS += run_basin_query_cvmh.sh
run_basin_query_cvmh_sh_SOURCES = run_basin_query_cvmh.sh
endif
run_basin_query_cvmh.sh:

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



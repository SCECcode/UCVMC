# Autoconf/Automake binaries and headers
#
#

# CVM-H includes
if UCVM_AM_ENABLE_CVMH
bin_PROGRAMS += run_basin_query_cvmh.sh
endif


############################################
# Special build targets
############################################

check: $(bin_PROGRAMS)
	@for i in $(bin_PROGRAMS); do \
	  ./$${i}; \
	done

clean: 
	rm -f *.o *~



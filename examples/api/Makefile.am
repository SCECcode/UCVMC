# Autoconf/Automake binaries and headers
#
#
noinst_PROGRAMS = query_1d_gtl
query_1d_gtl_SOURCES = *.c

# General compiler/linker flags
AM_CFLAGS = -I../../src/ucvm
AM_LDFLAGS = -L../../src/ucvm -lucvm $(LDFLAGS)

bin_PROGRAMS = query_1d_gtl

############################################
# Executables
############################################

query_1d_gtl: query_1d_gtl.o 
	$(CC) -o $@ $^ $(AM_LDFLAGS)


############################################
# Special build targets
############################################

check: $(bin_PROGRAMS)
	( cd ${prefix}/tests/api; \
	for i in $(bin_PROGRAMS); do \
		./run_$${i}.sh; \
	done
	)

install: $(bin_PROGRAMS)
	mkdir -p ${prefix}/tests/api
	@for i in $(bin_PROGRAMS); do \
		cp ${prefix}/tests/api/run_$${i}.sh ${prefix}/tests/api; \
		cp ${prefix}/tests/api/$${i} ${prefix}/tests/api; \
        done

clean: 
	rm -f *.o *~ $(noinst_PROGRAMS)



# Autoconf/Automake binaries and headers

LIST = query_1d_gtl

# General compiler/linker flags
AM_CFLAGS = -I../../src/ucvm
AM_LDFLAGS = -L../../src/ucvm -lucvm $(LDFLAGS)


############################################
# Executables
############################################

query_1d_gtl: query_1d_gtl.o 
	$(CC) -o $@ $^ $(AM_LDFLAGS)


############################################
# Special build targets
############################################

check: $(LIST)
	@for i in $(LIST); do \
	  ./run_$${i}; \
	done

clean: 
	rm -f *.o *~ $(noinst_PROGRAMS)



# Autoconf/Automake binaries and headers

inst_PROGRAMS = query_1d_gtl
query_1d_gtl_SOURCES = *.c

# General compiler/linker flags
AM_CFLAGS = -I../../src/ucvm
AM_LDFLAGS = -L../../src/ucvm -lucvm $(LDFLAGS)

all: $(inst_PROGRAMS)


############################################
# Executables
############################################

query_1d_gtl: query_1d_gtl.o 
	$(CC) -o $@ $^ $(AM_LDFLAGS)


############################################
# Special build targets
############################################

clean: 
	rm -f *.o *~ $(inst_PROGRAMS)



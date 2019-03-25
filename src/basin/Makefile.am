# Autoconf/Automake binaries and headers

bin_PROGRAMS = basin_query

if UCVM_HAVE_MPI
bin_PROGRAMS += basin_query_mpi
bin_PROGRAMS += basin_query_mpi_complete
endif

# General compiler/linker flags
AM_CFLAGS = -I../ucvm
AM_LDFLAGS = -L../ucvm -lucvm ${LDFLAGS}

if UCVM_HAVE_MPI
AM_CFLAGS += -DUM_ENABLE_MPI
endif

# Dist sources
basin_query_SOURCES = basin_query.c

if UCVM_HAVE_MPI
basin_query_mpi_SOURCES = basin_query_mpi.c
basin_query_mpi_complete_SOURCES = basin_query_mpi_complete.c
endif

all: $(bin_PROGRAMS)


############################################
# Executables
############################################

basin_query: basin_query.o
	$(CC) -o $@ $^ $(AM_LDFLAGS)

basin_query_mpi: basin_query_mpi.o
	$(CC) -o $@ $^ $(AM_LDFLAGS)

basin_query_mpi_complete: basin_query_mpi_complete.o
	$(CC) -o $@ $^ $(AM_LDFLAGS)

############################################
# Special build targets
############################################

clean:
	rm -f core *.o *~ $(bin_PROGRAMS)

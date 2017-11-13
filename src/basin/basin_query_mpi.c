/**
 * basin_query_mpi.c - Query UCVM for basin depths in parallel.
 *
 * Created by David Gill <davidgil@usc.edu>
 *
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <getopt.h>
#include <mpi.h>
#include "ucvm.h"
#include "ucvm_utils.h"

/* Constants */
#define MAX_RES_LEN 256
#define DEFAULT_ZRANGE_MIN 0.0
#define DEFAULT_ZRANGE_MAX 350.0
#define DEFAULT_MAX_DEPTH 15000.0
#define DEFAULT_NULL_DEPTH -1.0 
#define DEFAULT_ZERO_DEPTH 0.0 
#define DEFAULT_Z_INTERVAL 20.0
#define DEFAULT_VS_THRESH 1000.0

#define OUTPUT_FMT "%10.4lf %10.4lf %10.3lf %10.3lf\n"

#define WORKERREADY 99
#define DIEOFF -1

#define DEFAULT_MAX_FILE_LEN 512
#define DEFAULT_MAX_FILELIST_LEN 1024
#define DEFAULT_FILES_DELIM ","
#define DEFAULT_MAX_FILES 2

// to hold 4 floats and couple of comma and CRLF
#define DEFAULT_MAX_ENTRY_LEN  64

/* Get opt args */
extern char *optarg;
extern int optind, opterr, optopt;

/* Display usage information */
void usage() {
	printf("Usage: basin_query_mpi [-h] [-b outfile] [-m models<:ifunc>] [-f config] [-d max_depth] [-i inter] ");
	printf("[-v vs_thresh] [-l lat,lon] [-s spacing] [-x num lon pts] [-y num lat pts]\n\n");
	printf("where:\n");
	printf("\t-b Binary output to file.\n");
	printf("\t-h This help message\n");
	printf("\t-f Configuration file. Default is ./ucvm.conf.\n");
	printf("\t-i Interval between query points along z-axis (m, default is 20.0)\n");
	printf("\t-m Comma delimited list of crustal/GTL models to query in order\n");
	printf("\t-v Vs threshold (m/s, default is 1000.0).\n");
	printf("\t-l Bottom-left lat,lon separated by comma.\n");
	printf("\t-s Grid spacing.\n");
	printf("\t-x Number of longitude points.\n");
	printf("\t-y Number of latitude points.\n");
	printf("Notes:\n");
	printf("\t- If running interactively, type Cntl-D to end input coord list.\n\n");
	printf("Version: %s\n\n", VERSION);
	return;
}

/* Extract basin values for the specified point */
int extract_basin_mpi(ucvm_point_t *pnt, double *depths, double max_depth, double z_inter, double vs_thresh) {

	int j, numz;
	double vs_prev;

	numz = (int) (max_depth / z_inter);

	ucvm_point_t *qpnts = malloc(numz * sizeof(ucvm_point_t));
	ucvm_data_t *qprops = malloc(numz * sizeof(ucvm_data_t));

	for (j = 0; j < numz; j++) {
		qpnts[j].coord[0] = pnt[0].coord[0];
		qpnts[j].coord[1] = pnt[0].coord[1];
		qpnts[j].coord[2] = (double) j * z_inter;
	}

	/* Query the UCVM */
	if (ucvm_query(numz, qpnts, qprops) != UCVM_CODE_SUCCESS) {
		fprintf(stderr, "Query CVM failed\n");
		return (1);
	}

//  initialize to something
        depths[0]= DEFAULT_NULL_DEPTH;
        depths[1]= DEFAULT_NULL_DEPTH;
	vs_prev = DEFAULT_ZERO_DEPTH;
	for (j = 0; j < numz; j++) {
                // must be a valid depth
		if (qprops[j].cmb.vs > DEFAULT_ZERO_DEPTH) {
			if(vs_prev < vs_thresh &&
					(qprops[j].cmb.vs >= vs_thresh)) {
				// found a crossing point
				if(depths[0]==DEFAULT_NULL_DEPTH) {
					depths[0] = (double) j * z_inter;
					depths[1] = depths[0]; // preset last equals to first
					} else {
						depths[1] = (double) j * z_inter;
				}
			}
			vs_prev = qprops[j].cmb.vs;
		}
	}

	free(qprops);
	free(qpnts);
	return(0);
}

/* parse filename list */
/*   first.file
     first.file,
     ,last.file
     first.file,last.file
*/
int parse_file_list(const char *list, char **files) {
  char filesstr[DEFAULT_MAX_FILELIST_LEN];
  char *token;
  int i;
  int num_files = 0;

  /* initialize the files. */
  for( i=0 ; i < DEFAULT_MAX_FILES ; i++) {
    files[i]=malloc(DEFAULT_MAX_FILE_LEN * sizeof(char));
    strcpy(files[i], "");
  }
  if(strlen(list) == 0) {
      fprintf(stderr, "Did not specify result files\n");
      return(UCVM_CODE_ERROR);
  }

  strcpy(filesstr, list);

  /* special case, when first file is empty */
  if(filesstr[0]==',') {
    num_files++;
  }

  token = strtok(filesstr, DEFAULT_FILES_DELIM);
  while (token != NULL) {
    if (num_files == DEFAULT_MAX_FILES) {
      fprintf(stderr, "Max number of output file reached\n");
      return(UCVM_CODE_ERROR);
    }

    if(strlen(token) != 0) {
      strcpy(files[num_files], token);
    }

    num_files++;
    token = strtok(NULL, DEFAULT_FILES_DELIM);
  }

  printf("number of files.. %d\n", num_files);
  printf("first file (%s)\n", files[0]);
  if(num_files>1)
    printf("second file (%s)\n", files[1]);

  return (0);
}


int main(int argc, char **argv) {
	int opt;
	char modellist[UCVM_MAX_MODELLIST_LEN];
	char configfile[UCVM_MAX_PATH_LEN];
	double max_depth;
	double z_inter;
	double vs_thresh;
	double latlon[2];
	int nx = 0;
	int ny = 0;
	int currentline = 0;	// Current line we're working on.
	double spacing = 0;

	ucvm_ctype_t cmode;
	int have_model = 0;
	int have_map = 0;

	char map_label[UCVM_MAX_LABEL_LEN];

        char *binary_outfiles[DEFAULT_MAX_FILES];
        char *ascii_outfile;

	int numprocs, rank, i;

	MPI_Init(&argc, &argv);
	MPI_Comm_size(MPI_COMM_WORLD, &numprocs);
	MPI_Comm_rank(MPI_COMM_WORLD, &rank);

	cmode = UCVM_COORD_GEO_DEPTH;
	snprintf(configfile, UCVM_MAX_PATH_LEN, "%s", "./ucvm.conf");
	snprintf(modellist, UCVM_MAX_MODELLIST_LEN, "%s", "1d");
	snprintf(map_label, UCVM_MAX_LABEL_LEN, "%s", UCVM_MAP_UCVM);
	max_depth = DEFAULT_MAX_DEPTH;
	z_inter = DEFAULT_Z_INTERVAL;
	vs_thresh = DEFAULT_VS_THRESH;
        // initialize the result file names to null strings
	for( i=0 ; i < DEFAULT_MAX_FILES ; i++ ) {
          binary_outfiles[i] = "";
        }
        ascii_outfile = "";

	/* Parse options */
	while ((opt = getopt(argc, argv, "hb:o:m:f:d:i:v:l:s:x:y:")) != -1) {
		switch (opt) {
		case 'h':
			usage();
			exit(0);
			break;
		case 'b':
                        parse_file_list(optarg,binary_outfiles);
			break;
		case 'o':
                        ascii_outfile=optarg;
			break;
		case 'm':
			if (strlen(optarg) >= UCVM_MAX_MODELLIST_LEN - 1) {
				fprintf(stderr, "Model list is too long.\n");
				usage();
				exit(1);
			} else {
				snprintf(modellist, UCVM_MAX_MODELLIST_LEN, "%s", optarg);
				have_model = 1;
			}
			break;
		case 'f':
			if (strlen(optarg) < UCVM_MAX_PATH_LEN) {
				snprintf(configfile, UCVM_MAX_PATH_LEN, "%s", optarg);
			} else {
				fprintf(stderr, "Invalid config file specified: %s.\n", optarg);
				usage();
				exit(1);
			}
			break;
		case 'd':
			max_depth = (double) atof(optarg);
			if (max_depth <= 0.0) {
				fprintf(stderr, "Invalid max depth %s.\n", optarg);
				usage();
				exit(1);
			}
			break;
		case 'i':
			z_inter = (double) atof(optarg);
			if (z_inter <= 0.0) {
				fprintf(stderr, "Invalid z interval %s.\n", optarg);
				usage();
				exit(1);
			}
			break;
		case 'v':
			vs_thresh = (double) atof(optarg);
			if (vs_thresh <= 0.0) {
				fprintf(stderr, "Invalid vs threshold %s.\n", optarg);
				usage();
				exit(1);
			}
			break;
		case 'l':
			if (list_parse(optarg, UCVM_MAX_PATH_LEN,
					       latlon, 2) != UCVM_CODE_SUCCESS) {
				fprintf(stderr, "Invalid lat, lon range specified: %s.\n", optarg);
				usage();
				exit(1);
			}
			break;
		case 's':
			spacing = (double) atof(optarg);
			if (spacing <= 0.0) {
				fprintf(stderr, "Invalid spacing %s", optarg);
				usage();
				exit(1);
			}
			break;
		case 'x':
			nx = (int) atoi(optarg);
			if (nx <= 0) {
				fprintf(stderr, "Invalid number of x points %s", optarg);
				usage();
				exit(1);
			}
			break;
		case 'y':
			ny = (int) atoi(optarg);
			if (ny <= 0) {
				fprintf(stderr, "Invalid number of x points %s", optarg);
				usage();
				exit(1);
			}
			break;
		default: /* '?' */
			usage();
			exit(1);
		}
	}

	/* Initialize interface */
	if (ucvm_init(configfile) != UCVM_CODE_SUCCESS) {
		fprintf(stderr, "Failed to initialize UCVM API\n");
		return (1);
	}

	/* Add models */
	if (have_model == 0) {
		/* Add default model if none specified */
		fprintf(stderr, "Using 1D as default model.\n");
	}
	if (ucvm_add_model_list(modellist) != UCVM_CODE_SUCCESS) {
		fprintf(stderr, "Failed to enable model list %s\n", modellist);
		return (1);
	}

	/* Set user map if necessary */
	if (have_map == 1) {
		if (ucvm_use_map(map_label) != UCVM_CODE_SUCCESS) {
			fprintf(stderr, "Failed to set user map %s\n", map_label);
			return (1);
		}
	}

	/* Set z mode for depth*/
	if (ucvm_setparam(UCVM_PARAM_QUERY_MODE, cmode) != UCVM_CODE_SUCCESS) {
		fprintf(stderr, "Failed to set z mode\n");
		return (1);
	}

	MPI_Barrier(MPI_COMM_WORLD);

        MPI_File bfh[DEFAULT_MAX_FILES];
        MPI_File afh; 

        /* setup result file handler */
	for( i=0 ; i < DEFAULT_MAX_FILES ; i++ ) {
		if(strlen(binary_outfiles[i]) > 0) { 
			MPI_File_open(MPI_COMM_SELF, binary_outfiles[i], MPI_MODE_CREATE | MPI_MODE_WRONLY, MPI_INFO_NULL, &bfh[i]);
			} else {
				bfh[i]=NULL;
		}
	}
        if(strlen(ascii_outfile) > 0) { 
		MPI_File_open(MPI_COMM_SELF, ascii_outfile, MPI_MODE_CREATE | MPI_MODE_WRONLY, MPI_INFO_NULL, &afh);
		} else {
			afh=NULL;
	}

	// We divide the job up in terms of lines (i.e. ny).
	currentline = rank;

	while (currentline < ny) {
printf(" YYY mpi(%d)  == line(%d)\n",rank, currentline);
		ucvm_point_t *pnts = malloc(sizeof(ucvm_point_t));
		double tempDepths[2];
		float *retDepths = malloc(nx * sizeof(float));
		float *retLastDepths = malloc(nx * sizeof(float));
                char *retLiteral= malloc(DEFAULT_MAX_ENTRY_LEN * sizeof(char));

		printf("Current line: %d. Progress: %.2f\%\n", currentline, (float)currentline / (float)ny * 100.0f);

		for (i = 0; i < nx; i++) {
                        // pnts.coord's format is coord[0] is the lon, ccord[1] is the lat
			pnts[0].coord[1] = (currentline * spacing) + latlon[0];
			pnts[0].coord[0] = (i * spacing) + latlon[1];

			extract_basin_mpi(pnts, tempDepths, max_depth, z_inter, vs_thresh);

			retDepths[i] = (float)tempDepths[0];
			retLastDepths[i] = (float)tempDepths[1];
// XXX write out ascii 
#define DEFAULT_MAX_ENTRY_LEN  64
			if(afh != NULL) {
				snprintf(retLiteral, DEFAULT_MAX_ENTRY_LEN, "%f %f %f %f\n", pnts[0].coord[0], pnts[0].coord[1], retDepths[i], retLastDepths[i]);
				MPI_File_write(afh, retLiteral, strlen(retLiteral), MPI_CHAR, MPI_STATUS_IGNORE);
                       }

// MEI, ORIGINAL

			//printf("%f %f %f %d\n", pnts[0].coord[0], pnts[0].coord[1], retDepths[i], rank);
			//if (rank == 0) {
				//printf("On index: %d\n", i);
			//}

		}

                if(bfh[0] != NULL) {
		  MPI_File_set_view(bfh[0], currentline * nx * sizeof(float), MPI_FLOAT, MPI_FLOAT, "native", MPI_INFO_NULL);
		  MPI_File_write(bfh[0], /*currentline * nx * sizeof(float),*/ retDepths, nx, MPI_FLOAT, MPI_STATUS_IGNORE);
                }
                if(bfh[1] != NULL) {
		  MPI_File_set_view(bfh[1], currentline * nx * sizeof(float), MPI_FLOAT, MPI_FLOAT, "native", MPI_INFO_NULL);
		  MPI_File_write(bfh[1], /*currentline * nx * sizeof(float),*/ retLastDepths, nx, MPI_FLOAT, MPI_STATUS_IGNORE);
                }

		//free(pnts);
		//free(tempDepths);
		free(retDepths);
		free(retLastDepths);
                free(retLiteral);

		currentline += numprocs;

	}

	ucvm_finalize();

	MPI_Barrier(MPI_COMM_WORLD);

	if(bfh[0] != NULL) {
		MPI_File_close(&bfh[0]);
	}
	if(bfh[1] != NULL) {
		MPI_File_close(&bfh[0]);
	}
        if(afh != NULL) {
		MPI_File_close(&afh);
	}

	MPI_Finalize();

	return (0);
}

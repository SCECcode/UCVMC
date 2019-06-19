/**
 ** ucvm_crossing.c - Query UCVM for basin depths with threshold
 **
 ** based on basin_query.c
 **
 **/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "ucvm.h"
#include "ucvm_utils.h"
#include "ucvm_crossing.h"

int *ucvm_crossings;

/* Extract basin values for the specified points */
double ucvm_extract_basins(int n, ucvm_point_t *pnts, \
		   ucvm_point_t *qpnts, ucvm_data_t *qprops, \
		   double max_depth, double z_inter, double vs_thresh, \
                   ucvm_ctype_t cmode)
{
  int i, p, dnum, numz;
  double vs_prev;
  double depths[3];
  depths[0] = DEFAULT_NULL_DEPTH;
  depths[1] = DEFAULT_NULL_DEPTH;
  depths[2] = DEFAULT_NULL_DEPTH;
  
  numz = (int)(max_depth / z_inter);
  for (p = 0; p < n; p++) {
    /* Setup query points */
    for (i = 0; i < numz; i++) {
      qpnts[i].coord[0] = pnts[p].coord[0];
      qpnts[i].coord[1] = pnts[p].coord[1];
      // this is for 'depth'
      if(cmode == UCVM_COORD_GEO_DEPTH) {
              qpnts[i].coord[2] = (double)i * z_inter;
          } else {
//??? would thought that this should be elevation - 'depth' but ucvm.c seems
// to show the surf - depth and surf is initialize to 0
              qpnts[i].coord[2] = 0 - ((double)(i) * z_inter);
      }
    }
    /* Query the UCVM */
    if (ucvm_query(numz, qpnts, qprops) != UCVM_CODE_SUCCESS) {
      fprintf(stderr, "Query CVM failed\n");
      return(1);
    }
  
    /* Check for threshold crossing */
    vs_prev = DEFAULT_ZERO_DEPTH;
    dnum = 0;
    depths[0] = DEFAULT_NULL_DEPTH;
    depths[1] = DEFAULT_NULL_DEPTH;
    depths[2] = DEFAULT_NULL_DEPTH;
    for (i = 0; i < numz; i++) {
      /* Compare the Vs if it is valid */
      if (qprops[i].cmb.vs > DEFAULT_ZERO_DEPTH) {
	  if ((vs_prev < vs_thresh) && (qprops[i].cmb.vs >= vs_thresh)) {
	    depths[dnum] = (double)i * z_inter;
	    if (dnum == 0) {
	      depths[2] = depths[1] = depths[0];
	      dnum++;
	      } else {
                if(dnum == 1) {
                   depths[2] = depths[1];
                   dnum++;
                }
            }
      
	  }

	  /* Save current vs value */
          vs_prev = qprops[i].cmb.vs;
      }
    }

  /* Display output */
//    fprintf(stderr, "#%10.4lf %10.4lf %10.3lf %10.3lf %10.3lf\n" , pnts[p].coord[0], pnts[p].coord[1], depths[0], depths[1], depths[2]);

    }
  
    if (depths[0] == DEFAULT_NULL_DEPTH) {
      return (-1);
    }
    return depths[0];
}


int ucvm_first_crossing(ucvm_point_t *pnts, ucvm_ctype_t cmode, double vs_thresh) {

// variable, all locally defined
  ucvm_point_t *qpnts;
  ucvm_data_t *qprops;

  double max_depth = DEFAULT_MAX_DEPTH;
  double z_inter = DEFAULT_Z_INTERVAL;

  /* Allocate buffers */
  qpnts = malloc((int)(max_depth/z_inter+1) * sizeof(ucvm_data_t));
  qprops = malloc((int)(max_depth/z_inter+1) * sizeof(ucvm_data_t));

  int crossing=ucvm_extract_basins(1, pnts, qpnts, qprops, 
			   max_depth, z_inter, vs_thresh, cmode);

  free(qpnts);
  free(qprops);

  if( crossing == DEFAULT_NULL_DEPTH ) {
      fprintf(stderr, "Crossing retrieval failed\n");
      return(0);
  }
  return crossing;
}

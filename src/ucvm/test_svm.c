
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "ucvm.h"

//  test_svm data.in
int main(int argc, char **argv)
{
  int i;
  int nn;
  ucvm_point_t *pnt1;
  ucvm_data_t *prop1;
  File *fptr;
  int numread = 0;
  char *data_in;
  char data_out[100];

  if(argc != 3) {
     printf("Usage:  test_svm cnt data_file");
     return(1);
  }
  sscanf(argv[1],"%d", &nn);

  data_in=argv[2];
  sprintf(data_out,"%s_out",data_in);

  fptr=fopen(data_in, "r");
  if(fptr == NULL) {
     printf("Can not open %s\n", argv[1]);
     return(1);
  }

  pnt1 = malloc(nn * sizeof(ucvm_point_t));
  prop1 = malloc(nn * sizeof(ucvm_data_t));
  char gtl_label[UCVM_MAX_LABEL_LEN];
  char cr_label[UCVM_MAX_LABEL_LEN];

  while(numread < nn) {
    if (fscanf(fptr,"%lf,%lf,%lf",
               &(pnt1[numread].coord[0]),
               &(pnt1[numread].coord[1]),
               &(pnt1[numread].coord[2])) == 3) {

      /* Check for scan failure */
      if ((pnt1[numread].coord[0] == 0.0) ||
          (pnt1[numread].coord[1] == 0.0)) {
        continue;
      }

      numread++;
    }
  }
  fclose(fptr);
    
  printf("Init\n");
  if (ucvm_init("../conf/ucvm.conf") != UCVM_CODE_SUCCESS) {
    fprintf(stderr, "Init failed\n");
    return(1);
  }
  
  printf("set Query Mode\n");
  ucvm_ctype_t cmode = UCVM_COORD_GEO_DEPTH; 
  if (ucvm_setparam(UCVM_PARAM_QUERY_MODE, cmode) != UCVM_CODE_SUCCESS) {
    fprintf(stderr, "Failed to set z mode\n");
    return(1);
  }

#ifdef _UCVM_ENABLE_CVMS5
  fprintf(stdout,"adding cvms5\n");
  if (ucvm_add_model("cvms5") != UCVM_CODE_SUCCESS) {
    fprintf(stderr, "Retrieval of CVMS5 failed\n");
    return(1);
  }
#endif
  
  printf("Query Models\n");
  if (ucvm_query(nn, pnt1, prop1) != UCVM_CODE_SUCCESS) {
    fprintf(stderr, "Query CVM failed\n");
    return(1);
  }
 
  printf("Results\n");
  for (i = 0; i < numread; i++) {
    ucvm_model_label(prop1[i].crust.source,
                           cr_label, UCVM_MAX_LABEL_LEN);
    ucvm_model_label(prop1[i].gtl.source,
                           gtl_label, UCVM_MAX_LABEL_LEN);
    printf("%d: model=%s, gtl=%s, vp=%lf, vs=%lf, rho=%lf\n", i, 
	   cr_label, gtl_label, prop1[i].cmb.vp, prop1[i].cmb.vs, prop1[i].cmb.rho);
  }

  ucvm_finalize();
  free(pnt1);
  free(prop1);

  return(0);
}

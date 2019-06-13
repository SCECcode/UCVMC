#ifndef UCVM_MODEL_SVMGTL_H
#define UCVM_MODEL_SVMGTL_H

#include <stdarg.h>
#include "ucvm_dtypes.h"


/* Init SVM */
int ucvm_svmgtl_model_init(int id, ucvm_modelconf_t *conf);


/* Finalize SVM */
int ucvm_svmgtl_model_finalize();


/* Version SVM */
int ucvm_svmgtl_model_version(int id, char *ver, int len);


/* Label SVM */
int ucvm_svmgtl_model_version(int id, char *lab, int len);


/* Setparam SVM */
int ucvm_svmgtl_model_setparam(int id, int param, ...);


/* Query SVM */
int ucvm_svmgtl_model_query(int id, ucvm_ctype_t cmode,
			 int n, ucvm_point_t *pnt, 
			 ucvm_data_t *data);


/* Fill model structure with SVM */
int ucvm_svmgtl_get_model(ucvm_model_t *m);


#endif

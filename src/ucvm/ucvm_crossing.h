
/* Constants */

#define DEFAULT_Z_INTERVAL 20.0
#define DEFAULT_VS_THRESH 1000.0
#define DEFAULT_NULL_DEPTH -1.0
#define DEFAULT_ZERO_DEPTH 0.0
#define DEFAULT_MAX_DEPTH 15000.0

extern int *ucvm_crossings;

int ucvm_first_crossing(ucvm_point_t *pnts, ucvm_ctype_t cmode, double vs_thresh);


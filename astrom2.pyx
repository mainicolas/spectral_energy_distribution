import cython

cdef extern from "c_astrom2.h":
	cpdef double to_jsky(float fmag, float mag)
	int search_vega_filter(char *system, char *filtername, float *Lambda, float *dlambda, float *fmag)


def search_vega_filter_py(system_py, filtername_py):
	system_bytes		= bytes(system_py, "UTF-8")
	filtername_bytes 	= bytes(filtername_py, "UTF-8")
	cdef char* system	= system_bytes
	cdef char* filtername 	= filtername_bytes

	cdef float lambda_temp, dlambda_temp, fmag_temp = 0. 
	cdef float *Lambda	= &lambda_temp
	cdef float *dlambda 	= &dlambda_temp
	cdef float *fmag 	= &fmag_temp

	search_vega_filter(system, filtername, Lambda, dlambda, fmag)
	return Lambda[0], dlambda[0], fmag[0]


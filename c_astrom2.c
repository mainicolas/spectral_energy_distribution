/**@file astrom2.c
   @author G.Landais 
   @date  oct 2022
   @brief M2 astro
*/

#include <stdio.h>
#include <math.h>
#include <stdlib.h>
#include <string.h>
#include "c_astrom2.h"

#define PI 3.1415926
#define radian(deg) (deg*PI/180)
#define MAX_CHAR_LINE 100



/*****************************************************************************/
/*  PHOTOMETRY                                                               */
/*****************************************************************************/

/*****************************************************************************/
/**@brief transform magniture into jsky
   @param fmag zero point
   @param mag magnitude
   @return magnitude in Jsky
*/
/*****************************************************************************/
double to_jsky(float fmag, float mag) {
    return  fmag*pow(10, -0.4*mag);
}

/*****************************************************************************/
/**@brief transform magniture into jsky
   @param system : system photometric
   @param filter : filter photometric
   @param mag magnitude
   @return magnitude in Jsky

   Note: not optimized
*/
/*****************************************************************************/
double system_to_jsky(char *system, char *filter, float mag) {
    float lambda, dlambda, fmag;
    if (search_vega_filter(system, filter, &lambda, &dlambda, &fmag) == 0)
        return NAN;

    return  fmag*pow(10, -0.4*mag);
}

struct phot_filter list_filter[] = {
{"Johnson","U",0.3531,0.0619,1810.0},
{"Johnson","B",0.4442,0.0891,4260.0},
{"Johnson","V",0.5537,0.0818,3640.0},
{"Johnson","R",0.6938,0.1943,2890.0},
{"Johnson","I",0.878,0.2176,2280.0},
{"Johnson","J",1.25,0.3,1610.0},
{"Johnson","H",1.63,0.2,1040.0},
{"Johnson","K",2.19,0.54,653.0},
{"Johnson","L",3.4,0.9,288.0},
{"Johnson","M",5.03,1.06,158.0},
{"Cousins","B",0.4425,0.0928,4260.0},
{"Cousins","V",0.5544,0.0843,3640.0},
{"Cousins","R",0.6469,0.1297,3080.0},
{"Cousins","I",0.7886,0.095,2550.0},
{"Landolt","B",0.4326,0.0792,3962.0},
{"Landolt","V",0.5445,0.0817,3688.0},
{"Landolt","R",0.6529,0.154,3195.0},
{"Landolt","I",0.8104,0.1242,2520.0},
{"BATC","a",0.3353,0.032,1810.0},
{"BATC","b",0.3899,0.0248,4260.0},
{"BATC","c",0.4195,0.0299,3640.0},
{"BATC","d",0.4537,0.0278,3080.0},
{"BATC","e",0.4923,0.0338,2550.0},
{"BATC","f",0.5264,0.0315,4260.0},
{"BATC","g",0.5784,0.0254,3640.0},
{"BATC","h",0.6074,0.0267,3080.0},
{"BATC","i",0.6649,0.044,2550.0},
{"BATC","j",0.7053,0.0215,1810.0},
{"BATC","k",0.7536,0.0191,1810.0},
{"BATC","m",0.8007,0.0246,4260.0},
{"BATC","n",0.8467,0.0156,3640.0},
{"BATC","o",0.9162,0.0224,3080.0},
{"BATC","p",0.9714,0.025,2550.0},
{"ALHAMBRA","A457M",0.4575,0.0332,4286.0},
{"ALHAMBRA","A613M",0.6134,0.032,3221.0},
{"ALHAMBRA","A892M",0.8918,0.0303,2291.0},
{"SDSS","u'",0.3519,0.0555,3680.0},
{"SDSS","g'",0.482,0.1245,3643.0},
{"SDSS","r'",0.6247,0.1262,3648.0},
{"SDSS","i'",0.7635,0.1291,3644.0},
{"SDSS","z'",0.9018,0.1326,3631.0},
{"SDSS","u",0.3519,0.0555,3676.0},
{"SDSS","g",0.482,0.1245,3640.0},
{"SDSS","r",0.6247,0.1262,3645.0},
{"SDSS","i",0.7635,0.1291,3641.0},
{"SDSS","z",0.9018,0.1326,3631.0},
{"2MASS","J",1.239,0.15,1577.0},
{"2MASS","H",1.65,0.24,1050.0},
{"2MASS","Ks",2.164,0.25,674.9},
{"DENIS","I",0.79,0.11,2499.0},
{"DENIS","J",1.24,0.19,1595.0},
{"DENIS","Ks",2.16,0.28,665.0}, 
{"UKIDSS","Z",0.8817,0.093,2232.0},
{"UKIDSS","Y",1.031,0.102,2026.0},
{"UKIDSS","J",1.248,0.159,1530.0},
{"UKIDSS","H",1.631,0.292,1019.0},
{"UKIDSS","K",2.201,0.351,631.0},
{"UKIRT/WFCAM","Z",0.8802,0.0926,2261.0},
{"UKIRT/WFCAM","J",1.249,0.1513,1549.0},
{"UKIRT/WFCAM","H",1.634,0.281,1027.0},
{"UKIRT/WFCAM","K",2.218,0.3251,630.0},
{"CFHT/UBVRI","B",0.4471,0.0842,4260.0},
{"CFHT/UBVRI","R",0.6475,0.09,3080.0},
{"CFHT/UBVRI","I",0.8333,0.0873,2550.0},
{"MKO","J",1.25,0.162,1560.0},
{"MKO","H",1.635,0.304,1050.0},
{"MKO","Ks",2.15,0.315,670.0},
{"MKO","L'",3.77,0.697,249.0},
{"MKO","M'",4.68,0.248,163.0},
{"MKO","K",2.2,0.1,645.0},
{"INT/WFC","U",0.3632,0.0618,1698.0},
{"INT/WFC","g",0.4781,0.1201,3928.0},
{"INT/WFC","r",0.6154,0.1219,3146.0},
{"INT/WFC","Ha",0.6568,0.0094,2610.0},
{"INT/WFC","i",0.7664,0.1471,2508.0},
{"INT/WFC","Z",0.8744,0.0421,2268.0},
{"CFHT/WIRCAM","Y",1.022,0.1084,2073.0},
{"CFHT/WIRCAM","H",1.616,0.2886,1044.0},
{"CFHT/WIRCAM","Ks",2.134,0.3209,674.6},
{"CFHT/WIRCAM","J",1.248,0.1548,1551.0},
{"EIS","B",0.4556,0.0905,4063.0},
{"EIS","V",0.5342,0.09,3636.0},
{"EIS","I",0.8535,0.1387,2416.0},
{"ISAAC","Ks",2.152,0.2719,665.8},
{"VISTA","Z",0.8762,0.0978,2264.0},
{"VISTA","Y",1.018,0.0905,2087.0},
{"VISTA","J",1.246,0.1628,1554.0},
{"VISTA","H",1.631,0.2833,1030.0},
{"VISTA","Ks",2.134,0.3055,674.8},
{"HAWK-I","J",1.252,0.1524,1544.0},
{"HAWK-I","H",1.605,0.2861,1054.0},
{"HAWK-I","Ks",2.132,0.315,675.3},
{"HST/ACS","F435W",0.4319,0.02934,4015.0},
{"HST/ACS","F475W",0.4747,0.04202,3993.0},
{"HST/ACS","F555W",0.5361,0.03601,3661.0},
{"HST/ACS","F606W",0.5921,0.06722,3357.0},
{"HST/ACS","F775W",0.7692,0.04344,2540.0},
{"HST/ACS","F814W",0.8057,0.06519,2458.0},
{"HST/ACS","F850LP",0.9033,0.05257,2250.0},
{"HST/HRC","F250W",0.2716,0.02394,919.2},
{"IRAS","12",11.59,5.69,28.3},
{"IRAS","25",23.88,9.41,6.73},
{"IRAS","60",61.85,28.58,1.19},
{"IRAS","100",101.9,30.62,0.43},
{"MSX","A",8.28,3.36,58.55},
{"MSX","C",12.13,1.72,58.55},
{"MSX","D",14.65,2.23,18.29},
{"MSX","E",21.34,6.24,8.75},
{"Spitzer/IRAC","3.6",3.55,0.749,280.0},
{"Spitzer/IRAC","4.5",4.493,1.02,179.7},
{"Spitzer/IRAC","5.8",5.731,1.421,115.0},
{"Spitzer/IRAC","8.0",7.872,2.881,64.13},
{"Spitzer/MIPS","24",23.67,9.13,7.14},
{"Spitzer/MIPS","70",71.42,19.5,0.775},
{"Spitzer/MIPS","160",155.9,48.4,0.159},
{"AKARI","S9W",8.61,4.1,56.26},
{"AKARI","L18W",18.39,9.97,12.0},
{"AKARI","N3",3.19,0.87,343.3},
{"AKARI","S7",7.12,1.75,74.96},
{"AKARI","S11",10.45,4.12,38.26},
{"AKARI","L15",15.58,5.98,16.03},
{"AKARI","L24",22.89,5.34,8.046},
{"ISO","LW2",6.81,2.59,90.2},
{"ISO","LW3",14.48,4.25,19.7},
{"WISE","W1",3.35,0.66,306.6},
{"WISE","W2",4.6,1.04,170.6},
{"WISE","W3",11.56,5.51,29.0},
{"WISE","W4",22.09,4.1,8.3},
{"HIP","BT",0.4203,0.0668,3943.0},
{"HIP","Hp",0.402,0.2208,3748.0},
{"HIP","VT",0.5319,0.0949,3761.0},
{"GALEX","FUV",0.1529,0.0269,3631.0},
{"GALEX","NUV",0.2312,0.0616,3631.0},
{"Gaia","G",0.673,0.44,3016.0},
{"XMM-OT","UVM2",0.2311,0.0705,802.0},
{"XMM-OT","UVW2",0.2119,0.0649,755.},
{"XMM-OT","UVW1",0.2908,0.1155,1035.},
{"XMM-OT","U",0.3441,0.086,1542.},
{"XMM-OT","B",0.4506,0.1095,4306.},
{"XMM-OT","V",0.543,0.085,3768.},
{NULL, NULL,0,0,0}
};

/*****************************************************************************/
/**@brief iterator on filter for a given system
   @param system (IN) the photometric system
   @param phot (IN/OUT) filter information updated by the function
   @return 1 found, O not found   
*/
/*****************************************************************************/
int next_filter(char *system, struct phot_filter *phot) {
    static struct phot_filter *ptr = NULL;
    static char system_ref[100];
    int found_system = 0;
    //int j;

    if (system != NULL)  {
        strcpy(system_ref, system);
        ptr = list_filter;
        for (; ptr->system!=NULL; ptr++) {
            if (strcmp(system, ptr->system) == 0) {
                found_system = 1;
                break;
            }
        }
        if (found_system == 0) return 0;
    }
    else {
        if (ptr == NULL) return 0;
    }
    
    if (ptr->system == NULL) return 0;
    if (strcmp(system_ref, ptr->system) != 0)
        return 0; /* not found */
  
    phot->system = ptr->system; 
    phot->filter =  ptr->filter;
    phot->lambda0 = ptr->lambda0;
    phot->dlambda = ptr->dlambda;
    phot->fmag = ptr->fmag;
    ptr++;
    

    return 1;
}

/*****************************************************************************/
/**@brief search a filter by system+filter_name
   @param system (IN) the system
   @param filtername (IN) the filter name
   @param lambda (OUT)  wavelength center  (in um) - updated by the function
   @param dlambda (OUT) wavelength size  (in um) - updated by the function
   @fmag Vega zero point - updated by the function
   @return 0 if nothing found
*/
/*****************************************************************************/
int search_vega_filter(char *system, char *filtername, float *lambda, float *dlambda, float *fmag) {
    struct phot_filter *ptr;
    int found_system = 0;
    if (system == NULL || filtername == NULL) return 0;

    for (ptr = list_filter; ptr->system!=NULL; ptr++) {
        if (strcmp(system, ptr->system) == 0) {
            found_system = 1;
            if (strcmp(filtername, ptr->filter) == 0) {
                *lambda = ptr->lambda0;
                *dlambda = ptr->dlambda;
                *fmag = ptr->fmag;
                return 1;
            }
            continue;
        }
        if (found_system == 1) return 0;
    }

    return 1;
}


/*****************************************************************************/
/* TEST functions                                                            */
/*****************************************************************************/


#ifdef __PHOTOMETRY_MAIN
int main(int argc, char **argv) {
    float lambda,err,fmag;
    if (argc < 2) {
        printf("Help: %s system [filter] [mag]\n", argv[0]);
        printf("ex: %s XMM-OT U 20.8973\n", argv[0]);
        printf("ex: %s XMM-OT\n", argv[0]);
        return 0;
    }

    if (argc < 3) {
        struct phot_filter phot;
        int ret= next_filter(argv[1], &phot);
        while (ret != 0) {
             printf("system %s, filter %s (lambda=%f, err=%f, fmag=%f)\n",
                    phot.system,
                    phot.filter,
                    phot.lambda0,
                    phot.dlambda,
                    phot.fmag);
             ret = next_filter(NULL, &phot);
        }
        return 0;
    }

    if (search_vega_filter(argv[1], argv[2], &lambda, &err, &fmag) == 1) {
        printf("found filter %s/%s: lambda=%f, dlambda=%f, fmag=%f\n", 
                argv[1], argv[2], lambda, err, fmag);
        if (argc == 4)
            printf("to_jsky()=%le\n", to_jsky(fmag, atof(argv[3])));
        return 1;
    }
    fprintf(stderr,"filter is not found\n");
    return 0;
}
#endif

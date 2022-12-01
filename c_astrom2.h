/**@file astrom2.h
   @author G.Landais 
   @brief M2 astro
   @date oct-2022
*/

#ifndef __ASTROM2_H
#define __ASTROM2_H

struct phot_filter {
    char *system;
    char *filter;
    float lambda0;
    float dlambda;
    float fmag;
};

double to_jsky(float, float) ;
double system_to_jsky(char *, char *, float);
int next_filter(char *, struct phot_filter *) ;
int search_vega_filter(char *, char *, float *, float *, float *);
#endif

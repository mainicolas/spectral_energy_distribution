import os, sys
path = os.getcwd()
sys.path.insert(1, path+'/class/')

from simbad import Simbad
from vizier import Vizier

#### Choice of the target
targets = ["HD1", "HD225002", "TYC4619-98-1", "TYC2275-512-1", "TYC4018-3553-1", "other"]

for i in range(len(targets)):
	print(f"-> [{i}] {targets[i]}")
nb = int(input("\n[choose a target] "))

target = targets[nb]
if target == "other":
	target = input("[enter a target name] ")


#### Dictionnary mapping the system/filter between c_astrom2.c and the vizier request
apogee_system_filter = {
	"Jmag"		: {"system": "2MASS",		"filter": "J"},
	"Hmag"		: {"system": "2MASS",		"filter": "H"},
	"Ksmag"		: {"system": "2MASS",		"filter": "Ks"},
	"Mmag"		: {"system": "Washington",	"filter": "M"},
	"T2mag"		: {"system": "Washington",	"filter": "T2"},
	"3.6mag"	: {"system": "Spitzer/IRAC",	"filter": "3.6"},
	"4.5mag"	: {"system": "Spitzer/IRAC",	"filter": "4.5"},
	"5.8mag"	: {"system": "Spitzer/IRAC",	"filter": "5.8"},
	"8.0mag"	: {"system": "Spitzer/IRAC",	"filter": "8.0"},
	"4.5magW"	: {"system": "WISE",		"filter": "W2"}
}
xmm_system_filter = {
	"UVM2mag"	: {"system": "XMM-OT","filter": "V"},
	"UVW1mag"	: {"system": "XMM-OT","filter": "V"},
	"Umag"		: {"system": "XMM-OT","filter": "V"},
	"Bmag"		: {"system": "XMM-OT","filter": "B"},
	"Vmag"		: {"system": "XMM-OT","filter": "V"}
}

catalogue = {
	"APOGEE"	: apogee_system_filter,
	"XMM" 		: xmm_system_filter
}


#### Create a simbad object to get information on the object
sim = Simbad(target)
sim.simbad_table()


#### Create a vizier object to get the conesearch and the sed
conesearch = str(input(f"\n\n[do you want to perform a conesearch around {target} and get the sed? (y/n)] ")).upper()
while True:
	if conesearch == "Y" or conesearch == "YES" or conesearch == "N" or conesearch == "NO" :
		break
	else:			
		conesearch = str(input(f"[please enter (y/n)] ")).upper()

if conesearch == "Y" or conesearch == "YES":
		viz = Vizier(target, catalogue)
		table = viz.vizier_table()
		viz.plot(table)

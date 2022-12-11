from simbad import Simbad
from vizier import Vizier



target = 'TYC4018-3553-1'#str(input("Target name: "))


apogee_system_filter = {
	"Jmag"		: {"system": "2MASS","filter": "J"},
	"Hmag"		: {"system": "2MASS","filter": "H"},
	"Ksmag"		: {"system": "2MASS","filter": "Ks"},
	"Mmag"		: {"system": "Washington","filter": "M"},
	"T2mag"		: {"system": "Washington","filter": "T2"},
	"3.6mag"	: {"system": "Spitzer/IRAC","filter": "3.6"},
	"4.5mag"	: {"system": "Spitzer/IRAC","filter": "4.5"},
	"5.8mag"	: {"system": "Spitzer/IRAC","filter": "5.8"},
	"8.0mag"	: {"system": "Spitzer/IRAC","filter": "8.0"},
	"4.5magW"	: {"system": "WISE","filter": "W2"}
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




sim = Simbad(target)
sim.simbad_table()

conesearch = str(input(f"\n[do you want to perform a conesearch around {target} and get the sed? (y/n)] ")).upper()
while True:
	if conesearch == "Y" or conesearch == "YES" or conesearch == "N" or conesearch == "NO" :
		break
	else:			
		conesearch = str(input(f"[please enter (y/n)] ")).upper()

if conesearch == "Y" or conesearch == "YES":
		viz = Vizier(target, catalogue)
		table = viz.vizier_table()
		viz.plot(table)
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

viz = Vizier(target, catalogue)
table = viz.vizier_table()
viz.plot(table)
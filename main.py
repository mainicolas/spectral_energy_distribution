from astropy.table import Table, Column
import matplotlib.pyplot as plt
import urllib.request as http
import interface as ihi
import numpy as np

from astropy import units as u
from astropy.coordinates import SkyCoord




"""
class simbad():
	def __init__(self, target:str) -> None:
		self.target = target
		
	def resolver(self):
		simbad_url = f"https://simbad.u-strasbg.fr/simbad/sim-id?output.format=ASCII&output.console=off&output.script=off&Ident={self.target}"
		flux = [[], [], []]

		with http.urlopen(simbad_url) as fd:
			for line in fd:
				if "Coordinates(ICRS,ep=J2000,eq=2000)" in line.decode('UTF-8'):
					az = line.decode('UTF-8').split() 
					pos = SkyCoord(az[1]+" "+az[2]+" "+az[3]+" "+az[4]+" "+az[5]+" "+az[6], unit=(u.hourangle, u.deg))

				if "Flux" in line.decode('UTF-8'):
					if len(line.decode('UTF-8').split()) > 2:
						flux[0].append(line.decode('UTF-8').split()[1]) # Filter
						flux[1].append(line.decode('UTF-8').split()[3]) # Flux value
						if line.decode('UTF-8').split()[4] != '[~]':
							flux[2].append(line.decode('UTF-8').split()[4][1:-1]) # Error on flux
						else:
							flux[2].append(np.ma.masked) # If no error on flux
					else:
						flux[0].append(np.ma.masked)
						flux[1].append(np.ma.masked)
						flux[2].append(np.ma.masked)


"""




#########################################################################################################################
#########################################################################################################################
#########################################################################################################################
### Build a Simbad resolver
def simbad_resolver(target:str, system_:str="Johnson"):
	simbad_url = f"https://simbad.u-strasbg.fr/simbad/sim-id?output.format=ASCII&output.console=off&output.script=off&Ident={target}"

	flux = [[],[],[]] #filter, flux, flux error
	flux_jsky = []
	waveband, coordinates = [], []

	with http.urlopen(simbad_url) as fd:
		for line in fd:
			if "Coordinates(ICRS,ep=J2000,eq=2000)" in line.decode("UTF-8"):
				az = line.decode("UTF-8").split() 
				coordinates = SkyCoord(az[1]+" "+az[2]+" "+az[3]+" "+az[4]+" "+az[5]+" "+az[6], unit=(u.hourangle, u.deg))


			if "Flux" in line.decode("UTF-8"):
				if len(line.decode("UTF-8").split()) > 1:
					flux[0].append(line.decode("UTF-8").split()[1]) # Filter
					flux[1].append(line.decode("UTF-8").split()[3]) # Flux value

					if line.decode("UTF-8").split()[4] != '[~]':
						flux[2].append(line.decode("UTF-8").split()[4][1:-1]) # Error on flux
					else:
						flux[2].append(np.ma.masked) # If no error on flux
				else:
					flux[0].append(np.ma.masked)
					flux[1].append(np.ma.masked)
					flux[2].append(np.ma.masked)
					
	
	for i in range(len(flux[0])):
		waveband.append(ihi.search_vega_filter_py(system_, flux[0][i])[0])
		if waveband[i] < 1e-15:
			waveband[i] = np.nan
			flux_jsky.append(np.ma.masked)
			flux[2][i] = np.ma.masked
		else:
			flux_jsky.append(ihi.to_jsky(ihi.search_vega_filter_py(system_, flux[0][i])[2], float(flux[1][i])))
	
	waveband_col = Column(data=waveband, name="Waveband", dtype=float, unit="µm")

	coord_x = [coordinates.ra.deg]
	coord_y = [coordinates.dec.deg]
	while len(coord_x) < len(flux[1]):
		coord_x.append(" ")
		coord_y.append(" ")

	simbad = Table([coord_x, coord_y, flux[0], flux_jsky, flux[2]],names=("Ra", "Dec", "Filter", "Flux", "Flux_error"), units=("deg", "deg", " ", "jansky", "jansky"))
	simbad.add_column(waveband_col, index=3)
	print("[Informations on requested target]")
	print(simbad)

	return coord_x[0], coord_y[0], simbad








#########################################################################################################################
#########################################################################################################################
#########################################################################################################################
### Extract photometry from VizieR tables
def vizier_conesearch(center:str, radius:str, catalogue:dict, ra, dec)->list:
	requested_table = []
	column_choice	= []	
	sed				= []
	apogee_coord 	= ["RAJ2000", "DEJ2000"]
	xmm_coord		= ["RAICRS", "DEICRS"]


	###################interactive part in the terminal
	## Define the catalogue
	for i in range(len(catalogue)):
		print("->",list(catalogue.keys())[i])
	catalogue_choice = str(input("[enter the name of the catalogue] ")).upper()
	while True:
		if catalogue_choice in list(catalogue.keys()):
			break
		else:
			catalogue_choice = str(input("[please enter a valid name] ")).upper()

	if catalogue_choice == "APOGEE":
		name="III/284/allstars"
	else:
		name="II/340/xmmom2_1"

	#Define the requested columns
	for i in range(len(catalogue[catalogue_choice].values())):
		print("\t->",list(catalogue[catalogue_choice].keys())[i])
	nb_column = int(input('\t[enter the number of requested column(s) (integer)] '))
	
	for i in range(nb_column):
		choice = input("\t[enter requested column ("+str(i+1)+")] ")
		while True:
			if choice in list(catalogue[catalogue_choice].keys()):
				break
			else:
				choice =  str(input("\t[please enter a valid name] "))
		column_choice.append(choice)
		#column_choice.append(str(input("\t[enter requested column ("+str(i+1)+")] ")))
		if column_choice[i] == "3.6mag" or column_choice[i] == "4.5mag" or column_choice[i] == "5.8mag" or column_choice[i] == "8.0mag" or column_choice[i] == "4.5magW" :
			column_choice[i] = "_"+column_choice[i]
	print("\n")




	#Create vizier table
	vizier_url		= f"https://vizier.cds.unistra.fr/viz-bin/votable?-source={name}&-c={center}&-c.rm={radius}&-out.all=1"
	vizier_table	= Table.read(vizier_url, format="votable")
	
	if catalogue_choice == "APOGEE":
		for i in range(len(apogee_coord)):
			requested_table.append(vizier_table[apogee_coord[i]])

	else:
		for i in range(len(xmm_coord)):
			requested_table.append(vizier_table[xmm_coord[i]])
	

	for i in range(len(column_choice)):
		sed.append([])
		a = np.where(vizier_table[column_choice[i]].mask == False)

		for j in a[0]:
			vizier_table[column_choice[i]][j] = ihi.to_jsky(ihi.search_vega_filter_py(list(catalogue[catalogue_choice][column_choice[0]].values())[0],
					list(catalogue[catalogue_choice][column_choice[0]].values())[1])[2],vizier_table[column_choice[i]][j])
			vizier_table["e_"+column_choice[i]] = ihi.to_jsky(ihi.search_vega_filter_py(list(catalogue[catalogue_choice][column_choice[0]].values())[0],
					list(catalogue[catalogue_choice][column_choice[0]].values())[1])[2],vizier_table[column_choice[i]][j])
		
		requested_table.append(vizier_table[column_choice[i]])
		if column_choice[i] == "_3.6mag" or column_choice[i] == "_4.5mag" or column_choice[i] == "_5.8mag" or column_choice[i] == "_8.0mag" or column_choice[i] == "_4.5magW":
			column_choice[i] = column_choice[i].replace("_","")

		
		sed[i].append(ihi.search_vega_filter_py(list(catalogue[catalogue_choice][column_choice[i]].values())[0],list(catalogue[catalogue_choice][column_choice[i]].values())[1])[0])
		requested_table.append(vizier_table["e_"+column_choice[i]])


		if column_choice[i] == "3.6mag" or column_choice[i] == "4.5mag" or column_choice[i] == "5.8mag" or column_choice[i] == "8.0mag" or column_choice[i] == "4.5magW":
			column_choice[i] = "_"+column_choice[i]


	vizier = Table(requested_table)
	raa, decc = [], []
	for i in range(len(vizier["RAJ2000"])):
		if np.max(vizier["RAJ2000"]) > 340 and np.min(vizier["RAJ2000"]) < 20 and vizier["RAJ2000"][i] > 180:
			raa.append(vizier["RAJ2000"][i] -360)
		else:
			raa.append(vizier["RAJ2000"][i])

	plt.figure(figsize=(17,8))
	plt.subplot(121)
	if catalogue_choice == "APOGEE":
		plt.scatter(raa, vizier["DEJ2000"], c="orange")
		plt.scatter(ra,dec,c="dodgerblue")
	else:
		plt.scatter(vizier["RAICRS"], vizier["DEICRS"], c="orange")
	plt.title("Coordinates plot of nearby objects")
	plt.xlabel("Right ascension (deg)")
	plt.ylabel("Declination (deg)")
	plt.grid(ls=':')

	plt.subplot(122)
	for i in range(len(sed)):
		if len(sed[i]) != 0:
			l = np.ones(len(vizier[column_choice[i]]))*sed[i]
			plt.scatter(l, vizier[column_choice[i]], label=f"{column_choice[i]}")
	plt.title("Spectral energy distribution")
	plt.xlabel("Filter value $\lambda$ (µm)")
	plt.yscale("log")
	plt.ylabel("Flux (Jy)")
	plt.grid(ls=':')
	plt.legend()
	plt.show()	

	return requested_table, catalogue_choice, sed

### -> calculate error in jansky



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


#name = "III/284/allstars"#input(str('name: '))
centre = "HD1"#"TYC4018-3553-1"#"HD225002"#"TYC4619-98-1"
radius = "50"






#########################################################################################################################
#########################################################################################################################
#########################################################################################################################
###Compose Simbad and VizieR photometry


def photometry(target:str, radius:int):
	a = simbad_resolver(target)
	
	data = vizier_conesearch(target, radius, catalogue, a[0], a[1])
	plot = data[2:]
				
	jsky = "jansky"
	units_ = ["degree", "degree"]
	for i in range(len(data[0])-2):
		units_.append(jsky)
	data_table = Table(data[0], units=tuple(units_))
	print(data_table)
	"""
	if data[1] == "APOGEE":
		plt.scatter(data_table["RAJ2000"], data_table["DEJ2000"], c="orange")
	else:
		plt.scatter(data_table["RAICRS"], data_table["DEICRS"], c="orange")
	plt.xlabel("Right ascension (deg)")
	plt.ylabel("Declination (deg)")
	plt.grid(ls=':')
	plt.show()
	"""
photometry(centre,radius)

from astropy.table import Table, Column
import urllib.request as http
import astrom2 as astrom
import numpy as np

from astropy import units as u
from astropy.coordinates import SkyCoord


class Simbad():
	def __init__(self, target:str) -> None:
		self.target			= target
		self.system_ 		= "Johnson"	
		self.flux 			= [[],[],[]]
		self.flux_Jy		= [[],[],[]]
		self.coordinates 	= [[],[]]


	def get_data(self):
		simbad_url	= f"https://simbad.u-strasbg.fr/simbad/sim-id?output.format=ASCII&output.console=off&output.script=off&Ident={self.target}"

		with http.urlopen(simbad_url) as fd:
			for line in fd:
				if "Coordinates(ICRS,ep=J2000,eq=2000)" in line.decode("UTF-8"):
					decode = line.decode('UTF-8').split() 
					position = SkyCoord(decode[1]+" "+decode[2]+" "+decode[3]+" "+decode[4]+" "+decode[5]+" "+decode[6], unit=(u.hourangle, u.deg))

				if "Flux" in line.decode("UTF-8"):
					if len(line.decode('UTF-8').split()) > 2:
						self.flux[0].append(line.decode("UTF-8").split()[1]) 
						self.flux[1].append(line.decode("UTF-8").split()[3])
						if line.decode('UTF-8').split()[4] != '[~]':
							self.flux[2].append(line.decode("UTF-8").split()[4][1:-1]) 
						else:
							self.flux[2].append(np.ma.masked) 
					else:
						self.flux[0].append(np.ma.masked)
						self.flux[1].append(np.ma.masked)
						self.flux[2].append(np.ma.masked)

		self.coordinates[0].append(position.ra.deg)
		self.coordinates[1].append(position.dec.deg)


	def waveband(self):
		waveband 	= []

		for i in range(len(self.flux[0])):
			waveband.append(astrom.search_vega_filter_py(self.system_, self.flux[0][i])[0])
			if waveband[i] < 1e-15:
				waveband[i] = np.nan
				self.flux_Jy[0].append(np.ma.masked)
				self.flux_Jy[1].append(np.ma.masked)
				self.flux_Jy[2].append(np.ma.masked)
			else:
				self.flux_Jy[0].append(astrom.to_jsky(astrom.search_vega_filter_py(self.system_, self.flux[0][i])[2], float(self.flux[1][i])))
				self.flux_Jy[1].append(astrom.to_jsky(astrom.search_vega_filter_py(self.system_, self.flux[0][i])[2], float(self.flux[1][i])+float(self.flux[2][i])))
				self.flux_Jy[2].append(astrom.to_jsky(astrom.search_vega_filter_py(self.system_, self.flux[0][i])[2], float(self.flux[1][i])-float(self.flux[2][i])))

		waveband_col = Column(data=waveband, name="Waveband", dtype=float, unit="µm")
		return waveband_col

		

	def simbad_table(self):
		position 		= self.get_data()
		waveband_col	= self.waveband()
		sup, inf = [], []

		while len(self.coordinates[0]) < len(self.flux[0]):
			self.coordinates[0].append(" ")
			self.coordinates[1].append(" ")
		for i in range(len(self.flux_Jy[0])):
			if np.isnan(self.flux_Jy[0][i]) == False:
				sup.append(self.flux_Jy[0][i] - self.flux_Jy[1][i])
				inf.append(self.flux_Jy[2][i] - self.flux_Jy[0][i])
			else:
				sup.append(np.ma.masked)
				inf.append(np.ma.masked)

		simbad = Table([self.coordinates[0], self.coordinates[1], self.flux[0], self.flux_Jy[0], sup, inf],
				names=("Ra", "Dec", "Filter", "Flux", "Flux_err+", "Flux_err-"), units=("deg", "deg", " ", "jansky", "jansky", "jansky"))
		simbad.add_column(waveband_col, index=3)
		print(f"\nSimbad informations on object: {self.target}")
		print(simbad)
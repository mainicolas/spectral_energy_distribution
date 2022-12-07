import matplotlib.pyplot as plt

from simbad import *

class Vizier(Simbad):
	def __init__(self, target:str, catalogue:dict) -> None:
		super().__init__(target)
		self.requested_table 	= []
		self.column_choice 		= []
		self.sed				= []
		self.apogee_coord		= ["RAJ2000", "DEJ2000"]
		self.xmm_coord			= ["RAICRS", "DEICRS"]
		self.catalogue			= catalogue
		self.catalogue_choice	= None
		self.table_name			= None
		self.radius				= None

	def conesearch_radius(self):
		print("\n")
		self.radius = int(input("[enter the requested radius for the conesearch (in arcmin)]"))

	def catalogue_request(self):
		#Define the catalogue
		for i in range(len(self.catalogue)):
			print("->",list(self.catalogue.keys())[i])
		self.catalogue_choice = str(input("[enter the name of the catalogue] ")).upper()
		while True:
			if self.catalogue_choice in list(self.catalogue.keys()):
				break
			else:
				self.catalogue_choice = str(input("[please enter a valid name] ")).upper()

		if self.catalogue_choice == "APOGEE":
			self.name="III/284/allstars"
		else:
			self.name="II/340/xmmom2_1"


	def column_request(self):
		#Define the requested columns
		self.catalogue_request()
		for i in range(len(self.catalogue[self.catalogue_choice].values())):
			print("\t->",list(self.catalogue[self.catalogue_choice].keys())[i])
		nb_column = int(input('\t[enter the number of requested column(s) (integer)] '))
		
		for i in range(nb_column):
			choice = input("\t[enter requested column ("+str(i+1)+")] ")
			while True:
				if choice in list(self.catalogue[self.catalogue_choice].keys()):
					break
				else:
					choice =  str(input("\t[please enter a valid name] "))
			self.column_choice.append(choice)
			if self.column_choice[i] == "3.6mag" or self.column_choice[i] == "4.5mag" or self.column_choice[i] == "5.8mag" or self.column_choice[i] == "8.0mag" or self.column_choice[i] == "4.5magW" :
				self.column_choice[i] = "_"+self.column_choice[i]
		print("\n")


	def vizier_table(self):
		self.conesearch_radius()
		
		self.column_request()
		url = f"https://vizier.cds.unistra.fr/viz-bin/votable?-source={self.name}&-c={self.target}&-c.rm={self.radius}&-out.all=1"
		table = Table.read(url, format="votable")

		if self.catalogue_choice == "APOGEE":
			for i in range(len(self.apogee_coord)):
				self.requested_table.append(table[self.apogee_coord[i]])

		else:
			for i in range(len(self.xmm_coord)):
				self.requested_table.append(table[self.xmm_coord[i]])		


		for i in range(len(self.column_choice)):
			self.sed.append([])
			a = np.where(table[self.column_choice[i]].mask == False)
			if self.column_choice[i] == "_3.6mag" or self.column_choice[i] == "_4.5mag" or self.column_choice[i] == "_5.8mag" or self.column_choice[i] == "_8.0mag" or self.column_choice[i] == "_4.5magW":
				without = self.column_choice[i].replace("_","")
				# column_choice[i] = column_choice[i].replace("_","")
				for j in a[0]:#range(len(column_choice[i])):#a[0]:
					bb=ihi.to_jsky(ihi.search_vega_filter_py(list(self.catalogue[self.catalogue_choice][without].values())[0],
							list(self.catalogue[self.catalogue_choice][without].values())[1])[2],table[self.column_choice[i]][j])
					cc=ihi.to_jsky(ihi.search_vega_filter_py(list(self.catalogue[self.catalogue_choice][without].values())[0],
							list(self.catalogue[self.catalogue_choice][without].values())[1])[2],table[self.column_choice[i]][j])
					table[self.column_choice[i]][j] = bb
					table["e_"+without]=cc
			else:
				for j in a[0]:
					bb=ihi.to_jsky(ihi.search_vega_filter_py(list(self.catalogue[self.catalogue_choice][self.column_choice[i]].values())[0],
							list(self.catalogue[self.catalogue_choice][self.column_choice[i]].values())[1])[2],table[self.column_choice[i]][j])
					cc=ihi.to_jsky(ihi.search_vega_filter_py(list(self.catalogue[self.catalogue_choice][self.column_choice[i]].values())[0],
							list(self.catalogue[self.catalogue_choice][self.column_choice[i]].values())[1])[2],table[self.column_choice[i]][j])
					table[self.column_choice[i]][j] = bb
					table["e_"+self.column_choice[i]]=cc			

			if self.column_choice[i] == "3.6mag" or self.column_choice[i] == "4.5mag" or self.column_choice[i] == "5.8mag" or self.column_choice[i] == "8.0mag" or self.column_choice[i] == "4.5magW":
				self.column_choice[i] = "_"+self.column_choice[i]
			self.requested_table.append(table[self.column_choice[i]])
			if self.column_choice[i] == "_3.6mag" or self.column_choice[i] == "_4.5mag" or self.column_choice[i] == "_5.8mag" or self.column_choice[i] == "_8.0mag" or self.column_choice[i] == "_4.5magW":
				self.column_choice[i] = self.column_choice[i].replace("_","")

			
			self.sed[i].append(ihi.search_vega_filter_py(list(self.catalogue[self.catalogue_choice][self.column_choice[i]].values())[0],list(self.catalogue[self.catalogue_choice][self.column_choice[i]].values())[1])[0])
			self.requested_table.append(table["e_"+self.column_choice[i]])


			if self.column_choice[i] == "3.6mag" or self.column_choice[i] == "4.5mag" or self.column_choice[i] == "5.8mag" or self.column_choice[i] == "8.0mag" or self.column_choice[i] == "4.5magW":
				self.column_choice[i] = "_"+self.column_choice[i]

		vizier = Table(self.requested_table)
		print(vizier)
		return vizier


	def plot(self, table):
		self.get_data()
		
		ra, dec = self.coordinates[0], self.coordinates[1]
		raa = []
		
		if self.catalogue_choice == "APOGEE":
			for i in range(len(table["RAJ2000"])):
				if np.max(table["RAJ2000"]) > 340 and np.min(table["RAJ2000"]) < 20 and table["RAJ2000"][i] > 180:
					raa.append(table["RAJ2000"][i] -360)
				else:
					raa.append(table["RAJ2000"][i])
		else:
			for i in range(len(table["RAICRS"])):
				if np.max(table["RAICRS"]) > 340 and np.min(table["RAICRS"]) < 20 and table["RAICRS"][i] > 180:
					raa.append(table["RAICRS"][i] -360)
				else:
					raa.append(table["RAICRS"][i])
		print(len(ra),len(table["RAJ2000"]))
		plt.figure(figsize=(17,8))
		plt.subplot(121)
		if self.catalogue_choice == "APOGEE":
			plt.scatter(raa, table["DEJ2000"], c="orange")
			plt.scatter(ra,dec,c="dodgerblue")
		else:
			plt.scatter(raa, table["DEICRS"], c="orange")
			plt.scatter(ra,dec,c="dodgerblue")
		plt.title("Coordinates plot of nearby objects")
		plt.xlabel("Right ascension (deg)")
		plt.ylabel("Declination (deg)")
		plt.grid(ls=':')

		plt.subplot(122)
		for i in range(len(self.sed)):
			if len(self.sed[i]) != 0:
				l = np.ones(len(table[self.column_choice[i]]))*self.sed[i]
				plt.scatter(l, table[self.column_choice[i]], label=f" {self.column_choice[i]}")
		plt.title("Spectral energy distribution")
		plt.xlabel("Filter value $\lambda$ (µm)")
		#plt.xscale("log")
		plt.yscale("log")
		plt.ylabel("Flux (Jy)")
		plt.grid(ls=':')
		plt.legend()
		plt.show()	


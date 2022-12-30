import matplotlib.pyplot as plt

from simbad import *

class Vizier(Simbad):
	def __init__(self, target:str, catalogue:dict) -> None:
		super().__init__(target)
		self.requested_table	= []
		self.column_choice	= []
		self.sed		= [[],[]]
		self.apogee_coord	= ["RAJ2000", "DEJ2000"]
		self.xmm_coord		= ["RAICRS", "DEICRS"]
		self.catalogue		= catalogue
		self.catalogue_choice	= None
		self.table_name		= None
		self.radius		= None

	def conesearch_radius(self):
		'''
		update the attribute self.radius
		'''
		self.radius = int(input("\n[enter the requested radius for the conesearch (arcmin)] "))
		print("\n ")

	def catalogue_request(self):
		'''
		update the attribute self.catalogue_choice
		'''
		for i in range(len(self.catalogue)):
			print("->",list(self.catalogue.keys())[i])
		self.catalogue_choice = str(input("[enter the name of the catalogue] ")).upper()
		while True:
			if self.catalogue_choice in list(self.catalogue.keys()):
				break
			else:
				self.catalogue_choice = str(input("[please enter a valid name] ")).upper()

		if self.catalogue_choice == "APOGEE":
			self.name ="III/284/allstars"
		else:
			self.name ="II/340/xmmom2_1"


	def column_request(self):
		'''
		update the attribute self.column_choice:
			-> select all the columns
		  or
			-> ask number of requested column
			-> self.column_choice.append(requested_column)
		'''
		self.catalogue_request()
		for i in range(len(self.catalogue[self.catalogue_choice].values())):
			print("\t->",list(self.catalogue[self.catalogue_choice].keys())[i])
		#print("\t-> all")
		nb_column = (input('\t[enter the number of requested column(s) (integer) or \'all\'] '))
		if nb_column == "all" or nb_column == "ALL":
			for i in range(len(self.catalogue[self.catalogue_choice].keys())):
				self.column_choice.append(list(self.catalogue[self.catalogue_choice].keys())[i])
				if self.column_choice[i] == "3.6mag" or self.column_choice[i] == "4.5mag" or self.column_choice[i] == "5.8mag" or self.column_choice[i] == "8.0mag" or self.column_choice[i] == "4.5magW" :
									self.column_choice[i] = "_"+self.column_choice[i]

		else:
			nb_column = int(nb_column)
			while True:
				if nb_column <= len(self.catalogue[self.catalogue_choice].keys()) and nb_column > 0:
					break
				else:
					nb_column = int(input(f"\t[please enter a valid number of column(s) (1 to {len(self.catalogue[self.catalogue_choice].keys())})] "))
			
			for i in range(nb_column):
				choice = input("\t[enter requested column ("+str(i+1)+")] ")
				while True:
					if choice in list(self.catalogue[self.catalogue_choice].keys()) and choice not in self.column_choice:
						break
					else:
						choice =  str(input("\t[please enter a valid name] "))
				self.column_choice.append(choice)
				if self.column_choice[i] == "3.6mag" or self.column_choice[i] == "4.5mag" or self.column_choice[i] == "5.8mag" or self.column_choice[i] == "8.0mag" or self.column_choice[i] == "4.5magW" :
					self.column_choice[i] = "_"+self.column_choice[i]
		print("\n")


	def vizier_table(self):
		'''
		create an astropy table with all the requested columns
		update:
			flux in jansky
			self.sed[0] -> lambda,  from search_vega_filter_py() to get the sed
			self.sed[1] -> dlambda, from search_vega_filter_py() to get the sed
		return:
			vizier (astropy table)
		'''
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
			self.sed[0].append([])
			self.sed[1].append([])

			a = np.where(table[self.column_choice[i]].mask == False)
			if self.column_choice[i] == "_3.6mag" or self.column_choice[i] == "_4.5mag" or self.column_choice[i] == "_5.8mag" or self.column_choice[i] == "_8.0mag" or self.column_choice[i] == "_4.5magW":
				column = self.column_choice[i].replace("_","")
				for j in a[0]:
					table["e_" + column][j]		= astrom.to_jsky(astrom.search_vega_filter_py(list(self.catalogue[self.catalogue_choice][column].values())[0],
							list(self.catalogue[self.catalogue_choice][column].values())[1])[2],table["e_" + column][j]+table[self.column_choice[i]][j])
					table[self.column_choice[i]][j]	= astrom.to_jsky(astrom.search_vega_filter_py(list(self.catalogue[self.catalogue_choice][column].values())[0],
							list(self.catalogue[self.catalogue_choice][column].values())[1])[2],table[self.column_choice[i]][j])
					table["e_" + column][j] = table[self.column_choice[i]][j] - table["e_" + column][j]
			else:
				column = self.column_choice[i]
				for j in a[0]:
					table["e_"+self.column_choice[i]][j]	= astrom.to_jsky(astrom.search_vega_filter_py(list(self.catalogue[self.catalogue_choice][self.column_choice[i]].values())[0],
							list(self.catalogue[self.catalogue_choice][self.column_choice[i]].values())[1])[2], table["e_"+self.column_choice[i]][j]+table[self.column_choice[i]][j])	
					table[self.column_choice[i]][j]		= astrom.to_jsky(astrom.search_vega_filter_py(list(self.catalogue[self.catalogue_choice][self.column_choice[i]].values())[0],
							list(self.catalogue[self.catalogue_choice][self.column_choice[i]].values())[1])[2],table[self.column_choice[i]][j])
					table["e_"+self.column_choice[i]][j] 	= table[self.column_choice[i]][j] - table["e_"+self.column_choice[i]][j]
							

			self.requested_table.append(table[self.column_choice[i]])
			
			self.sed[0][i].append(astrom.search_vega_filter_py(list(self.catalogue[self.catalogue_choice][column].values())[0],list(self.catalogue[self.catalogue_choice][column].values())[1])[0])
			self.sed[1][i].append(astrom.search_vega_filter_py(list(self.catalogue[self.catalogue_choice][column].values())[0],list(self.catalogue[self.catalogue_choice][column].values())[1])[1])
			self.requested_table.append(table["e_"+column])


		vizier = Table(self.requested_table)
		print(vizier)
		return vizier


	def plot(self, table):
		'''
		plot the objects in the conesearch
		plot the sed
		'''
		self.get_data()
		ra, dec 	= self.coordinates[0], self.coordinates[1]
		ra_correction	= []
		
		for i in range(len(table.columns[0])):
			if np.max(table.columns[0]) > 340 and np.min(table.columns[0]) < 20 and table.columns[0][i] > 180:
				ra_correction.append(table.columns[0][i] - 360)
			else:
				ra_correction.append(table.columns[0][i])

		plt.figure(figsize=(17,8))
		plt.subplot(121)
		plt.scatter(ra_correction, table.columns[1], c="orange")
		plt.scatter(ra,dec,c="dodgerblue", label=f"{self.target}")

		plt.title("Coordinates plot of nearby objects", fontsize=17, fontname="Serif")
		plt.xlabel("Right ascension (deg)", fontsize=12, fontname="Serif")
		plt.ylabel("Declination (deg)", fontsize=12, fontname="Serif")
		plt.grid(ls=':')
		plt.legend()


		plt.subplot(122)
		for i in range(len(self.sed[0])):
			new	= []
			new_er 	= []
			
			a = np.where(table[self.column_choice[i]].mask == False)
			for j in a[0]:
				new.append(table[self.column_choice[i]][j])
			if len(new) != 0:
				l 	= np.ones(len(new))*self.sed[0][i]
				x_er 	= np.ones(len(new))*self.sed[1][i]

				if self.column_choice[i] == "_3.6mag" or self.column_choice[i] == "_4.5mag" or self.column_choice[i] == "_5.8mag" or self.column_choice[i] == "_8.0mag" or self.column_choice[i] == "_4.5magW":
					self.column_choice[i] = self.column_choice[i].replace("_","")
					b = np.where(table["e_"+self.column_choice[i]].mask == False)
					for j in b[0]:
						new_er.append(table["e_"+self.column_choice[i]][j])

					
				else:
					b = np.where(table["e_"+self.column_choice[i]].mask == False)
					for j in b[0]:
						new_er.append(table["e_"+self.column_choice[i]][j])

				
				plt.errorbar(l, new, xerr=x_er , yerr=new_er, fmt="o", label=f" {self.column_choice[i]}", elinewidth=0.9, capsize=2.7)
				plt.title("Spectral energy distribution", fontsize=17, fontname="Serif")
				plt.xlabel("Filter value $\lambda$ (µm)", fontsize=12, fontname="Serif")
				plt.ylabel("Flux (Jy)", fontsize=12, fontname="Serif")
				plt.yscale("log")
				plt.grid(ls=':')
				plt.legend()
		plt.show()

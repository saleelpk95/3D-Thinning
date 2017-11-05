import numpy as np
import itertools
import json

class Utils():
	
	def __init__(self):
		self.supportVectorList = [[1,1,1], [-1,1,1], [-1,-1,1], [1,-1,1], [1,1,-1], [-1,1,-1], [-1,-1,-1], [1,-1,-1],]
		self.essentialCliquesGlobal = {}

		simple_voxels_set_json = open('simple_voxels_set.json')
		simple_voxels_set_json_str = simple_voxels_set_json.read()
		self.simple_voxels_set = eval(json.loads(simple_voxels_set_json_str)['data'])

		isCritical_voxel_set_json = open('isCritical_voxel_set.json')
		isCritical_voxel_set_json_str = isCritical_voxel_set_json.read()
		self.isCritical_voxel_set = eval(json.loads(isCritical_voxel_set_json_str)['data'])

		maskForAllNeighbours_set_json = open('maskForAllNeighbours_set.json')
		maskForAllNeighbours_set_json_str = maskForAllNeighbours_set_json.read()
		self.maskForAllNeighbours_set = eval(json.loads(maskForAllNeighbours_set_json_str)['data'])

		isConnected_set_json = open('isConnected_set.json')
		isConnected_set_json_str = isConnected_set_json.read()
		self.isConnected_set = eval(json.loads(isConnected_set_json_str)['data'])

		essentialCliques_set_json = open('essentialCliques_set.json')
		essentialCliques_set_json_str = essentialCliques_set_json.read()
		self.essentialCliques_set = eval(json.loads(essentialCliques_set_json_str)['data'])

		criticalCliques_set_json = open('criticalCliques_set.json')
		criticalCliques_set_json_str = criticalCliques_set_json.read()
		self.criticalCliques_set = eval(json.loads(criticalCliques_set_json_str)['data'])

		# isReducible_set_json = open('isReducible_set.json')
		# isReducible_set_json_str = isReducible_set_json.read()
		# self.isReducible_set = eval(json.loads(isReducible_set_json_str)['data'])

		kCriticalCliques_set_json = open('kCriticalCliques_set.json')
		kCriticalCliques_set_json_str = kCriticalCliques_set_json.read()
		self.kCriticalCliques_set = eval(json.loads(kCriticalCliques_set_json_str)['data'])

	# Given a list of centres as tuples, generate the vertices for all the voxels.
	def generateVerticesForCentres(self, voxelCentreList, edgeLength=1):

		vertexListForAllCentres = []

		for centre in voxelCentreList:
		
			vertexListForOneCentre = []
			c = np.array(centre)
			
			for supportVector in self.supportVectorList:
		
				s = np.array(supportVector)
				singleVertexArray = c + (edgeLength/2.0)*s
				singleVertexList = tuple(singleVertexArray)
				vertexListForOneCentre.append(singleVertexList)

			vertexListForAllCentres.append(vertexListForOneCentre)

		return vertexListForAllCentres

	# def findAllCliquesForComplex(self, voxelCentreList, edgeLength):
	# 	powerSet = self.generatePowerSet(voxelCentreList)
	# 	powerSet.remove([])
	# 	cliqueList = [clique for clique in powerSet if self.isConnected(clique, edgeLength)]
	# 	return cliqueList

	def updateAllLookupFiles(self):
		f = open('simple_voxels_set.json', "w")
		data = json.dumps({'data':str(self.simple_voxels_set)})
		f.write(data)
		f.close()

		f = open('isCritical_voxel_set.json', "w")
		data = json.dumps({'data':str(self.isCritical_voxel_set)})
		f.write(data)
		f.close()

		# f = open('isReducible_set.json', "w")
		# data = json.dumps({'data':str(self.isReducible_set)})
		# f.write(data)
		# f.close()

		f = open('kCriticalCliques_set.json', "w")
		data = json.dumps({'data':str(self.kCriticalCliques_set)})
		f.write(data)
		f.close()

		f = open('criticalCliques_set.json', "w")
		data = json.dumps({'data':str(self.criticalCliques_set)})
		f.write(data)
		f.close()

		f = open('essentialCliques_set.json', "w")
		data = json.dumps({'data':str(self.essentialCliques_set)})
		f.write(data)
		f.close()

		f = open('maskForAllNeighbours_set.json', "w")
		data = json.dumps({'data':str(self.maskForAllNeighbours_set)})
		f.write(data)
		f.close()

		f = open('isConnected_set.json', "w")
		data = json.dumps({'data':str(self.isConnected_set)})
		f.write(data)
		f.close()

	def getSimpleVoxels(self, voxelCentreList):
		# print "complex", voxelCentreList
		print "entering getSimpleVoxels"
		if frozenset(voxelCentreList) in self.simple_voxels_set:
			print "leaving getSimpleVoxels"
			return self.simple_voxels_set[frozenset(voxelCentreList)]
		simple_voxels = []
		for voxel in voxelCentreList:
			temp = list(voxelCentreList)
			if self.isReducible(self.getNeighboursForGivenVoxel(voxel, temp)):
				simple_voxels.append(voxel)
		simple_voxels.sort()
		simple_voxels = list(simple_voxels for simple_voxels,_ in itertools.groupby(simple_voxels))
		self.simple_voxels_set[frozenset(voxelCentreList)] = simple_voxels
		# f = open('simple_voxels_set.json', "w")
		# data = json.dumps({'data':str(simple_voxels)})
		# f.write(data)
		# f.close()
		print "leaving getSimpleVoxels"
		return simple_voxels

	def isZeroSurface(self, voxelCentreList):
		if not len(voxelCentreList)==2:
			return False
		if self.isConnected(voxelCentreList):
			return False

		return True

	def isOneSurface(self, voxelCentreList):
		
		if not self.isConnected(voxelCentreList) or len(voxelCentreList)==0:
			return False
		for voxel in voxelCentreList:
			if not self.isZeroSurface(self.getNeighboursForGivenVoxel(voxel, voxelCentreList)):
				return False
		return True

	def isCritical(self, cliqueVoxelCentreList, voxelCentreList):
		print "entering isCritical"
		if frozenset(voxelCentreList) in self.isCritical_voxel_set:
			if frozenset(cliqueVoxelCentreList) in self.isCritical_voxel_set[frozenset(voxelCentreList)]:
				print "leaving isCritical"
				return self.isCritical_voxel_set[frozenset(voxelCentreList)][frozenset(cliqueVoxelCentreList)]
		else:
			self.isCritical_voxel_set[frozenset(voxelCentreList)] = {}
		isRegular = self.isReducible(self.findKStarForClique(cliqueVoxelCentreList, voxelCentreList))
		if not isRegular:
			print "leaving isCritical"
			self.isCritical_voxel_set[frozenset(voxelCentreList)][frozenset(cliqueVoxelCentreList)] = True
			# f = open('isCritical_voxel_set.json', "w")
			# data = json.dumps({'data':str(self.isCritical_voxel_set)})
			# f.write(data)
			# f.close()
			return True
		print "leaving isCritical"
		self.isCritical_voxel_set[frozenset(voxelCentreList)][frozenset(cliqueVoxelCentreList)] = False
		# f = open('isCritical_voxel_set.json', "w")
		# data = json.dumps({'data':str(self.isCritical_voxel_set)})
		# f.write(data)
		# f.close()
		return False

	def isReducible(self, voxelCentreList):
		# if frozenset(voxelCentreList) in self.isReducible_set:
		# 	return self.isReducible_set[frozenset(voxelCentreList)]
		if len(voxelCentreList) == 1:
			# self.isReducible_set[frozenset(voxelCentreList)] = True
			# f = open('isReducible_set.json', "w")
			# data = json.dumps({'data':str(self.isReducible_set)})
			# f.write(data)
			# f.close()
			return True
		for voxel in voxelCentreList:
			# print "voxel in isReducible", voxel
			temp = list(voxelCentreList)
			temp.remove(voxel)
			isNeighboursReducible = self.isReducible(self.getNeighboursForGivenVoxel(voxel, voxelCentreList))
			isOthersReducible = self.isReducible(temp)
			# print "isNeighboursReducible",isNeighboursReducible, "isOthersReducible",isOthersReducible
			if isNeighboursReducible and isOthersReducible:
				# self.isReducible_set[frozenset(voxelCentreList)] = True
				# f = open('isReducible_set.json', "w")
				# data = json.dumps({'data':str(self.isReducible_set)})
				# f.write(data)
				# f.close()
				return True
			# self.isReducible_set[frozenset(voxelCentreList)] = False
			# f = open('isReducible_set.json', "w")
			# data = json.dumps({'data':str(self.isReducible_set)})
			# f.write(data)
			# f.close()
		return False

	def getKCriticalCliques(self, voxelCentreList, k):
		print "entering getKCriticalCliques"
		if frozenset( [frozenset(voxelCentreList), k] ) in self.kCriticalCliques_set:
			print "leaving getKCriticalCliques"
			return self.kCriticalCliques_set[frozenset( [frozenset(voxelCentreList), k] )]
		essentialCliques = self.findEssentialCliquesForComplex(list(voxelCentreList))
		
		simple_voxels = self.getSimpleVoxels(list(voxelCentreList))
		# simple_voxels = [(0,0,0),(2,0,-1)]
		# print "simple_voxels", simple_voxels
		k_critical_cliques = []
		cliques_combined = []
		cliques_combined = list(essentialCliques['three_cliques']) + list(essentialCliques['two_cliques']) + list(essentialCliques['one_cliques']) + list(essentialCliques['zero_cliques'])
		# print 'cliques_combined', cliques_combined
		for clique in cliques_combined:
			
			# temp = list(clique)
			temp = list(self.findKStarForClique(list(clique),list(voxelCentreList)))
			print "kStar for clique",temp
			for voxel in temp:
				if voxel in simple_voxels:
					temp.remove(voxel)
			print "thinned complex for the clique, ",clique," is ", temp
			if k == 1:
				
				if self.isZeroSurface(temp):
					print "this clique is isReducible to isZeroSurface, ",clique," and reduced form is ",temp
					k_critical_cliques.append(clique)
			if k == 2:
				
				if self.isOneSurface(temp):
					print "this clique is isReducible to isoneSurface, ",clique," and reduced form is ",temp
					k_critical_cliques.append(clique)
			if k == 3:
				
				if self.isZeroSurface(temp) or self.isOneSurface(temp):
					print "this clique is isReducible to isZero or one Surface, ",clique," and reduced form is ",temp
					k_critical_cliques.append(clique)
		self.kCriticalCliques_set[frozenset( [frozenset(voxelCentreList), k] )] = k_critical_cliques
		# f = open('kCriticalCliques_set.json', "w")
		# data = json.dumps({'data':str(self.kCriticalCliques_set)})
		# f.write(data)
		# f.close()
		print "leaving getKCriticalCliques"
		return k_critical_cliques

	def findCriticalCliques(self, voxelCentreList):
		print "entering findCriticalCliques"
		if frozenset(voxelCentreList) in self.criticalCliques_set:
			print "leaving findCriticalCliques"
			return self.criticalCliques_set[frozenset(voxelCentreList)]

		essentialCliques = self.findEssentialCliquesForComplex(list(voxelCentreList))
		
		critical_cliques = essentialCliques
		
		zero_cliques = list(essentialCliques['zero_cliques'])
		one_cliques = list(essentialCliques['one_cliques'])
		two_cliques = list(essentialCliques['two_cliques'])
		for clique in zero_cliques:
			if not self.isCritical(clique, voxelCentreList):
				zero_cliques.remove(clique)
		for clique in one_cliques:
			if not self.isCritical(clique, voxelCentreList):
				one_cliques.remove(clique)
		for clique in two_cliques:
			if not self.isCritical(clique, voxelCentreList):
				two_cliques.remove(clique)
		critical_cliques['two_cliques'] = two_cliques
		critical_cliques['one_cliques'] = one_cliques
		critical_cliques['zero_cliques'] = zero_cliques

		self.criticalCliques_set[frozenset(voxelCentreList)] = critical_cliques
		# f = open('criticalCliques_set.json', "w")
		# data = json.dumps({'data':str(self.criticalCliques_set)})
		# f.write(data)
		# f.close()

		print "leaving findCriticalCliques"
		return critical_cliques

	def findEssentialCliquesForComplex(self, voxelCentreList):
		print "entering findEssentialCliquesForComplex"
		if frozenset(voxelCentreList) in self.essentialCliques_set:
			print "leaving findEssentialCliquesForComplex"
			return self.essentialCliques_set[frozenset(voxelCentreList)]
		# contains the cliques according to d-values
		final_dict = {}
		zero_cliques = []
		one_cliques = []
		two_cliques = []
		three_cliques = []
		for centre in voxelCentreList:
			# add voxel as it is three clique
			# three_cliques = list(set(three_cliques).union(set([centre])))
			three_cliques.append([centre])
			
			# check for two cliques
			for mask in self.maskFor2clique(centre):
				common = list(set(mask).intersection(set(voxelCentreList)))
				if len(common)==2:
					# two_cliques = list(set(two_cliques).union(set(common)))
					two_cliques.append(common)

			# check for one cliques
			for mask in self.maskFor1clique(centre):
				common = list(set(mask).intersection(set(voxelCentreList)))
				if len(common)>2:
					# one_cliques = list(set(one_cliques).union(set(common)))
					one_cliques.append(common)
				elif len(common)>1:
					if common not in two_cliques:
						one_cliques.append(common)


			# check for zero cliques
			for mask in self.maskFor0clique(centre):
				common = list(set(mask).intersection(set(voxelCentreList)))
				if len(common)>4:
					# zero_cliques = list(set(zero_cliques).union(set(common)))
					zero_cliques.append(common)
				elif len(common)>1:
					if (common not in two_cliques) and (common not in one_cliques):
						zero_cliques.append(common)
					
		three_cliques.sort()
		three_cliques = list(three_cliques for three_cliques,_ in itertools.groupby(three_cliques))
		two_cliques.sort()
		two_cliques = list(two_cliques for two_cliques,_ in itertools.groupby(two_cliques))
		one_cliques.sort()
		one_cliques = list(one_cliques for one_cliques,_ in itertools.groupby(one_cliques))
		zero_cliques.sort()
		zero_cliques = list(zero_cliques for zero_cliques,_ in itertools.groupby(zero_cliques))
		final_dict['three_cliques'] = three_cliques
		final_dict['two_cliques'] = two_cliques
		final_dict['one_cliques'] = one_cliques
		final_dict['zero_cliques'] = zero_cliques
		self.essentialCliques_set[frozenset(voxelCentreList)] = final_dict
		# f = open('essentialCliques_set.json', "w")
		# data = json.dumps({'data':str(self.essentialCliques_set)})
		# f.write(data)
		# f.close()
		print "leaving findEssentialCliquesForComplex"
		return final_dict

	def findKStarForClique(self, cliqueVoxelCentreList, voxelCentreList, edgeLength = 1):
		kStar = []
		flag = True
		# print "kstar", cliqueVoxelCentreList
		for centre in cliqueVoxelCentreList:
			voxelListForComparison = []
			adjacentVoxels = self.findAllAdjacentVoxelsForGivenVoxel(centre, voxelCentreList, edgeLength)
			
			if flag:
				flag = False
				for voxelList in adjacentVoxels:
					kStar += voxelList
			else:
				for voxelList in adjacentVoxels:
					voxelListForComparison += voxelList
				kStar = list(set(kStar).intersection(voxelListForComparison))

		for centre in cliqueVoxelCentreList:
			try:
				kStar.remove(centre)
			except:
				pass

		return kStar

	def maskFor2clique(self, centre):
		mask = []
		temp = list(centre)
		# do x coordiinate +- 1
		temp[0] += 1
		mask.append([tuple(temp),centre])
		temp = list(centre)
		temp[0] -= 1
		mask.append([tuple(temp),centre])
		temp = list(centre)
		temp[1] += 1
		mask.append([tuple(temp),centre])
		temp = list(centre)
		temp[1] -= 1
		mask.append([tuple(temp),centre])
		temp = list(centre)
		temp[2] += 1
		mask.append([tuple(temp),centre])
		temp = list(centre)
		temp[2] -= 1
		mask.append([tuple(temp),centre])

		return mask

	def maskFor1clique(self, centre):
		mask = []

		for i in range(1,7):
			# for x
			if i==1:
				temp = list(centre)
				tempxplus = list(centre)
				tempxplus[0] += 1
				temp_up = list(temp)
				tempxplus_up = list(tempxplus)
				temp_up[1] += 1
				tempxplus_up[1] += 1
				temp_down = list(temp)
				tempxplus_down = list(tempxplus)
				temp_down[1] -= 1
				tempxplus_down[1] -= 1
				mask.append([tuple(temp),tuple(tempxplus),tuple(temp_up),tuple(tempxplus_up)])
				mask.append([tuple(temp),tuple(tempxplus),tuple(temp_down),tuple(tempxplus_down)])
			elif i==2:
				temp = list(centre)
				tempxminus = list(centre)
				tempxminus[0] -= 1
				temp_up = list(temp)
				tempxminus_up = list(tempxminus)
				temp_up[1] += 1
				tempxminus_up[1] += 1
				temp_down = list(temp)
				tempxminus_down = list(tempxminus)
				temp_down[1] -= 1
				tempxminus_down[1] -= 1
				mask.append([tuple(temp),tuple(tempxminus),tuple(temp_up),tuple(tempxminus_up)])
				mask.append([tuple(temp),tuple(tempxminus),tuple(temp_down),tuple(tempxminus_down)])

			# for y
			elif i==3:
				temp = list(centre)
				tempyplus = list(centre)
				tempyplus[1] += 1
				temp_front = list(temp)
				temp_back = list(temp)
				tempyplus_front = list(tempyplus)
				temp_front[2] += 1
				tempyplus_front[2] += 1
				temp_down = list(temp)
				tempyplus_back = list(tempyplus)
				temp_back[2] -= 1
				tempyplus_back[2] -= 1
				mask.append([tuple(temp),tuple(tempyplus),tuple(temp_front),tuple(tempyplus_front)])
				mask.append([tuple(temp),tuple(tempyplus),tuple(temp_back),tuple(tempyplus_back)])
			elif i==4:
				temp = list(centre)
				tempyminus = list(centre)
				tempyminus[1] -= 1
				temp_front = list(temp)
				tempyminus_front = list(tempyminus)
				temp_front[2] += 1
				tempyminus_front[2] += 1
				temp_back = list(temp)
				tempyminus_back = list(tempyminus)
				temp_back[2] -= 1
				tempyminus_back[2] -= 1
				mask.append([tuple(temp),tuple(tempyminus),tuple(temp_front),tuple(tempyminus_front)])
				mask.append([tuple(temp),tuple(tempyminus),tuple(temp_back),tuple(tempyminus_back)])

			# for z
			elif i==5:
				temp = list(centre)
				tempzplus = list(centre)
				tempzplus[2] += 1
				temp_up = list(temp)
				tempzplus_up = list(tempzplus)
				temp_up[1] += 1
				tempzplus_up[1] += 1
				temp_down = list(temp)
				tempzplus_down = list(tempzplus)
				temp_down[1] -= 1
				tempzplus_down[1] -= 1
				mask.append([tuple(temp),tuple(tempzplus),tuple(temp_up),tuple(tempzplus_up)])
				mask.append([tuple(temp),tuple(tempzplus),tuple(temp_down),tuple(tempzplus_down)])
			elif i==6:
				temp = list(centre)
				tempzminus = list(centre)
				tempzminus[2] -= 1
				temp_up = list(temp)
				tempzminus_up = list(tempzminus)
				temp_up[1] += 1
				tempzminus_up[1] += 1
				temp_down = list(temp)
				tempzminus_down = list(tempzminus)
				temp_down[1] -= 1
				tempzminus_down[1] -= 1
				mask.append([tuple(temp),tuple(tempzminus),tuple(temp_up),tuple(tempzminus_up)])
				mask.append([tuple(temp),tuple(tempzminus),tuple(temp_down),tuple(tempzminus_down)])

		return mask

	def maskFor0clique(self,centre):
		mask = []
		temp = list(centre)
		tempxplus = list(centre)
		tempxplus[0] += 1
		tempxminus = list(centre)
		tempxminus[0] -= 1
		temp_front = list(temp)
		temp_back = list(temp)
		temp_front[2] += 1
		temp_back[2] -= 1
		temp_front_up = list(temp_front)
		temp_back_up = list(temp_back)
		temp_front_down = list(temp_front)
		temp_back_down = list(temp_back)
		temp_front_up[1] += 1
		temp_back_up[1] += 1
		temp_front_down[1] -= 1
		temp_back_down[1] -= 1
		tempxplus_front = list(tempxplus)
		tempxplus_back = list(tempxplus)
		tempxminus_front = list(tempxminus)
		tempxminus_back = list(tempxminus)
		tempxplus_front[2] += 1
		tempxplus_back[2] -= 1
		tempxminus_front[2] += 1
		tempxminus_back[2] -= 1
		temp_up = list(temp)
		tempxplus_up = list(tempxplus)
		tempxminus_up = list(tempxminus)
		tempxplus_front_up = list(tempxplus_front)
		tempxplus_back_up = list(tempxplus_back)
		tempxminus_front_up = list(tempxminus_front)
		tempxminus_back_up = list(tempxminus_back)
		temp_up[1] += 1
		tempxplus_up[1] += 1
		tempxminus_up[1] += 1
		tempxplus_front_up[1] += 1
		tempxplus_back_up[1] += 1
		tempxminus_front_up[1] += 1
		tempxminus_back_up[1] += 1
		temp_down = list(temp)
		tempxplus_down =  list(tempxplus)
		tempxminus_down =  list(tempxminus)
		tempxplus_front_down =  list(tempxplus_front)
		tempxplus_back_down =  list(tempxplus_back)
		tempxminus_front_down =  list(tempxminus_front)
		tempxminus_back_down =  list(tempxminus_back)
		temp_down[1] -= 1
		tempxplus_down[1] -= 1
		tempxminus_down[1] -= 1
		tempxplus_front_down[1] -= 1
		tempxplus_back_down[1] -= 1
		tempxminus_front_down[1] -= 1
		tempxminus_back_down[1] -= 1

		mask.append([tuple(temp),tuple(tempxplus),tuple(tempxplus_front),tuple(temp_front),tuple(temp_up),tuple(tempxplus_up),tuple(tempxplus_front_up),tuple(temp_front_up)])
		mask.append([tuple(temp),tuple(tempxplus),tuple(tempxplus_front),tuple(temp_front),tuple(temp_down),tuple(tempxplus_down),tuple(tempxplus_front_down),tuple(temp_front_down)])
		mask.append([tuple(temp),tuple(tempxplus),tuple(tempxplus_back),tuple(temp_back),tuple(temp_up),tuple(tempxplus_up),tuple(tempxplus_back_up),tuple(temp_back_up)])
		mask.append([tuple(temp),tuple(tempxplus),tuple(tempxplus_back),tuple(temp_back),tuple(temp_down),tuple(tempxplus_down),tuple(tempxplus_back_down),tuple(temp_back_down)])
		mask.append([tuple(temp),tuple(tempxminus),tuple(tempxminus_front),tuple(temp_front),tuple(temp_up),tuple(tempxminus_up),tuple(tempxminus_front_up),tuple(temp_front_up)])
		mask.append([tuple(temp),tuple(tempxminus),tuple(tempxminus_front),tuple(temp_front),tuple(temp_down),tuple(tempxminus_down),tuple(tempxminus_front_down),tuple(temp_front_down)])
		mask.append([tuple(temp),tuple(tempxminus),tuple(tempxminus_back),tuple(temp_back),tuple(temp_up),tuple(tempxminus_up),tuple(tempxminus_back_up),tuple(temp_back_up)])
		mask.append([tuple(temp),tuple(tempxminus),tuple(tempxminus_back),tuple(temp_back),tuple(temp_down),tuple(tempxminus_down),tuple(tempxminus_back_down),tuple(temp_back_down)])

		return mask

	def maskForAllNeighbours(self,centre):
		if centre in self.maskForAllNeighbours_set:
			return self.maskForAllNeighbours_set[centre]
		temp = list(centre)
		tempxplus = list(centre)
		tempxplus[0] += 1
		tempxminus = list(centre)
		tempxminus[0] -= 1
		temp_front = list(temp)
		temp_back = list(temp)
		temp_front[2] += 1
		temp_back[2] -= 1
		temp_front_up = list(temp_front)
		temp_back_up = list(temp_back)
		temp_front_down = list(temp_front)
		temp_back_down = list(temp_back)
		temp_front_up[1] += 1
		temp_back_up[1] += 1
		temp_front_down[1] -= 1
		temp_back_down[1] -= 1
		tempxplus_front = list(tempxplus)
		tempxplus_back = list(tempxplus)
		tempxminus_front = list(tempxminus)
		tempxminus_back = list(tempxminus)
		tempxplus_front[2] += 1
		tempxplus_back[2] -= 1
		tempxminus_front[2] += 1
		tempxminus_back[2] -= 1
		temp_up = list(temp)
		tempxplus_up = list(tempxplus)
		tempxminus_up = list(tempxminus)
		tempxplus_front_up = list(tempxplus_front)
		tempxplus_back_up = list(tempxplus_back)
		tempxminus_front_up = list(tempxminus_front)
		tempxminus_back_up = list(tempxminus_back)
		temp_up[1] += 1
		tempxplus_up[1] += 1
		tempxminus_up[1] += 1
		tempxplus_front_up[1] += 1
		tempxplus_back_up[1] += 1
		tempxminus_front_up[1] += 1
		tempxminus_back_up[1] += 1
		temp_down = list(temp)
		tempxplus_down =  list(tempxplus)
		tempxminus_down =  list(tempxminus)
		tempxplus_front_down =  list(tempxplus_front)
		tempxplus_back_down =  list(tempxplus_back)
		tempxminus_front_down =  list(tempxminus_front)
		tempxminus_back_down =  list(tempxminus_back)
		temp_down[1] -= 1
		tempxplus_down[1] -= 1
		tempxminus_down[1] -= 1
		tempxplus_front_down[1] -= 1
		tempxplus_back_down[1] -= 1
		tempxminus_front_down[1] -= 1
		tempxminus_back_down[1] -= 1

		mask = [tuple(tempxplus), tuple(tempxminus), tuple(temp_front), tuple(temp_back), tuple(temp_front_up), tuple(temp_back_up), tuple(temp_front_down), tuple(temp_back_down), tuple(tempxplus_front), tuple(tempxplus_back), tuple(tempxminus_front), tuple(tempxminus_back), tuple(temp_up), tuple(tempxplus_up), tuple(tempxminus_up), tuple(tempxplus_front_up), tuple(tempxplus_back_up), tuple(tempxminus_front_up), tuple(tempxminus_back_up), tuple(temp_down), tuple(tempxplus_down), tuple(tempxminus_down), tuple(tempxplus_front_down), tuple(tempxplus_back_down), tuple(tempxminus_front_down), tuple(tempxminus_back_down)]
		self.maskForAllNeighbours_set[centre] = mask
		# f = open('maskForAllNeighbours_set.json', "w")
		# data = json.dumps({'data':str(self.maskForAllNeighbours_set)})
		# f.write(data)
		# f.close()
		return mask

	# def getNeighboursForGivenVoxel(self, centre, voxelCentreList, edgeLength = 1):
	# 	listOfAdjacentVoxels = self.findAllAdjacentVoxelsForGivenVoxel(centre, voxelCentreList, edgeLength)
	# 	final_list = []
	# 	final_list = list(set(final_list).union(set(listOfAdjacentVoxels[0])))
	# 	final_list = list(set(final_list).union(set(listOfAdjacentVoxels[1])))
	# 	final_list = list(set(final_list).union(set(listOfAdjacentVoxels[2])))
	# 	return final_list

	def getNeighboursForGivenVoxel(self, centre, voxelCentreList, edgeLength = 1):
		listOfAdjacentVoxels = self.maskForAllNeighbours(centre)
		final_list = []
		final_list = list(set(voxelCentreList).intersection(set(listOfAdjacentVoxels)))
		return final_list

	def findAllAdjacentVoxelsForGivenVoxel(self, centre, voxelCentreList, edgeLength):
		print "entering findAllAdjacentVoxelsForGivenVoxel"
		# print "centre in findAllAdjacentVoxelsForGivenVoxel", centre
		listOf2AdjacentVoxels = self.findAll2AdjacentVoxelsForGivenVoxel(centre, voxelCentreList, edgeLength)
		listOf1AdjacentVoxels = self.findAll1AdjacentVoxelsForGivenVoxel(centre, voxelCentreList, edgeLength)
		listOf0AdjacentVoxels = self.findAll0AdjacentVoxelsForGivenVoxel(centre, voxelCentreList, edgeLength)
		print "leaving findAllAdjacentVoxelsForGivenVoxel"
		return [listOf2AdjacentVoxels, listOf1AdjacentVoxels, listOf0AdjacentVoxels]

	# Find all the voxels centres that are 2-adjacent to the the given voxel.
	def findAll2AdjacentVoxelsForGivenVoxel(self, centre, voxelCentreList, edgeLength):
		
		flag = False
		# Remove the voxel for whom the neighbours needs to be found, from the complex.
		try:
			voxelCentreList.remove(centre)
			flag = True
		except:
			pass

		listOf2AdjacentVoxels = []

		for voxelCentre in voxelCentreList:
			if self.is2Adjacent(centre, voxelCentre, edgeLength):
				listOf2AdjacentVoxels.append(voxelCentre)
		if flag:
			voxelCentreList.append(centre)
		return listOf2AdjacentVoxels

	# Find all the voxels centres that are 1-adjacent to the the given voxel.
	def findAll1AdjacentVoxelsForGivenVoxel(self, centre, voxelCentreList, edgeLength):

		flag = False
		# Remove the voxel for whom the neighbours needs to be found, from the complex.
		try:
			voxelCentreList.remove(centre)
			flag = True
		except:
			pass

		listOf1AdjacentVoxels = []

		for voxelCentre in voxelCentreList:
			if self.is1Adjacent(centre, voxelCentre, edgeLength):
				listOf1AdjacentVoxels.append(voxelCentre)

		if flag:
			voxelCentreList.append(centre)

		return listOf1AdjacentVoxels
			
	# Find all the voxels centres that are 2-adjacent to the the given voxel.
	def findAll0AdjacentVoxelsForGivenVoxel(self, centre, voxelCentreList, edgeLength):

		flag = False
		# Remove the voxel for whom the neighbours needs to be found, from the complex.
		try:
			voxelCentreList.remove(centre)
			flag = True
		except:
			pass

		listOf0AdjacentVoxels = []

		for voxelCentre in voxelCentreList:
			if self.is0Adjacent(centre, voxelCentre, edgeLength):
				listOf0AdjacentVoxels.append(voxelCentre)

		if flag:
			voxelCentreList.append(centre)

		return listOf0AdjacentVoxels

	# def extractEssential(self):
	# 	pass

	# def isRegular():
	# 	pass

	# def isCritical():
	# 	pass

	# Given two voxel centres, find if they are 2-adjacent or not.
	def is2Adjacent(self, centre1, centre2, edgeLength):

		centre1 = list(centre1)
		centre2 = list(centre2)
		c1 = np.array(centre1)
		c2 = np.array(centre2)
		# print c1,c2
		distanceBetweenCentres = np.linalg.norm(c1-c2)

		if self.isClose(edgeLength, distanceBetweenCentres):
			return True

		return False

	# Given two voxel centres, find if they are 1-adjacent or not.
	def is1Adjacent(self, centre1, centre2, edgeLength):

		c1 = np.array(list(centre1))
		c2 = np.array(list(centre2))

		distanceBetweenCentres = np.linalg.norm(c1-c2)
		
		centreToEdge = self.centreToEdgeDistance(edgeLength)
		
		if self.isClose(centreToEdge, distanceBetweenCentres/2.0):
			return True

		return False

	# Given two voxel centres, find if they are 0-adjacent or not.
	def is0Adjacent(self, centre1, centre2, edgeLength):

		c1 = np.array(list(centre1))
		c2 = np.array(list(centre2))

		distanceBetweenCentres = np.linalg.norm(c1-c2)

		centreToCorner = self.centreToCornerDistance(edgeLength)

		if self.isClose(centreToCorner, distanceBetweenCentres/2.0):
			return True

		return False

	# Given the edge length of a voxel, calculate the shortest distance from the centre of a voxel to the edge.
	def centreToEdgeDistance(self, edgeLength):

		return edgeLength/np.sqrt(2.0)

	# Given the edge length of a voxel, calculate the distance from the centre of a voxel to a corner.
	def centreToCornerDistance(self, edgeLength):
		
		return (edgeLength/2.0)*np.sqrt(3.0)

	# Check if the given complex is connected or not
	# def isConnected(self, voxelCentreList, edgeLength=1):
	# 	if len(voxelCentreList) == 1:
	# 		return True
	# 	for centre in voxelCentreList:
	# 		if self.findAll2AdjacentVoxelsForGivenVoxel(centre, voxelCentreList, edgeLength)==[] and self.findAll1AdjacentVoxelsForGivenVoxel(centre, voxelCentreList, edgeLength)==[] and self.findAll0AdjacentVoxelsForGivenVoxel(centre, voxelCentreList, edgeLength)==[]:
	# 			return False
	# 	return True

	def isConnected(self, voxelCentreList, edgeLength=1):
		if frozenset(voxelCentreList) in self.isConnected_set:
			return self.isConnected_set[frozenset(voxelCentreList)]
		if len(voxelCentreList) == 1:
			self.isConnected_set[frozenset(voxelCentreList)] = True
			# f = open('isConnected_set.json', "w")
			# data = json.dumps({'data':str(self.isConnected_set)})
			# f.write(data)
			# f.close()
			return True
		for centre in voxelCentreList:
			if list(set(self.maskForAllNeighbours(centre)).intersection(set(voxelCentreList)))==[]:
				self.isConnected_set[frozenset(voxelCentreList)] = False
				# f = open('isConnected_set.json', "w")
				# data = json.dumps({'data':str(self.isConnected_set)})
				# f.write(data)
				# f.close()
				return False
		self.isConnected_set[frozenset(voxelCentreList)] = True
		# f = open('isConnected_set.json', "w")
		# data = json.dumps({'data':str(self.isConnected_set)})
		# f.write(data)
		# f.close()
		return True

	def generatePowerSet(self, lst):
		return reduce(lambda result, x: result + [subset + [x] for subset in result], lst, [[]])

	# Compare two floating point numbers for almost-equality
	def isClose(self, a, b, rel_tol=1e-09, abs_tol=0.0):
		return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

	def buildComplexFromPyFile(self, list):
		voxelCentreList = []
		for voxelDict in list:
			voxelCentreList.append((voxelDict['x'],voxelDict['y'],voxelDict['z']))
		print 'complex built: ', voxelCentreList	
		return voxelCentreList


	def tester(self, complex):
		simple_voxels = self.getSimpleVoxels(list(complex))
		for voxel in simple_voxels:
			temp = list(complex)
			temp.remove(voxel)
			if self.isConnected(temp):
				complex.remove(voxel)
		return complex








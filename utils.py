import numpy as np
import itertools

class Utils():
	
	def __init__(self):
		self.supportVectorList = [[1,1,1], [-1,1,1], [-1,-1,1], [1,-1,1], [1,1,-1], [-1,1,-1], [-1,-1,-1], [1,-1,-1],]

	# Given a list of centres as tuples, generate the vertices for all the voxels.
	def generateVerticesForCentres(self, voxelCentreList, edgeLength):

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

		print vertexListForAllCentres

	# def findAllCliquesForComplex(self, voxelCentreList, edgeLength):
	# 	powerSet = self.generatePowerSet(voxelCentreList)
	# 	powerSet.remove([])
	# 	cliqueList = [clique for clique in powerSet if self.isConnected(clique, edgeLength)]
	# 	return cliqueList
	def getSimpleVoxels(self, voxelCentreList):
		simple_voxels = []
		for voxel in voxelCentreList:
			if self.isReducible(self.getNeighboursForGivenVoxel(voxel, voxelCentreList)):
				simple_voxels.append(voxel)
		simple_voxels.sort()
		simple_voxels = list(simple_voxels for simple_voxels,_ in itertools.groupby(simple_voxels))
		return simple_voxels

	def isZeroSurface(self, voxelCentreList):
		if not len(voxelCentreList)==2:
			return False
		if self.isConnected(voxelCentreList):
			return False

		return True

	def isOneSurface(self, voxelCentreList):
		
		if not self.isConnected(voxelCentreList):
			return False
		for voxel in voxelCentreList:
			if not self.isZeroSurface(self.getNeighboursForGivenVoxel(voxel, voxelCentreList)):
				return False
		return True

	def isCritical(self, cliqueVoxelCentreList, voxelCentreList):
		
		isRegular = self.isReducible(self.findKStarForClique(cliqueVoxelCentreList, voxelCentreList))
		if not isRegular:
			return True
		return False

	def isReducible(self, voxelCentreList):
		if len(voxelCentreList) == 1:
			return True
		for voxel in voxelCentreList:
			print "voxel in isReducible", voxel
			temp = list(voxelCentreList)
			temp.remove(voxel)
			isNeighboursReducible = self.isReducible(self.getNeighboursForGivenVoxel(voxel, voxelCentreList))
			isOthersReducible = self.isReducible(temp)
			print "isNeighboursReducible",isNeighboursReducible, "isOthersReducible",isOthersReducible
			if isNeighboursReducible and isOthersReducible:
				return True
		return False

	def getKCriticalCliques(self, voxelCentreList, k):
		essentialCliques = self.findEssentialCliquesForComplex(voxelCentreList)
		# simple_voxels = self.getSimpleVoxels(voxelCentreList)
		simple_voxels = [(0,0,0),(2,0,-1)]
		print "simple_voxels", simple_voxels
		k_critical_cliques = []
		cliques_combined = []
		cliques_combined = list(essentialCliques['three_cliques']) + list(essentialCliques['two_cliques']) + list(essentialCliques['one_cliques']) + list(essentialCliques['zero_cliques'])
		print 'cliques_combined', cliques_combined
		for clique in cliques_combined:
			
			temp = list(clique)
			for voxel in temp:
				if voxel in simple_voxels:
					temp.remove(voxel)

			if k == 1:
				
				if self.isZeroSurface(temp):
					k_critical_cliques.append(clique)
			if k == 2:
				
				if self.isOneSurface(temp):
					k_critical_cliques.append(clique)
			if k == 3:
				
				if self.isZeroSurface(temp) or self.isOneSurface(temp):
					k_critical_cliques.append(clique)
		return k_critical_cliques

	def findCriticalCliques(self, voxelCentreList):
		essentialCliques = self.findEssentialCliquesForComplex(voxelCentreList)
		
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
		essentialCliques['two_cliques'] = two_cliques
		essentialCliques['one_cliques'] = one_cliques
		essentialCliques['zero_cliques'] = zero_cliques

		return essentialCliques

	def findEssentialCliquesForComplex(self, voxelCentreList):

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

			# check for zero cliques
			for mask in self.maskFor0clique(centre):
				common = list(set(mask).intersection(set(voxelCentreList)))
				if len(common)>4:
					# zero_cliques = list(set(zero_cliques).union(set(common)))
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
				temp_up = temp
				tempxplus_up = tempxplus
				temp_up[1] += 1
				tempxplus_up[1] += 1
				temp_down = temp
				tempxplus_down = tempxplus
				temp_down[1] -= 1
				tempxplus_down[1] -= 1
				mask.append([tuple(temp),tuple(tempxplus),tuple(temp_up),tuple(tempxplus_up)])
				mask.append([tuple(temp),tuple(tempxplus),tuple(temp_down),tuple(tempxplus_down)])
			elif i==2:
				temp = list(centre)
				tempxminus = list(centre)
				tempxminus[0] -= 1
				temp_up = temp
				tempxminus_up = tempxminus
				temp_up[1] += 1
				tempxminus_up[1] += 1
				temp_down = temp
				tempxminus_down = tempxminus
				temp_down[1] -= 1
				tempxminus_down[1] -= 1
				mask.append([tuple(temp),tuple(tempxminus),tuple(temp_up),tuple(tempxminus_up)])
				mask.append([tuple(temp),tuple(tempxminus),tuple(temp_down),tuple(tempxminus_down)])

			# for y
			elif i==3:
				temp = list(centre)
				tempyplus = list(centre)
				tempyplus[1] += 1
				temp_front = temp
				temp_back = temp
				tempyplus_front = tempyplus
				temp_front[2] += 1
				tempyplus_front[2] += 1
				temp_down = temp
				tempyplus_back = tempyplus
				temp_back[2] -= 1
				tempyplus_back[2] -= 1
				mask.append([tuple(temp),tuple(tempyplus),tuple(temp_front),tuple(tempyplus_front)])
				mask.append([tuple(temp),tuple(tempyplus),tuple(temp_back),tuple(tempyplus_back)])
			elif i==4:
				temp = list(centre)
				tempyminus = list(centre)
				tempyminus[1] -= 1
				temp_front = temp
				tempyminus_front = tempyminus
				temp_front[2] += 1
				tempyminus_front[2] += 1
				temp_back = temp
				tempyminus_back = tempyminus
				temp_back[2] -= 1
				tempyminus_back[2] -= 1
				mask.append([tuple(temp),tuple(tempyminus),tuple(temp_front),tuple(tempyminus_front)])
				mask.append([tuple(temp),tuple(tempyminus),tuple(temp_back),tuple(tempyminus_back)])

			# for z
			elif i==5:
				temp = list(centre)
				tempzplus = list(centre)
				tempzplus[2] += 1
				temp_up = temp
				tempzplus_up = tempzplus
				temp_up[1] += 1
				tempzplus_up[1] += 1
				temp_down = temp
				tempzplus_down = tempzplus
				temp_down[1] -= 1
				tempzplus_down[1] -= 1
				mask.append([tuple(temp),tuple(tempzplus),tuple(temp_up),tuple(tempzplus_up)])
				mask.append([tuple(temp),tuple(tempzplus),tuple(temp_down),tuple(tempzplus_down)])
			elif i==6:
				temp = list(centre)
				tempzminus = list(centre)
				tempzminus[2] -= 1
				temp_up = temp
				tempzminus_up = tempzminus
				temp_up[1] += 1
				tempzminus_up[1] += 1
				temp_down = temp
				tempzminus_down = tempzminus
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
		temp_front = temp
		temp_back = temp
		temp_front[2] += 1
		temp_back[2] -= 1
		temp_front_up = temp_front
		temp_back_up = temp_back
		temp_front_down = temp_front
		temp_back_down = temp_back
		temp_front_up[1] += 1
		temp_back_up[1] += 1
		temp_front_down[1] -= 1
		temp_back_down[1] -= 1
		tempxplus_front = tempxplus
		tempxplus_back = tempxplus
		tempxminus_front = tempxminus
		tempxminus_back = tempxminus
		tempxplus_front[2] += 1
		tempxplus_back[2] -= 1
		tempxminus_front[2] += 1
		tempxminus_back[2] -= 1
		temp_up = temp
		tempxplus_up = tempxplus
		tempxminus_up = tempxminus
		tempxplus_front_up = tempxplus_front
		tempxplus_back_up = tempxplus_back
		tempxminus_front_up = tempxminus_front
		tempxminus_back_up = tempxminus_back
		temp_up[1] += 1
		tempxplus_up[1] += 1
		tempxminus_up[1] += 1
		tempxplus_front_up[1] += 1
		tempxplus_back_up[1] += 1
		tempxminus_front_up[1] += 1
		tempxminus_back_up[1] += 1
		temp_down = temp
		tempxplus_down =  tempxplus
		tempxminus_down =  tempxminus
		tempxplus_front_down =  tempxplus_front
		tempxplus_back_down =  tempxplus_back
		tempxminus_front_down =  tempxminus_front
		tempxminus_back_down =  tempxminus_back
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

	def getNeighboursForGivenVoxel(self, centre, voxelCentreList, edgeLength = 1):
		listOfAdjacentVoxels = self.findAllAdjacentVoxelsForGivenVoxel(centre, voxelCentreList, edgeLength)
		final_list = []
		final_list = list(set(final_list).union(set(listOfAdjacentVoxels[0])))
		final_list = list(set(final_list).union(set(listOfAdjacentVoxels[1])))
		final_list = list(set(final_list).union(set(listOfAdjacentVoxels[2])))
		return final_list
	def findAllAdjacentVoxelsForGivenVoxel(self, centre, voxelCentreList, edgeLength):
		# print "centre in findAllAdjacentVoxelsForGivenVoxel", centre
		listOf2AdjacentVoxels = self.findAll2AdjacentVoxelsForGivenVoxel(centre, voxelCentreList, edgeLength)
		listOf1AdjacentVoxels = self.findAll1AdjacentVoxelsForGivenVoxel(centre, voxelCentreList, edgeLength)
		listOf0AdjacentVoxels = self.findAll0AdjacentVoxelsForGivenVoxel(centre, voxelCentreList, edgeLength)

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
	def isConnected(self, voxelCentreList, edgeLength=1):
		if len(voxelCentreList) == 1:
			return True
		for centre in voxelCentreList:
			if self.findAll2AdjacentVoxelsForGivenVoxel(centre, voxelCentreList, edgeLength)==[] and self.findAll1AdjacentVoxelsForGivenVoxel(centre, voxelCentreList, edgeLength)==[] and self.findAll0AdjacentVoxelsForGivenVoxel(centre, voxelCentreList, edgeLength)==[]:
				return False
		return True

	def generatePowerSet(self, lst):
		return reduce(lambda result, x: result + [subset + [x] for subset in result], lst, [[]])

	# Compare two floating point numbers for almost-equality
	def isClose(self, a, b, rel_tol=1e-09, abs_tol=0.0):
		return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)
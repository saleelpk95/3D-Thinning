import numpy as np

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

	def findAllCliquesForComplex(self, voxelCentreList, edgeLength):
		powerSet = self.generatePowerSet(voxelCentreList)
		powerSet.remove([])
		cliqueList = [clique for clique in powerSet if self.isConnected(clique, edgeLength)]
		return cliqueList

	def findKStarForClique(self, cliqueVoxelCentreList, voxelCentreList, edgeLength):
		kStar = []
		flag = True
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

	def findAllAdjacentVoxelsForGivenVoxel(self, centre, voxelCentreList, edgeLength):

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

	# Given two voxel centres, find if they are 2-adjacent or not.
	def is2Adjacent(self, centre1, centre2, edgeLength):

		c1 = np.array(centre1)
		c2 = np.array(centre2)

		distanceBetweenCentres = np.linalg.norm(c1-c2)

		if self.isClose(edgeLength, distanceBetweenCentres):
			return True

		return False

	# Given two voxel centres, find if they are 1-adjacent or not.
	def is1Adjacent(self, centre1, centre2, edgeLength):

		c1 = np.array(centre1)
		c2 = np.array(centre2)

		distanceBetweenCentres = np.linalg.norm(c1-c2)
		
		centreToEdge = self.centreToEdgeDistance(edgeLength)
		
		if self.isClose(centreToEdge, distanceBetweenCentres/2.0):
			return True

		return False

	# Given two voxel centres, find if they are 0-adjacent or not.
	def is0Adjacent(self, centre1, centre2, edgeLength):

		c1 = np.array(centre1)
		c2 = np.array(centre2)

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
	def isConnected(self, voxelCentreList, edgeLength):
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
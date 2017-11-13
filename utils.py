import numpy as np
import itertools
import json

class Utils():
	
	def __init__(self):
		self.supportVectorList = [[1,1,1], [-1,1,1], [-1,-1,1], [1,-1,1], [1,1,-1], [-1,1,-1], [-1,-1,-1], [1,-1,-1],]
		self.complexGlobal = []

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

		isReducible_set_json = open('isReducible_set.json')
		isReducible_set_json_str = isReducible_set_json.read()
		self.isReducible_set = eval(json.loads(isReducible_set_json_str)['data'])

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

	def generateCornerVertices(self, voxelCentreList, edgeLength=1):

		vertexListForAllCentres = []

		for centre in voxelCentreList:
		
			vertexListForOneCentre = {}
			vertexListForOneCentre['min'] = tuple(np.subtract(centre, (0.5, 0.5, 0.5)))
			vertexListForOneCentre['max'] = tuple(np.add(centre, (0.5, 0.5, 0.5)))
			

			vertexListForAllCentres.append(vertexListForOneCentre)

		return vertexListForAllCentres

	def buildObjFile(self, voxelCentreList, filename):

		s = 0
		list_for_print_voxel = []
		list_for_print_faces = []
		for voxel in voxelCentreList:
			print voxel

			i = voxel[0]
			j = voxel[1]
			k = voxel[2]
			list_for_print_voxel.append( ("v %d %d %d\n" %(i,j,k)));
			list_for_print_voxel.append( ("v %d %d %d\n" %(i,j,k+1)));
			list_for_print_voxel.append( ("v %d %d %d\n" %(i,j+1,k)));
			list_for_print_voxel.append( ("v %d %d %d\n" %(i,j+1,k+1)));
			list_for_print_voxel.append( ("v %d %d %d\n" %(i+1,j,k)));
			list_for_print_voxel.append( ("v %d %d %d\n" %(i+1,j,k+1)));
			list_for_print_voxel.append( ("v %d %d %d\n" %(i+1,j+1,k)));
			list_for_print_voxel.append( ("v %d %d %d\n" %(i+1,j+1,k+1)));
			list_for_print_faces.append( ("f %ld %ld %ld %ld\n" %(s+8,s+4,s+2,s+6)));
			list_for_print_faces.append( ("f %ld %ld %ld %ld\n" %(s+8,s+6,s+5,s+7)));
			list_for_print_faces.append( ("f %ld %ld %ld %ld\n" %(s+8,s+7,s+3,s+4)));
			list_for_print_faces.append( ("f %ld %ld %ld %ld\n" %(s+4,s+3,s+1,s+2)));
			list_for_print_faces.append( ("f %ld %ld %ld %ld\n" %(s+1,s+3,s+7,s+5)));
			list_for_print_faces.append( ("f %ld %ld %ld %ld\n" %(s+2,s+1,s+5,s+6)));
			s+=8;

		file = open('./visualize/'+filename+'.obj', 'w+')

		file.write("#"+filename+'.obj')
		file.write("\n")
		file.write("g "+filename)
		file.write("\n")
		for vertex in list_for_print_voxel:
			file.write("%s" % vertex)
		file.write("\n")

		for face in list_for_print_faces:
			file.write("%s\n" % face)

		file.close()

	# def buildObjFile(self, voxelCentreList, filename):
	# 	vertex_obj = []
	# 	face_obj = []
	# 	normal_obj = ["vn  1.0  0.0  0.0", "vn -1.0  0.0  0.0", "vn  0.0  1.0  0.0", "vn  0.0 -1.0  0.0", "vn  0.0  0.0  1.0", "vn  0.0  0.0 -1.0"]
	# 	i = 1
	# 	for voxel in voxelCentreList:
	# 		vertex_1 = voxel['min']
	# 		vertex_2 = tuple(np.add(vertex_1, (1, 0, 0)))
	# 		vertex_3 = tuple(np.add(vertex_1, (0, 1, 0)))
	# 		vertex_4 = tuple(np.add(vertex_1, (1, 1, 0)))
	# 		vertex_5 = tuple(np.add(vertex_1, (0, 0, 1)))
	# 		vertex_6 = tuple(np.add(vertex_1, (1, 0, 1)))
	# 		vertex_7 = tuple(np.add(vertex_1, (0, 1, 1)))
	# 		vertex_8 = voxel['max']

	# 		vertex_obj.append("v " + str(vertex_1[0]) + " " + str(vertex_1[1]) + " " + str(vertex_1[2]))
	# 		vertex_obj.append("v " + str(vertex_2[0]) + " " + str(vertex_2[1]) + " " + str(vertex_2[2]))
	# 		vertex_obj.append("v " + str(vertex_3[0]) + " " + str(vertex_3[1]) + " " + str(vertex_3[2]))
	# 		vertex_obj.append("v " + str(vertex_4[0]) + " " + str(vertex_4[1]) + " " + str(vertex_4[2]))
	# 		vertex_obj.append("v " + str(vertex_5[0]) + " " + str(vertex_5[1]) + " " + str(vertex_5[2]))
	# 		vertex_obj.append("v " + str(vertex_6[0]) + " " + str(vertex_6[1]) + " " + str(vertex_6[2]))
	# 		vertex_obj.append("v " + str(vertex_7[0]) + " " + str(vertex_7[1]) + " " + str(vertex_7[2]))
	# 		vertex_obj.append("v " + str(vertex_8[0]) + " " + str(vertex_8[1]) + " " + str(vertex_8[2]))

	# 		face_1 = "f " + str(i) + "//" + str(6) + " " + str(i+1) + "//" + str(6) + " " + str(i+2) + "//" + str(6) 
	# 		face_2 = "f " + str(i+1) + "//" + str(6) + " " + str(i+2) + "//" + str(6) + " " + str(i+3) + "//" + str(6)
	# 		face_3 = "f " + str(i) + "//" + str(2) + " " + str(i+4) + "//" + str(2) + " " + str(i+2) + "//" + str(2)
	# 		face_4 = "f " + str(i+2) + "//" + str(2) + " " + str(i+4) + "//" + str(2) + " " + str(i+6) + "//" + str(2)
	# 		face_5 = "f " + str(i) + "//" + str(4) + " " + str(i+1) + "//" + str(4) + " " + str(i+4) + "//" + str(4)
	# 		face_6 = "f " + str(i+1) + "//" + str(4) + " " + str(i+4) + "//" + str(4) + " " + str(i+5) + "//" + str(4)
	# 		face_7 = "f " + str(i+7) + "//" + str(3) + " " + str(i+3) + "//" + str(3) + " " + str(i+6) + "//" + str(3) 
	# 		face_8 = "f " + str(i+3) + "//" + str(3) + " " + str(i+6) + "//" + str(3) + " " + str(i+2) + "//" + str(3) 
	# 		face_9 = "f " + str(i+7) + "//" + str(1) + " " + str(i+5) + "//" + str(1) + " " + str(i+1) + "//" + str(1) 
	# 		face_10 = "f " + str(i+7) + "//" + str(1) + " " + str(i+1) + "//" + str(1) + " " + str(i+3) + "//" + str(1) 
	# 		face_11 = "f " + str(i+7) + "//" + str(5) + " " + str(i+4) + "//" + str(5) + " " + str(i+5) + "//" + str(5) 
	# 		face_12 = "f " + str(i+7) + "//" + str(5) + " " + str(i+4) + "//" + str(5) + " " + str(i+6) + "//" + str(5) 

	# 		face_obj.append(face_1)
	# 		face_obj.append(face_2)
	# 		face_obj.append(face_3)
	# 		face_obj.append(face_4)
	# 		face_obj.append(face_5)
	# 		face_obj.append(face_6)
	# 		face_obj.append(face_7)
	# 		face_obj.append(face_8)
	# 		face_obj.append(face_9)
	# 		face_obj.append(face_10)
	# 		face_obj.append(face_11)
	# 		face_obj.append(face_12)

	# 		i += 8
		# file = open('./visualize/'+filename+'.obj', 'w+')

		# file.write("#"+filename+'.obj')
		# file.write("\n")
		# file.write("g "+filename)
		# file.write("\n")
		# for vertex in vertex_obj:
		# 	file.write("%s\n" % vertex)
		# file.write("\n")

	# 	for normal in normal_obj:
	# 		file.write("%s\n" % normal)
	# 	file.write("\n")

		# for face in face_obj:
		# 	file.write("%s\n" % face)

		# file.close()

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

		f = open('isReducible_set.json', "w")
		data = json.dumps({'data':str(self.isReducible_set)})
		f.write(data)
		f.close()

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

	def clearAllLookupFiles(self):
		f = open('simple_voxels_set.json', "w")
		data = json.dumps({'data':"{}"})
		f.write(data)
		f.close()

		f = open('isCritical_voxel_set.json', "w")
		data = json.dumps({'data':"{}"})
		f.write(data)
		f.close()

		f = open('isReducible_set.json', "w")
		data = json.dumps({'data':"{}"})
		f.write(data)
		f.close()

		f = open('kCriticalCliques_set.json', "w")
		data = json.dumps({'data':"{}"})
		f.write(data)
		f.close()

		f = open('criticalCliques_set.json', "w")
		data = json.dumps({'data':"{}"})
		f.write(data)
		f.close()

		f = open('essentialCliques_set.json', "w")
		data = json.dumps({'data':"{}"})
		f.write(data)
		f.close()

		# f = open('maskForAllNeighbours_set.json', "w")
		# data = json.dumps({'data':"{}"})
		# f.write(data)
		# f.close()

		f = open('isConnected_set.json', "w")
		data = json.dumps({'data':"{}"})
		f.write(data)
		f.close()

		self.simple_voxels_set = {}
		self.isCritical_voxel_set = {}
		self.maskForAllNeighbours_set = {}
		self.isConnected_set = {}
		self.essentialCliques_set = {}
		self.criticalCliques_set = {}
		self.kCriticalCliques_set = {}

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
		print "simple_voxels",simple_voxels
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
		if frozenset(voxelCentreList) in self.isReducible_set:
			return self.isReducible_set[frozenset(voxelCentreList)]
		print "isReducible voxelCentreList",voxelCentreList
		if len(voxelCentreList) == 1:
			self.isReducible_set[frozenset(voxelCentreList)] = True
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
				self.isReducible_set[frozenset(voxelCentreList)] = True
				# f = open('isReducible_set.json', "w")
				# data = json.dumps({'data':str(self.isReducible_set)})
				# f.write(data)
				# f.close()
				return True
			self.isReducible_set[frozenset(voxelCentreList)] = False
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
			temp_for_removal = list(self.findKStarForClique(list(clique),list(voxelCentreList)))
			print "kStar for clique",temp
			for voxel in temp_for_removal:
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
		simple_voxels = self.getSimpleVoxels(list(voxelCentreList))
		print "simple_voxels",simple_voxels
		
		critical_cliques = essentialCliques
		
		zero_cliques = list(essentialCliques['zero_cliques'])
		one_cliques = list(essentialCliques['one_cliques'])
		two_cliques = list(essentialCliques['two_cliques'])
		three_cliques = list(essentialCliques['three_cliques'])
		zero_cliques_temp = list(essentialCliques['zero_cliques'])
		one_cliques_temp = list(essentialCliques['one_cliques'])
		two_cliques_temp = list(essentialCliques['two_cliques'])
		three_cliques_temp = list(essentialCliques['three_cliques'])
		for clique in zero_cliques_temp:
			if not self.isCritical(clique, voxelCentreList):
				zero_cliques.remove(clique)
		for clique in one_cliques_temp:
			if not self.isCritical(clique, voxelCentreList):
				one_cliques.remove(clique)
		for clique in two_cliques_temp:
			if not self.isCritical(clique, voxelCentreList):
				two_cliques.remove(clique)
		for clique in three_cliques_temp:
			print "clique for three_cliques",clique
			if clique[0] in simple_voxels:
				three_cliques.remove(clique)
		critical_cliques['three_cliques'] = three_cliques
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
			# print "kStar centre",centre
			voxelListForComparison = []
			adjacentVoxels = self.getNeighboursForGivenVoxel(centre, voxelCentreList)
			# print "kStar adjacentVoxels",adjacentVoxels
			# print "kStar flag",flag
			if flag:
				flag = False
				# for voxels in adjacentVoxels:
				kStar += adjacentVoxels
			else:
				# for voxels in adjacentVoxels:
				voxelListForComparison += adjacentVoxels
				kStar = list(set(kStar).intersection(set(voxelListForComparison)))

		for centre in cliqueVoxelCentreList:
			try:
				kStar.remove(centre)
			except:
				pass
		print "kStar for clique ",cliqueVoxelCentreList," is ", kStar
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
		# print "centre",centre
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
		# print "getNeighboursForGivenVoxel centre",centre
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

	def process_output(self, complex):
		return self.processThinning(complex)

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


	def processThinning(self, complex):
		simple_voxels = self.getSimpleVoxels(list(complex))
		for voxel in simple_voxels:
			temp = list(complex)
			temp.remove(voxel)
			if self.isConnected(temp):
				complex.remove(voxel)
		return complex
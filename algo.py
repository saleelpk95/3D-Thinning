from utils import Utils
import time
import itertools

class Algorithms():
	def __init__(self):
		self.util = Utils()

	def crucial_isthmus(self, X, K, k):
		print "entering crucial_isthmus complex",X
		Y = K
		Z = []
		A = []
		B = []
		cliques = []
		criticalCliques = self.util.findCriticalCliques(list(X))
		print "criticalCliques",criticalCliques
		k_critical_cliques = self.util.getKCriticalCliques(list(X), k)
		print "k_critical_cliques",k_critical_cliques
		self.util.buildObjFile(list(X),"finalX-"+str(time.time()))
		self.util.buildObjFile(list(K),"finalK-"+str(time.time()))
		for d in range(3,-1,-1):
			if d == 3:
				cliques = list(criticalCliques['three_cliques'])
			elif d == 2:
				cliques = list(criticalCliques['two_cliques'])
			elif d == 1:
				cliques = list(criticalCliques['one_cliques'])
			elif d == 0:
				cliques = list(criticalCliques['zero_cliques'])
			# print "d = ",d," cliques are ",cliques
			# cliqueSet = [item for sublist in cliques for item in sublist]
			# cliqueSet.sort()
			# cliqueSet = list(cliqueSet for cliqueSet,_ in itertools.groupby(cliqueSet))
			print "cliques",cliques
			# print "cliqueSet", cliqueSet
			print "set(list(X))",set(list(X))
			print "set(Y)",set(Y)
			print "set(list(X)) - set(Y)", set(list(X)) - set(Y)

			for clique in cliques:
				voxel_intersection = set(list(clique))&(set(list(X)) - set(Y))
				if set(clique) == set(voxel_intersection):
					A = list(set(A).union(set(clique)))
			# A = set(list(cliqueSet))&(set(list(X)) - set(Y))
			# self.util.buildObjFile(self.util.generateCornerVertices(list(A)),str(time.time()))
			print "A",A
			# kCriticalCliqueSet = [item for sublist in k_critical_cliques for item in sublist]
			# kCriticalCliqueSet.sort()
			# kCriticalCliqueSet = list(kCriticalCliqueSet for kCriticalCliqueSet,_ in itertools.groupby(kCriticalCliqueSet))
			for clique in k_critical_cliques:
				voxel_intersection = set(list(clique))&(set(list(X)) - set(Y))
				if set(clique) == set(voxel_intersection):
					B = list(set(B).union(set(clique)))
			# B = set(kCriticalCliqueSet)&(set(list(X)) - set(Y))

			Y = list(set(Y).union(A))
			# self.util.buildObjFile(self.util.generateCornerVertices(list(Y)),str(time.time()))
			Z = list(set(Z).union(B))
			self.util.buildObjFile(list(Y),"finalY-"+str(time.time()))
			self.util.buildObjFile(list(Z),"finalZ-"+str(time.time()))
		self.util.updateAllLookupFiles()
		print "Y, z", Y,Z
		return Y, Z

	def isthmus_sym_thinning(self, X, k):
		K = []
		Y = []
		self.util.complexGlobal = list(X)
		# self.util.buildObjFile(list(X),"final-"+str(time.time()))
		crucial_isthmus = self.crucial_isthmus(X, K, k)
		print "crucial_isthmus",crucial_isthmus
		print "set(Y)",set(Y)
		print set(Y) != set(crucial_isthmus[0])
		while set(Y) != set(crucial_isthmus[0]):
			print "inside loop"
			Y = crucial_isthmus[0]
			Z = crucial_isthmus[1]
			# self.util.buildObjFile(list(Y),"final-"+str(time.time()))
			# self.util.buildObjFile(list(Z),"final-"+str(time.time()))
			X = list(Y)
			# self.util.buildObjFile(self.util.generateCornerVertices(list(X)),str(time.time()))
			K = list(set(K).union(set(Z)))
			crucial_isthmus = self.crucial_isthmus(X, K, k)
		print "crucial_isthmus",crucial_isthmus[0]
		# X = self.util.process_output(self.util.complexGlobal)
		print "set(Y)",set(Y)
		print set(Y) != set(crucial_isthmus[0])
		print "X",X
		# self.util.buildObjFile(list(X),str(time.time()))
		return X





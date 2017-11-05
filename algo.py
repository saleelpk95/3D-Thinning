from utils import Utils
import itertools

class Algorithms():
	def __init__(self):
		self.util = Utils()

	def crucial_isthmus(self, X, K, k):
		Y = K
		Z = []
		A = []
		B = []
		cliques = []
		criticalCliques = self.util.findCriticalCliques(list(X))
		print "criticalCliques",criticalCliques
		k_critical_cliques = self.util.getKCriticalCliques(list(X), k)
		print "k_critical_cliques",k_critical_cliques
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
			cliqueSet = [item for sublist in cliques for item in sublist]
			cliqueSet.sort()
			cliqueSet = list(cliqueSet for cliqueSet,_ in itertools.groupby(cliqueSet))
			# for clique in cliques:
			# 	# convert to list while returning
			A = set(list(cliqueSet))&(set(list(X)) - set(Y))
			print "A",A
			kCriticalCliqueSet = [item for sublist in k_critical_cliques for item in sublist]
			kCriticalCliqueSet.sort()
			kCriticalCliqueSet = list(kCriticalCliqueSet for kCriticalCliqueSet,_ in itertools.groupby(kCriticalCliqueSet))
			# for clique in k_critical_cliques:
			B = set(kCriticalCliqueSet)&(set(list(X)) - set(Y))

			Y = list(set(Y).union(A))
			Z = list(set(Z).union(B))
		self.util.updateAllLookupFiles()
		print "Y, z", Y,Z
		return Y, Z

	def isthmus_sym_thinning(self, X, k):
		K = []
		Y = []
		crucial_isthmus = self.crucial_isthmus(X, K, k)
		print "crucial_isthmus",crucial_isthmus[0]
		print "set(Y)",set(Y)
		print set(Y) != set(crucial_isthmus[0])
		while set(Y) != set(crucial_isthmus[0]):
			print "inside loop"
			Y = crucial_isthmus[0]
			Z = crucial_isthmus[1]
			X = list(Y)
			K = list(set(K).union(set(Z)))
			crucial_isthmus = self.crucial_isthmus(X, K, k)
		print "crucial_isthmus",crucial_isthmus[0]
		print "set(Y)",set(Y)
		print set(Y) != set(crucial_isthmus[0])
		print "X",X
		return X





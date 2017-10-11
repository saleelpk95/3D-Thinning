from utils import Utils

class Algorithms():
	def __init__(self):
		self.util = Utils()

	def crucial_isthmus(self, X, K, k):
		Y = K
		Z = []
		A=[]
		B=[]
		criticalCliques = self.util.findCriticalCliques(X)
		print "criticalCliques",criticalCliques
		k_critical_cliques = self.util.getKCriticalCliques(X, k)
		print "k_critical_cliques",k_critical_cliques
		for d in range(3,-1,-1):
			if d == 3:
				cliques = criticalCliques['three_cliques']
			elif d == 2:
				cliques = criticalCliques['two_cliques']
			elif d == 1:
				cliques = criticalCliques['one_cliques']
			elif d == 0:
				cliques = criticalCliques['zero_cliques']

			for clique in cliques:
				# convert to list while returning
				A = set(clique)&(set(X) - set(Y))
			for clique in k_critical_cliques:
				B = set(clique)&(set(X) - set(Y))

			Y = list(set(Y).union(A))
			Z = list(set(Z).union(B))

		return Y, Z

	def isthmus_sym_thinning(self, X, k):
		K = []
		# repeat:
		crucial_isthmus = self.crucial_isthmus(X, K, k)
		Y = crucial_isthmus[0]
		Z = crucial_isthmus[1]
		X = Y
		K = list(set(K).union(set(Z)))
		# until stability
		return X
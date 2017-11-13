from datetime import datetime
import time,os
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt
from itertools import product, combinations
dict = {}

def plotCubeAt(single_voxel_vertices,ax):
	X = [x[0] for x in single_voxel_vertices]
	Y = [x[1] for x in single_voxel_vertices]
	Z = [x[2] for x in single_voxel_vertices]

	dict = {(voxel[0],voxel[1]):voxel[2] for voxel in single_voxel_vertices}

	X = np.array(X)
	print "shape",X.shape
	Y = np.array(Y)
	# X, Y = np.meshgrid(X, Y)
	print "shape",X.shape
	print X
	Z = np.array(Z)
	# Z = Z.reshape(X.shape)
	print X,Y,Z
	ax.scatter(X,Y,Z, marker='s')
	# ax.plot_surface(X, Y, Z, color='b', rstride=1, cstride=1, alpha=1)

def getZ(x, y):
	return dict[(x,y)]
def visualize(list_of_voxel_vertices):
	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')
	# ax.set_aspect('equal')    

	for voxel in list_of_voxel_vertices:
		plotCubeAt(voxel,ax)
	plt.show()

def plotComplex(complex):
	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')

	X = [x[0] for x in complex]
	Y = [x[1] for x in complex]
	Z = [x[2] for x in complex]

	X = np.array(X)
	Y = np.array(Y)
	Z = np.array(Z)
	ax.scatter(X,Y,Z, marker='s')

	# plt.show()
	timestamp = str(datetime.now())
	path = './images/' + timestamp + '.png'
	plt.savefig(path,dpi=200)
	time.sleep(5)

def plot_tester():

	fig = plt.figure()
	ax = fig.gca(projection='3d')
	ax.set_aspect("equal")

	# draw cube
	r = [-2, 5]
	for s, e in combinations(np.array(list(product(r, r, r))), 2):
		if np.sum(np.abs(s-e)) == r[1]-r[0]:
			ax.plot3D(*zip(s, e), color="b")
	plt.show()



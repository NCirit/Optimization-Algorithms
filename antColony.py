import copy
import random
import time

from util import Util
from coordinate import Coordinate

class Ant:

	costMatrix = []
	phenemonMatrix = []
	probs = []

	def __init__(self, positionId):
		if len(Ant.costMatrix) == 0 or len(Ant.phenemonMatrix) == 0:
			raise Exception("Cost or phenomon matrix not initialized")
		self.currentPositionId = positionId
		self.route = [positionId]

	def travel(self):
		self.route = [random.randint(0, len(Ant.costMatrix[0]) - 1)]
		while len(self.route) != len(Ant.costMatrix[0]):
			triedIds = []
			maxPb = -1
			maxId = 0
			for i in range(len(Ant.costMatrix[0])):
				if i not in self.route and maxPb < Ant.probs[self.currentPositionId][i]:
					maxPb = Ant.probs[self.currentPositionId][i]
					maxId = i
			self.currentPositionId = maxId
			self.route.append(self.currentPositionId)


	@staticmethod
	def initializeCostMatrix(coords):
		Ant.costMatrix = [[0 for i in range(len(coords))] for i in range(len(coords))]
		for i in range(len(coords)):
			for j in range(len(coords)):
				Ant.costMatrix[i][j] = Coordinate.get_distance(coords[i], coords[j])
	
	@staticmethod
	def updateProbabilities():
		if len(Ant.costMatrix) == 0 or len(Ant.phenemonMatrix) == 0:
			raise Exception("Cost or phenomon matrix not initialized")

		Ant.probs = [ [0 for i in range(len(Ant.costMatrix[0]))] for i in range(len(Ant.costMatrix[0]))]
		for i in range(len(Ant.costMatrix[0])):
			divider = 0
			for k in range(len(Ant.costMatrix[0])):
				if k == i:
					continue
				divider += Ant.phenemonMatrix[i][k]/Ant.costMatrix[i][k]
			for j in range(len(Ant.costMatrix[0])):
				if j == i:
					continue
				Ant.probs[i][j] =  (Ant.phenemonMatrix[i][j]/ Ant.costMatrix[i][j]) / divider

	@staticmethod
	def initializePhenomonMatrix(size):
		Ant.phenemonMatrix = [[1 for i in range(size)] for i in range(size)]


class AntColony:
	def __init__(self, coords, colonySize = 15, ro = 0.5):
		self.coords = coords
		self.ro = ro
		Ant.initializeCostMatrix(coords)
		Ant.initializePhenomonMatrix(len(coords))
		self.colony = [Ant(min(random.randint(0, len(coords) - 1), len(coords) - 1)) for i in range(colonySize)]
		self.globalBest = 0
		self.globalBestRoute = []

	def iter(self):
		Ant.updateProbabilities()
		for i in self.colony:
			i.travel()
		self.updatePhenomon()

	def updatePhenomon(self):
		tempPhenomon = [[0 for i in range(len(Ant.phenemonMatrix[0]))] for i in range(len(Ant.phenemonMatrix[0]))]
		for i in self.colony:
			routeLength = Coordinate.get_total_distance2(self.coords, i.route)
			if len(self.globalBestRoute) == 0 or self.globalBest > routeLength:
				self.globalBest = routeLength
				self.globalBestRoute = copy.deepcopy(i.route)
			for j in range(len(i.route) - 1):
				tempPhenomon[i.route[j]][i.route[j + 1]] += 1/routeLength
			tempPhenomon[i.route[-1]][i.route[0]] += 1/routeLength
		for i in range(len(Ant.phenemonMatrix[0])):
			for j in range(len(Ant.phenemonMatrix[0])):
				Ant.phenemonMatrix[i][j] = (1 - self.ro)*Ant.phenemonMatrix[i][j] + tempPhenomon[i][j]
			



		
		
	

def main():
	tspContents = Util.parseTSP("berlin52.tsp")
	coords = [Coordinate(p[0], p[1], i)\
						for i, p in zip(range(len(tspContents)), tspContents)]
	configs = [
						[100, 30, 0],\
						[100, 30, 0.2],\
						[100, 30, 0.5],\
						[100, 100, 0],\
						[100, 100, 0.2],\
						[100, 100, 0.5],\
						[1000, 30, 0],\
						[1000, 30, 0.2],\
						[1000, 30, 0.5],\
						[1000, 100, 0],\
						[1000, 100, 0.2],\
						[1000, 100, 0.5]]
	for iterCount, colonySize, ro in configs:
		colony = AntColony(coords, colonySize, ro)
		costs = []
		start = time.time()
		for i in range(iterCount):
			colony.iter()
			#print("Iter{}: Cost:{}".format(i,colony.globalBest))
			costs.append(colony.globalBest)
		end = time.time()
		bestCoords = []
		for i in colony.globalBestRoute:
			bestCoords.append(coords[i])
		
		title = "Iteration:{} ColonySize:{}\n Ro:{} ElapsedTime:{:.2f}sn".format(\
			iterCount, colonySize, ro, end - start)
		Util.showPlot(bestCoords, costs, title, "Ant Colony")

if __name__ == "__main__":
	main()
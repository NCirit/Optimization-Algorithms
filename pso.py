import random
import copy
from util import Util
from coordinate import Coordinate
import time


NOT_TAKEN = 0
TAKEN = 1
NONE_ID = None
NONE_INDEX = None

class SwapOperator:

	@staticmethod
	def createRandomSwap(dimension, swapCount):
		tempSwapSequance = [[None, None] for i in range(swapCount)] 
		for i in range(0, swapCount):
			swapItemID1 = random.randint(0, dimension - 1)
			swapItemID2 = random.randint(0, dimension - 1)
			while swapItemID1 == swapItemID2:
				swapItemID2 = random.randint(0, dimension - 1)
			tempSwapSequance[i][0] = swapItemID1
			tempSwapSequance[i][1] = swapItemID2
		return tempSwapSequance 

	@staticmethod
	def calculateSwapSequance(position, toPosition):
		newSwapSequance = []
		for i in toPosition[0]:
			if toPosition[1][i] != position[1][i]:
				itemID1 = i
				itemID2 = position[0][toPosition[1][i]]

				newSwapSequance.append([itemID1, itemID2])
				
				index1 = position[1][itemID1]
				index2 = position[1][itemID2]

				position[0][index1] = itemID2
				position[0][index2] = itemID1

				position[1][itemID1] = index2
				position[1][itemID2] = index1
		return newSwapSequance

	@staticmethod
	def calculateBasicSwapSequance(position, swaps):
		tempPosition = copy.deepcopy(position)
		for itemID1, itemID2 in swaps:
			index1 = tempPosition[1][itemID1]
			index2 = tempPosition[1][itemID2]

			tempPosition[0][index1] = itemID2
			tempPosition[0][index2] = itemID1

			tempPosition[1][itemID1] = index2
			tempPosition[1][itemID2] = index1
		newSwapSequance = SwapOperator.calculateSwapSequance(position, tempPosition)
		return newSwapSequance



class Particle:
	COORDINATES = []
	def __init__(self, omega=0.2, alfa=0.3, beta = 0.5):
		if len(Particle.COORDINATES) == 0:
			raise Exception("You should define coordinate first with:\
				 Particle.setCoordinates(arrayofCoordinateobjects)")
		self.position = Particle.createRandomPosition(len(Particle.COORDINATES))
		self.bestPersonelPosition = self.position
		self.bestPositionFitness = self.fitness()
		self.position =  Particle.createRandomPosition(len(Particle.COORDINATES))
		self.velocity = SwapOperator.createRandomSwap(len(Particle.COORDINATES), 1)
		self.velocity = SwapOperator.calculateBasicSwapSequance(copy.deepcopy(self.position), self.velocity)
		
		self.omega = omega# / (alfa + beta + omega)
		self.alfa = alfa# / (alfa + beta + omega)
		self.beta = beta# / (alfa + beta + omega)

	def updatePosition(self, globalBest):
		swapSequance = []

		## Pid - Xid
		## Pid'i elde etmek icin Xid'ye uygulanacak olan swap sequance
		personelBestDistance = SwapOperator.calculateSwapSequance(copy.deepcopy(self.position), self.bestPersonelPosition)
		for i in personelBestDistance:
			if self.alfa >= random.random():
				## olasilik degerleri icin
				swapSequance.append(i)
		## Pgd - Xid
		## Pgd'yi elde etmek icin Xid'ye uygulanacak  olan swap sequance
		globalBestDistance = SwapOperator.calculateSwapSequance(copy.deepcopy(self.position), globalBest)
		for i in globalBestDistance:
			if self.beta >= random.random():
						## olasilik degerleri icin
				swapSequance.append(i)
		
		self.velocity = SwapOperator.createRandomSwap(len(Particle.COORDINATES), 1)
		for i in self.velocity:
			if self.omega >= random.uniform(0,1):
				## olasilik degerleri icin
				swapSequance.append(i)
	
		self.velocity = SwapOperator.calculateBasicSwapSequance(copy.deepcopy(self.position), swapSequance)
		self.applyVelocity()
		#self.velocity = SwapOperator.calculateBasicSwapSequance(copy.deepcopy(self.position),\
		#								 SwapOperator.createRandomSwap(len(Particle.COORDINATES), random.randint(1, 20)))
		self.updatePersonelBest()

	def updatePersonelBest(self):
		currentFitness = self.fitness()
		if currentFitness < self.bestPositionFitness:
			self.bestPersonelPosition = copy.deepcopy(self.position)
			self.bestPositionFitness = currentFitness
	
	def applyVelocity(self):
		for itemID1, itemID2 in self.velocity:
			index1 = self.position[1][itemID1]
			index2 = self.position[1][itemID2]

			self.position[0][index1] = itemID2
			self.position[0][index2] = itemID1

			self.position[1][itemID1] = index2
			self.position[1][itemID2] = index1

	def fitness(self):
		rota = []
		for i in self.position[0]:
			rota.append(Particle.COORDINATES[i])
		return Coordinate.get_total_distance(rota)
		
	@staticmethod
	def createRandomPosition(dimension):
		taken = [NOT_TAKEN] * dimension
		# stores the squence of cities by squence number, and squence number by city Id
		# newPosition[0][5] is equal to id of fifth city to be visited
		# newPosition[1][5] is equal to sequance number of the city that has the id of 5 
		newPosition =  [[NOT_TAKEN] * dimension, [NONE_INDEX] * dimension] 
		for i in range(0, dimension):
			id = random.randint(0,dimension - 1)
			while taken[id] == TAKEN:
				id = random.randint(0, dimension - 1)
			taken[id] = TAKEN
			newPosition[0][i] = id
			newPosition[1][id] = i
		
		return newPosition

	@staticmethod
	def setCoordinates(coordinate):
		Particle.COORDINATES = coordinate

	@staticmethod
	def getCoordinateFromRoute(rota):
		coords = []
		for i in rota:
			coords.append(Particle.COORDINATES[i])
		return coords
	
	def __str__(self):
		str = ""
		for i in range(len(self.position[0])):
			temp = "Index:{} , ItemID {} -> ItemID {} , Index {}\n".format(i,self.position[0][i],\
							i,self.position[1][i])
			str += temp
		return str
	def __repr__(self):
		return str(self)

class ParticleSwarmOptimization:

	def __init__(self, particleCount, coordinates , omega=0.2, alfa=0.3, beta = 0.5):
		Particle.setCoordinates(coordinates)
		self.particles = [Particle(omega, alfa, beta) for i in range(particleCount)]
		self.globalBest = None
		self.globalbestFitness = None
		self.calculateGlobalBest()

	def calculateGlobalBest(self):
		if len(self.particles) == 0:
			raise Exception("There is zero particle!!")

		bestFitness = self.particles[0].bestPositionFitness
		bestPositon = self.particles[0].bestPersonelPosition
		for i in range(1, len(self.particles)):
			if bestFitness > self.particles[i].bestPositionFitness:
				bestFitness = self.particles[i].bestPositionFitness
				bestPositon = self.particles[i].bestPersonelPosition
		
		if self.globalBest is None or self.globalbestFitness is None:
			self.globalBest = bestPositon
			self.bestFitness = bestFitness
		else:
			if(self.globalbestFitness > bestFitness):
				self.globalbestFitness = bestFitness
				self.globalBest = bestPositon
				print(self.globalbestFitness)
				print(self.globalBest)
		return bestPositon,bestFitness
	
	def iter(self):
		for particle in self.particles:
			particle.updatePosition(self.globalBest)
		self.calculateGlobalBest()

	def printFitness(self):
		fitness = [i.bestPositionFitness for i in self.particles]
		fitness = sorted(fitness, key= lambda x: x, reverse=False)
		for i in fitness:
			print(i)
		print()
		
def main():
	tspContents = Util.parseTSP("berlin52.tsp")
	points = [Coordinate(p[0], p[1], i)\
						for i, p in zip(range(len(tspContents)), tspContents)]
	params = [[100, 30, 1, 0.5, 0.5],\
						[100, 30, 1, 0.5, 0.2],\
						[100, 30, 1, 0.2, 0.5],\
						[100, 30, 1, 0.2, 0.2],\
						[100, 100, 1, 0.5, 0.5],\
						[100, 100, 1, 0.5, 0.2],\
						[100, 100, 1, 0.2, 0.5],\
						[100, 100, 1, 0.2, 0.2],\
						[100, 30, 0.5, 0.5, 0.5],\
						[100, 30, 0.5, 0.5, 0.2],\
						[100, 30, 0.5, 0.2, 0.5],\
						[100, 30, 0.5, 0.2, 0.2],\
						[100, 100, 0.5, 0.5, 0.5],\
						[100, 100, 0.5, 0.5, 0.2],\
						[100, 100, 0.5, 0.2, 0.5],\
						[100, 100, 0.5, 0.2, 0.2],\
						[1000, 30, 1, 0.5, 0.5],\
						[1000, 30, 1, 0.5, 0.2],\
						[1000, 30, 1, 0.2, 0.5],\
						[1000, 30, 1, 0.2, 0.2],\
						[1000, 100, 1, 0.5, 0.5],\
						[1000, 100, 1, 0.5, 0.2],\
						[1000, 100, 1, 0.2, 0.5],\
						[1000, 100, 1, 0.2, 0.2],\
						[1000, 30, 0.5, 0.5, 0.5],\
						[1000, 30, 0.5, 0.5, 0.2],\
						[1000, 30, 0.5, 0.2, 0.5],\
						[1000, 30, 0.5, 0.2, 0.2],\
						[1000, 100, 0.5, 0.5, 0.5],\
						[1000, 100, 0.5, 0.5, 0.2],\
						[1000, 100, 0.5, 0.2, 0.5],\
						[1000, 100, 0.5, 0.2, 0.2]
						]
	title = "Iteration:{} ParticleCount:{}\n Omega:{} Alfa:{}\n Beta:{} ElapsedTime:{:.2f}sn"
	for iteration, particleCount, omega, alfa, beta in params:
		pso = ParticleSwarmOptimization(particleCount, points, omega, alfa, beta)
		costs = []
		start = time.time()
		for i in range(iteration):
			pso.iter()
			#pso.printFitness()
			#print("Iter " + str(i) + ": ", pso.bestFitness)
			costs.append(pso.bestFitness)
		end = time.time()
		print(pso.globalBest[0])
		Util.showPlot(Particle.getCoordinateFromRoute(pso.globalBest[0]), costs,\
			title.format(iteration, particleCount, omega, alfa, beta, end - start), fileName="PSO")

if __name__ == "__main__":
	main()
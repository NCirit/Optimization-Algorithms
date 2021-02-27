import numpy as np
import random
import time
import matplotlib.pyplot as plt

from coordinate import Coordinate
from util import Util

class GeneticSalesmanAlgorithm:
	def __init__(self, points, iterCount = 100, populationSize=30, selectionRate=0.2, mutationRate=0):
		self.points = points
		self.genCount = len(points) # For sales man gens are x and y location of cities
		self.populationSize = populationSize
		self.iterCount = iterCount
		self.selectionRate = selectionRate
		self.mutationRate = mutationRate
		self.costs = []
		self.figure = plt.figure(figsize=(10, 5))
		self.population = self.create_starting_population(populationSize)
		self.population = sorted(self.population, key= lambda x: self.fitness(x), reverse=False)

	def create_individual(self):
		individual = [[None] * self.genCount, [None] * self.genCount]
		for i in range(self.genCount):
			randNumber = random.randint(0, self.genCount - 1)
			while individual[0][randNumber] != None:
				randNumber = random.randint(0, self.genCount - 1)
			individual[0][randNumber] = self.points[i]
			individual[1][i] = randNumber
		return individual
	
	def create_starting_population(self, count):
		return [self.create_individual() for i in range(count)]

	def fitness(self, individual):
		return Coordinate.get_total_distance(individual[0])

	def crossover(self, individual1, individual2):
		newIndividual = [[None] * self.genCount, [None] * self.genCount]
		temp = random.randint(0, self.genCount - 1)
		newIndividual[0][0] = individual1[0][temp]
		newIndividual[1][individual1[0][temp].id] = 0
		lastIndex = 0
		for i in range(1, self.genCount):
			if i & 1 == 1:
				genId = newIndividual[0][lastIndex].id
				index =  individual2[1][genId]
				while index < self.genCount and newIndividual[1][individual2[0][index].id] is not None:
					index += 1 

				if index == self.genCount:
					index = individual2[1][genId]
					while index >= 0 and newIndividual[1][individual2[0][index].id] is not None:
						index -= 1
				
				if(index == self.genCount or index == -1):
					raise Exception("Array size is larger than the unique gen count")

				lastIndex += 1
				newIndividual[0][lastIndex] = individual2[0][index]
				newIndividual[1][individual2[0][index].id] = lastIndex
			else:
				genId = newIndividual[0][lastIndex].id
				index =  individual1[1][genId]
				while index < self.genCount and newIndividual[1][individual1[0][index].id] is not None:
					index += 1 

				if index == self.genCount:
					index = individual1[1][genId]
					while index >= 0 and newIndividual[1][individual1[0][index].id] is not None:
						index -= 1
				
				if(index == -1):
					raise Exception("Array size is larger than the unique gen count")

				lastIndex += 1
				newIndividual[0][lastIndex] = individual1[0][index]
				newIndividual[1][individual1[0][index].id] = lastIndex
		if None in newIndividual[0] or None in newIndividual[1]:
			raise Exception("None gene found on new individual at crossover step.")
		return newIndividual

	def selectionOfBests(self, isSorted = True):
		if not isSorted:
			self.population = sorted(self.population, key=lambda x:self.fitness(x), reverse = False)
		return self.population[:int(self.populationSize * self.selectionRate)]
	
	def  mutate(self, individual):
		selectGen = random.randint(0,  self.genCount - 1)
		selectSequance = random.randint(0,  self.genCount - 1)

		temp = individual[0][selectSequance]
		individual[0][selectSequance] = individual[0][selectGen]
		individual[0][selectGen] = temp

		individual[1][temp.id] = selectGen
		individual[1][individual[0][selectSequance].id] = selectSequance
		
		return individual

	def iter(self):
		parents = self.selectionOfBests()
		childs = []
		for i in range(1, int(self.populationSize * self.selectionRate)):
			if(len(childs) + len(parents) >= self.populationSize):
				break
			childs.append(self.crossover(parents[i], parents[i-1]))
		mutatedIndividuals = []
		for i in range(0, self.populationSize - (len(childs) + len(parents))):
			temp = self.population[len(parents) + i]
			temp = self.mutate(temp)
			for j in range(int(self.genCount * self.mutationRate)):
				temp = self.mutate(temp)
			mutatedIndividuals.append(temp)
		parents.extend(childs)
		parents.extend(mutatedIndividuals)
		self.population = sorted(parents, key= lambda x: self.fitness(x), reverse=False)
		self.costs.append(self.fitness(self.population[0]))

	def showPlot(self):
		ax1 = self.figure.add_subplot(222)
		ax2 = self.figure.add_subplot(212)

		coords = self.population[0][0]
		for first, second in zip(coords[:-1], coords[1:]):
			ax1.plot([first.x, second.x], [first.y, second.y])
		ax1.plot([coords[0].x, coords[-1].x], [coords[0].y, coords[-1].y])
		for c in coords:
			ax1.plot(c.x, c.y, "ro", markersize=1)
		
		ax1.plot(coords[0].x, coords[0].y, "bo",markersize=1)
		ax2.plot(self.costs)
		ax2.text(len(self.costs) - 1, self.costs[-1], "LastCost=\n " + "{:.2f}".format(self.costs[-1]))

		title = "Iteration={} |||Population size={}\n \
Selection Rate={:.2f} |||Mutation Rate={:.2f}"\
														.format(self.iterCount, self.populationSize,\
															self.selectionRate, self.mutationRate)
		self.figure.suptitle(title)
		plt.savefig(title.replace("|", "").replace("\n", "").replace(" ", "_") + ".png")
		plt.show()
		







def main():
	#points = [Coordinate(np.random.uniform(), np.random.uniform(), i) for i in range(self.genCount)]
	tspContents = Util.parseTSP("berlin52.tsp")
	points = [Coordinate(p[0], p[1], i)\
						for i, p in zip(range(len(tspContents)), tspContents)]
	genCount = len(points)
	iterCount = 1000
	popSize = 100
	selectionRate=0.4
	mutationRate=0
	config = [[100, 30, 0.2, 0],\
						[100, 30, 0.2, 0.1],\
						[100, 30, 0.4, 0],\
						[100, 30, 0.4, 0.1],\
						[100, 100, 0.2, 0],\
						[100, 100, 0.2, 0.1],\
						[100, 100, 0.4, 0],\
						[100, 100, 0.4, 0.1],\
						[1000, 30, 0.2, 0],\
						[1000, 30, 0.2, 0.1],\
						[1000, 30, 0.4, 0],\
						[1000, 30, 0.4, 0.1],\
						[1000, 100, 0.2, 0],\
						[1000, 100, 0.2, 0.1],\
						[1000, 100, 0.4, 0],\
						[1000, 100, 0.4, 0.1]]
	for iterCount, popSize, selectionRate, mutationRate in config:
		ga = GeneticSalesmanAlgorithm(points, iterCount, popSize, selectionRate, mutationRate)
		start = time.time()
		for i in range(iterCount):
			ga.iter()
		end = time.time()
		#ga.showPlot()
		title = "Iteration={} Population size={}\n Selection Rate={:.2f} Mutation Rate={:.2f}\n ElapsedTime:{:.2f}sn"\
							.format(iterCount, popSize, selectionRate, mutationRate, end - start)
		Util.showPlot(ga.population[0][0], ga.costs, title, "Genetic Algorithm")


if __name__ == "__main__":
	main()
	input()
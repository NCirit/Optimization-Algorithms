import random
import numpy as np
import time
from util import Util
from coordinate import Coordinate



class SimulatedAnnealing:
	def __init__(self, startingSolution, startingTemperature, temperatureFactor, lookAround):
		self.temperature = startingTemperature
		self.solution = startingSolution
		self.temperatureFactor = temperatureFactor
		self.lookAround = lookAround
		self.currentFitness = Coordinate.get_total_distance(startingSolution)

	def iter(self):
		self.temperature = self.temperature * self.temperatureFactor
		for k in range(self.lookAround):
			swapID1 = random.randint(0, len(self.solution) - 1)
			swapID2 = random.randint(0, len(self.solution) - 1)
			while swapID1 == swapID2:
				swapID2 = random.randint(0, len(self.solution) - 1)

			temp = self.solution[swapID1]
			self.solution[swapID1] = self.solution[swapID2]
			self.solution[swapID2] = temp

			tempFitness = Coordinate.get_total_distance(self.solution)

			if(tempFitness < self.currentFitness):
				self.currentFitness = tempFitness
				continue

			r = np.random.uniform() # 0-1 arasinda birtane deger urettik
			#print("r:{}, xp:{}".format(r, np.exp((self.currentFitness - tempFitness)/(self.temperature))))
			if self.temperature != 0 and r < np.exp((self.currentFitness - tempFitness)/(self.temperature)):
				self.currentFitness = tempFitness
			else:
				temp = self.solution[swapID1]
				self.solution[swapID1] = self.solution[swapID2]
				self.solution[swapID2] = temp


def main():
	tspContents = Util.parseTSP("berlin52.tsp")

	configs = [
						[100, 30, 50, 0.2],\
						[100, 30, 50, 0.5],\
						[100, 30, 50, 0.9],\
						[100, 30, 100, 0.2],\
						[100, 30, 100, 0.5],\
						[100, 30, 100, 0.9],\
						[100, 100, 50, 0.2],\
						[100, 100, 50, 0.5],\
						[100, 100, 50, 0.9],\
						[100, 100, 100, 0.2],\
						[100, 100, 100, 0.5],\
						[100, 100, 100, 0.9],\
						[1000, 30, 50, 0.2],\
						[1000, 30, 50, 0.5],\
						[1000, 30, 50, 0.9],\
						[1000, 30, 100, 0.2],\
						[1000, 30, 100, 0.5],\
						[1000, 30, 100, 0.9],\
						[1000, 100, 50, 0.2],\
						[1000, 100, 50, 0.5],\
						[1000, 100, 50, 0.9],\
						[1000, 100, 100, 0.2],\
						[1000, 100, 100, 0.5],\
						[1000, 100, 100, 0.9]]
	for iterCount, lookAround, temperature, temperatureFactor in configs:
		coords = [Coordinate(p[0], p[1], i)\
						for i, p in zip(range(len(tspContents)), tspContents)]
		sim = SimulatedAnnealing(coords, temperature, temperatureFactor, lookAround)
		costs = []
		start = time.time()
		for i in range(iterCount):
			sim.iter()
			costs.append(sim.currentFitness)
		endtime = time.time()
		title = "iterCount: {} lookAround:{}\nStartingTemperature:{} TemperatureFactor:{}\n ElapsedTime:{:.2f}sn".\
			format(iterCount, lookAround, temperature, temperatureFactor, (endtime - start))
		Util.showPlot(sim.solution, costs, title, "Simulated Annealing")
		sim = None


if __name__ == "__main__":
	main()




	
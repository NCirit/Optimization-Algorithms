import matplotlib.pyplot as plt
import os
class Util:
	counter = 0

	@staticmethod
	def parseTSP(filepath):
		fl = open(filepath, "r")
		str = fl.readlines()
		fl.close()
		i = 0
		for i in range(len(str)):
			if(str[i].strip() == "NODE_COORD_SECTION"):
				break

		if (i + 1) >= len(str):
			raise Exception("TSP Parse Error")

		points = []
		for j in range(i + 1, len(str) - 1):
			temp = str[j].split(" ")
			points.append([float(temp[1]), float(temp[2])])
		
		return points
	
	@staticmethod
	def showPlot(coords, costs, title = "", fileName = "", showIt = False):
		figure = plt.figure(figsize=(10, 5))
		ax1 = figure.add_subplot(222)
		ax2 = figure.add_subplot(212)
		ax3 = figure.add_subplot(221)

		for first, second in zip(coords[:-1], coords[1:]):
			ax1.plot([first.x, second.x], [first.y, second.y])
		ax1.plot([coords[0].x, coords[-1].x], [coords[0].y, coords[-1].y])
		for c in coords:
			ax1.plot(c.x, c.y, "ro", markersize=1)
		
		ax1.plot(coords[0].x, coords[0].y, "bo",markersize=1)
		ax2.plot(costs)
		ax2.text(len(costs) - 1, costs[-1], "LastCost=\n " + "{:.2f}".format(costs[-1]))

		ax3.set_title(fileName + "\n" + title, wrap = True, y = 1.0, pad= -10)
		if not os.path.exists(fileName):
			os.makedirs(fileName)
		plt.savefig(fileName+"/"+fileName + str(Util.counter) + ".png")
		Util.counter += 1
		if showIt:
			plt.show()
		else:
			plt.close(figure)

		
		
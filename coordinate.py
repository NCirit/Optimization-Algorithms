import numpy as np

class Coordinate:

	def __init__(self, x, y, id):
		self.x = x
		self.y = y
		self.id = id
	

	@staticmethod
	def get_distance(p1, p2):
		return np.sqrt(np.power(p1.x - p2.x, 2) + np.power(p1.y - p2.y, 2))

	@staticmethod
	def get_total_distance2(coords, rota):
		distance = 0
		for pId1, pId2 in zip(rota[:-1], rota[1:]):
			distance += Coordinate.get_distance(coords[pId1], coords[pId2])
		distance += Coordinate.get_distance(coords[rota[0]], coords[-1])

		return distance

	@staticmethod
	def get_total_distance(rota): 
		distance = 0
		for p1,p2 in zip(rota[:-1],rota[1:]):
			distance += Coordinate.get_distance(p1,p2)
		distance += Coordinate.get_distance(rota[0], rota[-1])
		
		return distance

	def __str__(self):
		return "id:{} ({},{})\n".format(self.id, self.x, self.y)
	def __repr__(self):
		return str(self)
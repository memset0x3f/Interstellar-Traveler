from constant import *

class Coordinate():
	def __init__(self, x, y):                   # receive a coordinate (x, y), create a new Coordinate instance
		self.x = x
		self.y = y
		self.dir_ = [(0, Y_STEP), (0, -Y_STEP), (-X_STEP, 0), (X_STEP, 0)]

	def __call__(self, *args, **kwargs):        # return current position
		return self.x, self.y

	def __add__(self, right):
		return Coordinate(self.x+right.x, self.y+right.y)

	def __eq__(self, other):
		return self.x == other.x and self.y == other.y

	def left(self):
		return Coordinate(self.x - X_STEP, self.y)

	def right(self):
		return Coordinate(self.x + X_STEP, self.y)

	def up(self):
		return Coordinate(self.x, self.y - Y_STEP)

	def down(self):
		return Coordinate(self.x, self.y + Y_STEP)

	def next(self, dir_:int):
		return Coordinate(self.x+self.dir_[dir_][0], self.y+self.dir_[dir_][1])

	def out_of_bound(self):
		"""
		Check if current coordinate is out of bound
		:return:
		"""
		if self.x <= LEFT_BOUND or self.x >= RIGHT_BOUND or self.y <= UP_BOUND or self.y >= DOWN_BOUND:
			return True
		return False
import time
from constant import *
from node import Node
from coordinate import Coordinate

class Bullet:
	def __init__(self, pos: Coordinate, interval = BULLET_SPEED):
		self.nodes = [Node('o', pos)]
		self.power = 1                  # Attack power
		self.time = time.time()         # The time of last movement
		self.interval = interval        # Interval between movements

	def interval_reached(self):
		"""
		Check if the bullet needs to move
		:return: None
		"""
		cur_time = time.time()
		return cur_time - self.time >= self.interval

	def out_of_bound(self) -> bool:
		"""
		Check if the bullet is out-of-bound
		:return: Bool
		"""
		return self.nodes[0].pos.out_of_bound()

	def move(self):
		"""
		Move the bullet if the interval condition is satisfied
		:return: None
		"""
		for i, node in enumerate(self.nodes):
			self.nodes[i].pos = node.pos.up()
		self.time = time.time()
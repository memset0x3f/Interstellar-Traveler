from node import Node
from coordinate import Coordinate
from constant import *

'''
The shape of plane:
  ^
 ^^^
^^^^^
'''


class Plane:
	def __init__(self):
		center = Node('^', Coordinate(WIDTH // 2, DOWN_BOUND - 1))
		self.head = center.up().up()
		self.nodes = [center, center.left(), center.left().left(), center.right(), center.right().right(),
		              center.up(), center.up().left(), center.up().right(), center.up().up()]

	def __eq__(self, other):
		for node_self in self.nodes:
			if node_self not in other.nodes:
				return False
		return True

	def _is_legal_move(self, direction) -> bool:
		for node in self.nodes:
			pos = node.pos.next(direction)
			if pos.out_of_bound():
				return False
		return True

	def move(self, direction):
		"""
		Move the plane toward the given direction (if legal).
		:param direction: The moving direction
		:return: None
		"""
		if not self._is_legal_move(direction):
			return
		self.head.pos = self.head.pos.next(direction)
		for i, node in enumerate(self.nodes):
			self.nodes[i].pos = node.pos.next(direction)

	def crash(self, obstacle) -> bool:
		"""
		Check if the plane crashes into an obstacle
		:param obstacle: An obstacle
		:return: Boolean
		"""
		for plane_node in self.nodes:
			for obstacle_node in obstacle.nodes:
				if plane_node.pos == obstacle_node.pos:
					return True
		return False

from coordinate import Coordinate
from constant import *

class Node:
	def __init__(self, char: str, pos: Coordinate):
		self.char = char            # The character of the current node
		self.pos = pos              # The position of the current node

	def __eq__(self, other):
		return self.char == other.char and self.pos == other.pos

	def left(self):
		return Node(self.char, self.pos.left())

	def right(self):
		return Node(self.char, self.pos.right())

	def up(self):
		return Node(self.char, self.pos.up())

	def down(self):
		return Node(self.char, self.pos.down())
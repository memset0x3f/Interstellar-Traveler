import curses
from coordinate import Coordinate
from constant import *

'''
Color1: fr: BLACK, bg: BLACK
Color2: fr: WHITE, bg: WHITE
Color3: fr: RED, bg:RED
Color4: fr: CYAN, bg:CYAN
Color5: fr: GREEN, bg:GREEN
Color6: fr: RED, bg: BLACK
Color7: fr: Yellow, bg: BLACK
Color8: fr: BLUE, bg: BLACK
'''

def init_curses():
	"""
	initialize some color pairs and some curses settings.
	:return: None
	"""
	curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_BLACK)
	curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_WHITE)
	curses.init_pair(3, curses.COLOR_RED, curses.COLOR_RED)
	curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_CYAN)
	curses.init_pair(5, curses.COLOR_GREEN, curses.COLOR_GREEN)

	curses.init_pair(6, curses.COLOR_RED, curses.COLOR_BLACK)
	curses.init_pair(7, curses.COLOR_YELLOW, curses.COLOR_BLACK)
	curses.init_pair(8, curses.COLOR_BLUE, curses.COLOR_BLACK)
	curses.noecho()             # Turn off terminal echo
	curses.curs_set(0)          # Remove the curser from the window
	# stdscr.timeout(300)

class Window:
	def __init__(self, screen, height, width):
		"""
		Initialize a window to process the drawing
		:param screen: a curses stdscr object
		"""
		init_curses()
		self.stdscr = screen
		self.stdscr.nodelay(True)
		self.height = height
		self.width = width
		self.color_blocks = {'BLACK':1, 'WHITE':2, 'RED':3, 'CYAN':4, 'GREEN':5}
		self.colors = {'RED': 6, 'YELLOW': 7, 'BLUE':8}

	def clear(self):
		"""
		Clear all the content in the current window
		:return:
		"""
		self.stdscr.clear()
		self.refresh()

	def refresh(self):
		"""
		Refresh the window
		:return:
		"""
		self.stdscr.refresh()

	def draw_text(self, pos, text, color, bold=False):
		"""
		Display a single line of text on the screen at pos.
		:param pos: The start position of the text(Coordinate instance).
		:param text: The text to be printed
		:param color: The color of drawing(str), options: RED, YELLOW, BLUE
		:param bold: Set the text to bold style if bold=True
		:return: None
		"""
		if color not in self.colors:
			raise IndexError('Invalid Color.')
		self.stdscr.addstr(pos.y, pos.x, text, curses.color_pair(self.colors[color]) | (bold*curses.A_BOLD))
		self.refresh()

	def draw_node(self, pos, color):
		"""
		Draw a single node on the screen at pos.
		:param pos: the start position of the node(Coordinate instance).
		:param color: the color of drawing(str), options: BLACK, WHITE, RED, GREEN, CYAN.
		:return:
		"""
		if color not in self.color_blocks:
			raise IndexError('Invalid Color.')
		self.stdscr.addstr(pos.y, pos.x, " ", curses.color_pair(self.color_blocks[color]))    # add 2 spaces to form a square
		self.refresh()

	def draw_frame(self):
		"""
		Draw the boarder of the game
		:return:
		"""
		for i in range(LEFT_BOUND+1, RIGHT_BOUND):
			for j in range(UP_BOUND+1, DOWN_BOUND):
				self.draw_node(Coordinate(i, j), 'BLACK')
		for i in range(self.height):
			self.draw_node(Coordinate(0, i), 'CYAN')
			self.draw_node(Coordinate(1, i), 'CYAN')
			self.draw_node(Coordinate(self.width-2, i), 'CYAN')
			self.draw_node(Coordinate(self.width-1, i), 'CYAN')
		for i in range(0, self.width):
			self.draw_node(Coordinate(i, 0), 'CYAN')
			self.draw_node(Coordinate(i, self.height-1), 'CYAN')
		self.refresh()

	def draw_item(self, item, color):
		"""
		Draw a plane in the current window.
		:param plane: The plane to be drawn
		:return:
		"""
		for node in item.nodes:
			if node.pos.out_of_bound():
				continue
			self.draw_text(node.pos, node.char, color, bold=True)
		self.refresh()

	def clear_item(self, item):
		"""
		Clear the former position of the item in the window
		:param item:
		:return:
		"""
		for node in item.nodes:
			if node.pos.out_of_bound():
				continue
			self.draw_node(node.pos, 'BLACK')
		self.refresh()

import copy
import curses
import time
from random import randint

from coordinate import Coordinate
from UI import Window
from constant import *
from plane import Plane
from obstacle import Obstacle
from bullet import Bullet

class MainGame:
	def __init__(self):
		# Game initialization
		self.time = time.time()                                     # Set the main timer
		self.last_acceleration = time.time()

		# Obstacles
		self.last_obstacle = time.time()                            # The time when the last obstacle was generated
		self.obstacle_interval = OBSTACLE_GENERATION_INTERVAL       # Set the generation interval of obstacles
		self.obstacle_speed = INITIAL_OBSTACLE_SPEED
		self.obstacles = []                                         # The list of all the existing obstacles

		# Bullet
		self.bullet_interval = BULLET_GENERATION_INTERVAL           # Set default bullet generation interval
		self.bullets = []

		# Plane
		self.plane = Plane()

	def __call__(self, stdscr):
		if curses.LINES < HEIGHT or curses.COLS < WIDTH:              # Exit when terminal size is too small
			stdscr.addstr(1, 1, 'Your terminal window size is too small.')
			stdscr.addstr(2, 1, f'The game needs at least {HEIGHT} lines and {WIDTH} columns.')
			stdscr.addstr(3, 1, f'Current Size: {curses.LINES} * {curses.COLS}')
			stdscr.addstr(4, 1, 'Press any key to quit.')
			stdscr.getch()
			return

		# Initial UI details
		self.stdscr = stdscr
		self.window = Window(stdscr, HEIGHT, WIDTH)         # Set default window size
		self.window.draw_frame()                            # Draw the boarder of the game window
		self.window.draw_item(self.plane, color='YELLOW')                   # Draw the plane

		# Game control process
		self.game_loop()

	def check_legal_obstacle_pos(self, pos:Coordinate) -> bool:
		"""
		Check if the initial obstacle position clash with other obstacles
		:param pos:
		:return: Bool
		"""
		for obstacle in self.obstacles:
			for node in obstacle.nodes:
				if node.pos == pos:
					return False
		return True

	def random_obstacle(self) -> Obstacle:
		"""
		Create a new obstacle instance with a random starting position
		:return: An Obstacle instance
		"""
		x = randint(LEFT_BOUND+1, RIGHT_BOUND-2)            # Random position of the left-top part of the obstacle
		pos = Coordinate(x, UP_BOUND+1)
		while not (self.check_legal_obstacle_pos(pos) and self.check_legal_obstacle_pos(pos.right())):
			x = randint(LEFT_BOUND + 1, RIGHT_BOUND - 2)
			pos = Coordinate(x, UP_BOUND + 1)
		return Obstacle(Coordinate(x, UP_BOUND), self.obstacle_speed)

	def generate_obstacle(self):
		"""
		Generate new obstacles if reaching the time interval
		:return: None
		"""
		cur_time = time.time()
		if cur_time - self.last_obstacle >= self.obstacle_interval:
			obstacle = self.random_obstacle()
			self.obstacles.append(obstacle)
			self.window.draw_item(obstacle, 'RED')
			self.last_obstacle = time.time()

	def update_obstacles(self):
		"""
		Clear out-of-bound obstacles
		:return: None
		"""
		new_obstacles = []
		for obstacle in self.obstacles:
			if not obstacle.out_of_bound():
				new_obstacles.append(obstacle)
			else:
				del obstacle
		self.obstacles = new_obstacles

	def move_obstacles(self):
		"""
		Move obstacles respectively
		:return: None
		"""
		for obstacle in self.obstacles:
			if obstacle.interval_reached():
				self.window.clear_item(obstacle)
				obstacle.move()
				self.window.draw_item(obstacle, color='RED')

	def fail(self):
		"""
		Show failure information and quit the game
		:return: None
		"""
		time.sleep(0.5)
		self.window.clear()
		self.window.draw_text(Coordinate(1, 1), 'You DIED!', 'RED', bold=True)
		survial = int(time.time()-self.time)            # Calculate the time duration
		self.window.draw_text(Coordinate(1, 2), f'You survived {survial//60} min {survial%60} sec', 'YELLOW', bold=True)
		self.window.draw_text(Coordinate(1, 4), 'Quit in 5 secs', 'RED', bold=False)
		time.sleep(5)

	def accelerate(self):
		"""
		Increase the speed of obstacle
		:return: None
		"""
		cur_time = time.time()
		if cur_time-self.last_acceleration >= ACCELERATION_INTERVAL:
			self.obstacle_interval *= ACCELERATION
			self.obstacle_speed *= ACCELERATION
			self.last_acceleration = time.time()

	def generate_bullet(self, pos):
		"""
		Generate a new bullet
		:param pos: the initial position of the bullet
		:return: None
		"""
		bullet = Bullet(pos, interval=BULLET_SPEED)
		self.bullets.append(bullet)

	def move_bullet(self):
		"""
		Move and redraw the bullets
		:return: None
		"""
		for bullet in self.bullets:
			if bullet.interval_reached():
				self.window.clear_item(bullet)
				bullet.move()
				self.window.draw_item(bullet, color='BLUE')

	def update_bullet(self):
		"""
		Clear out out-of-bound bullets
		:return: None
		"""
		new_bullets = []
		for bullet in self.bullets:
			if not bullet.out_of_bound():
				new_bullets.append(bullet)
			else:
				del bullet
		self.bullets = new_bullets

	def check_collision(self):
		"""
		Check if the bullets hit the obstacles
		Update the coresponding bullets and obstacles (Clear of life decrease)
		:return:
		"""
		new_obstacles = []
		for obstacle in self.obstacles:
			new_bullets = []                # Update bullets
			for bullet in self.bullets:
				flag = False            # Whether the obstacle have been hit by a bullet
				for node in obstacle.nodes:
					if node.pos == bullet.nodes[0].pos:
						flag = True
						break
				if flag:                                # The bullet hit the obstacle
					self.window.clear_item(bullet)      # Clear the bullet from the screen
					obstacle.life -= bullet.power       # Obstacle lose life
					del bullet
				else:
					new_bullets.append(bullet)
			self.bullets = new_bullets                  # Update bullets
			if obstacle.life <= 0:                      # If the obstacle dies
				self.window.clear_item(obstacle)        # Clear the obstacle from the screen
				del obstacle
			else:
				new_obstacles.append(obstacle)
		self.obstacles = new_obstacles

	def game_loop(self):
		last = copy.deepcopy(self.plane)       # Record the last position of the plane to decide whether to redraw the plane
		while True:
			key = self.stdscr.getch()
			if key == curses.KEY_LEFT:
				self.plane.move(LEFT)
			elif key == curses.KEY_RIGHT:
				self.plane.move(RIGHT)
			elif key == ord(' '):
				self.generate_bullet(self.plane.head.pos.up())
			elif key == ord('q'):
				break

			# Plane update
			if not self.plane == last:              # The position have been changed. Redraw the plane.
				self.window.clear_item(last)
				del last
				last = copy.deepcopy(self.plane)    # Record current position
				self.window.draw_item(self.plane, color='YELLOW')

			# Bullet update
			self.move_bullet()
			self.update_bullet()

			# Obstacle generation and update
			self.generate_obstacle()
			self.move_obstacles()
			self.update_obstacles()

			# Check collision between the bullets and the obstacles
			self.check_collision()

			# Check if the plane crashes into obstacles
			fail = False
			for obstacle in self.obstacles:
				if self.plane.crash(obstacle):          # Plane crashed, game failed
					self.fail()
					fail = True
					break
			if fail:
				break

			# Accelerate the obstacles
			self.accelerate()


if __name__ == '__main__':
	game = MainGame()
	curses.wrapper(game)

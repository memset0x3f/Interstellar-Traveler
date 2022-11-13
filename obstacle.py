from coordinate import Coordinate
from node import Node
from constant import *
import time

class Obstacle:
    def __init__(self, pos: Coordinate, interval=INITIAL_OBSTACLE_SPEED):
        leftup = Node('@', pos)
        self.nodes = [leftup, leftup.right(), leftup.down(), leftup.down().right()]
        self.time = time.time()                 # The time of last movement
        self.interval = interval                # The time interval between movements
        self.life = OBSTACLE_LIFE

    def out_of_bound(self) -> bool:
        """
        Check if ALL THE PART of the obstacle is out of bound.
        :return:
        """
        for node in self.nodes:
            if not node.pos.out_of_bound():
                return False
        return True

    def interval_reached(self):
        """
        Check if the obstacle needs to move
        :return: None
        """
        cur_time = time.time()
        return cur_time - self.time >= self.interval

    def move(self):
        """
        Move the obstacle if the interval condition is satisfied
        :return:
        """
        for i, node in enumerate(self.nodes):
            self.nodes[i].pos = node.pos.down()
        self.time = time.time()

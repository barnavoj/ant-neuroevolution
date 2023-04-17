import cv2 as cv
import numpy as np

from config import ACCELERATION_STD, MAX_SPEED
from sklearn.neural_network import MLPRegressor

class Ant:
    def __init__(self, position, size, colour):
        self.position = position
        self.colour = colour
        self.size = size
        self.speed = 0
        self.acceleration = 0
        
        self.brain = MLPRegressor(hidden_layer_sizes=(5,), max_iter=1)
        # brain inputs  ant x,y/ nearestfood x,y
        # brain outputs ant.acceleration vector
        self.brain.fit([[0,0,0,0]],[[0,0]])        

    def think(self, limits, nearest_food):
        # self.acceleration = np.random.normal(0, 1, 2) * ACCELERATION_STD
        
        # normalize inputs
        sx = self.position[1] / limits[1]
        sy = self.position[0] / limits[0]
        fx = nearest_food[1] / limits[1]
        fy = nearest_food[0] / limits[0]
        self.acceleration = self.brain.predict([[sx,sy,fx,fy]])[0]

    def move(self, limits):
        
        self.speed += self.acceleration

        speed_norm = np.linalg.norm(self.speed)
        if speed_norm > MAX_SPEED:
            self.speed = self.speed/speed_norm
            self.speed *= MAX_SPEED

        self.position += self.speed

        if self.position[0] > limits[0]:
            self.position[0] = 0

        if self.position[1] > limits[1]:
            self.position[1] = 0

        if self.position[0] < 0:
            self.position[0] = limits[0]

        if self.position[1] < 0:
            self.position[1] = limits[1]

    def draw_trail(self, scene):
        pt1 = (int(self.position[1]), int(self.position[0]))
        scene = cv.circle(scene, pt1, 1, self.colour, -1)

    def draw_body(self, scene):
        pt1 = (int(self.position[1]), int(self.position[0]))
        scene = cv.circle(scene, pt1, self.size, self.colour, -1)

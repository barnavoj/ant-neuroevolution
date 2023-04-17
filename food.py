import cv2 as cv
import numpy as np


class Food:
    def __init__(self, position, size, colour):
        self.position = position
        self.colour = colour
        self.size = size

    def draw(self, scene):
        pt1 = (int(self.position[1]), int(self.position[0]))
        scene = cv.circle(scene, pt1, self.size, self.colour, -1)

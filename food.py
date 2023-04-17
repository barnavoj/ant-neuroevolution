import cv2 as cv
import numpy as np


class Food:
    def __init__(self, position, size, colour):
        self.position = position
        self.colour = colour
        self.size = size

    def draw(self, scene, index):
        pt1 = (int(self.position[1]), int(self.position[0]))
        scene = cv.circle(scene, pt1, self.size, self.colour, -1)
        ## debug index
        #scene = cv.putText(scene, str(index), pt1, cv.FONT_ITALIC, 1, (0,0,255), 2)

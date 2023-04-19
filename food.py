import cv2 as cv
import numpy as np


class Food:
    def __init__(self, position, size, colour):
        
        # Check position type and always use tuple
        if type(position) is not tuple and type(position) is not list:
            raise TypeError
        elif type(position) is list:
            position = tuple(position)
        
        # Check position length
        if len(position) != 2:
            raise ValueError
       
        # Check position elements are int
        if not all(isinstance(elem, int) for elem in position):
            raise ValueError
        
        # Check color type and always use tuple    
        if type(colour) is not tuple and type(colour) is not list:
            raise TypeError
        elif type(colour) is list:
            colour = tuple(colour)

        # Check color length
        if len(colour) != 3:
            raise ValueError
        
        # Check colour elements are int
        if not all(isinstance(elem, int) for elem in colour):
            raise ValueError
        
        # Check size is int
        if not isinstance(size, int):
            raise ValueError
        
        self.position = position
        self.colour = colour
        self.size = size

    def draw(self, scene, index):
        pt1 = (int(self.position[1]), int(self.position[0]))
        scene = cv.circle(scene, pt1, self.size, self.colour, -1)
        ## debug index
        #scene = cv.putText(scene, str(index), pt1, cv.FONT_ITALIC, 1, (0,0,255), 2)

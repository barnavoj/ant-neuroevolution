import cv2 as cv
import numpy as np

from config import ACCELERATION_STD, MAX_SPEED, FOOD_REGEN, HEALTH_DECREASE, MUTATION_STD, CROSSOVER_PROB
from sklearn.neural_network import MLPRegressor

import warnings
from sklearn.exceptions import ConvergenceWarning
warnings.filterwarnings("ignore", category=ConvergenceWarning)

class Ant:
    def __init__(self, position, size=3, colour=(0, 0, 0), brain_1=None, brain_2=None):
        
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
        self.speed = 0
        self.acceleration = 0
        
        self.brain = MLPRegressor(hidden_layer_sizes=(5,), max_iter=1)
        # brain inputs  ant x,y/ nearestfood x,y
        # brain outputs ant.acceleration vector
        self.brain.fit([[0,0,0,0]],[[0,0]])
        
        if brain_1 is not None and brain_2 is not None:
            # crossover here
            for i, layer in enumerate(brain_2.coefs_):
                for j, ws in enumerate(layer):
                    for k, w in enumerate(ws):
                        if np.random.uniform(0,1) < CROSSOVER_PROB:
                            brain_1.coefs_[i][j][k] = w  
                                      
            for i, layer in enumerate(brain_2.intercepts_):
                for j, bias in enumerate(layer):
                    if np.random.uniform(0,1) < CROSSOVER_PROB:
                        brain_1.intercepts_[i][j] = bias
            
            # mutate the brain   
            for i in range(len(brain_1.coefs_)):
                self.brain.coefs_[i] = brain_1.coefs_[i] + np.random.normal(0, MUTATION_STD, brain_1.coefs_[i].shape)
                self.brain.intercepts_[i] = brain_1.intercepts_[i] + np.random.normal(0, MUTATION_STD, brain_1.intercepts_[i].shape)
 

        self.health = 100    
        self.score = 0
        
        
    def think(self, limits, nearest_food):
        # self.acceleration = np.random.normal(0, 1, 2) * ACCELERATION_STD
              
        # normalize inputs
        sx = self.position[1] / limits[1]
        sy = self.position[0] / limits[0]
        fx = nearest_food.position[1] / limits[1]
        fy = nearest_food.position[0] / limits[0]
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
        
    def starve(self):
        self.health -= HEALTH_DECREASE
        
    def regen(self):
        self.health += FOOD_REGEN
            
    def draw_trail(self, scene):
        pt1 = (int(self.position[1]), int(self.position[0]))
        scene = cv.circle(scene, pt1, 1, self.colour, -1)

    def draw_body(self, scene, index):
        pt1 = (int(self.position[1]), int(self.position[0]))
        scene = cv.circle(scene, pt1, self.size, self.colour, -1)
        ## debug index
        #scene = cv.putText(scene, str(index), pt1, cv.FONT_ITALIC, 0.5, (0,0,0), 2)
        # debug health
        #scene = cv.putText(scene, str(round(self.health)), pt1, cv.FONT_ITALIC, 0.5, (0,0,0), 2)
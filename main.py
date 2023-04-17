import cv2 as cv
import numpy as np
import time

from ant import Ant
from food import Food


class Colony:
    def __init__(self, scene_shape):
        self.num_ants = 0
        self.ants = []
        self.scene_shape = scene_shape

    def add_ants(self, num_ants):
        self.num_ants = num_ants

        for i in range(num_ants):
            position = [np.random.randint(0, self.scene_shape[0]),
                        np.random.randint(0, self.scene_shape[1])]
            colour = (0, 0, 0)
            new_ant = Ant(position, 3, colour)
            self.ants.append(new_ant)

    def update(self, food):
        limits = (self.scene_shape[0], self.scene_shape[1])
        for ant in self.ants:
            ant.think(limits, food)
            ant.move(limits)


class Scene:
    def __init__(self, colony):
        self.colony = colony
        self.food = []
        
    def add_background(self, scene_shape):
        self.scene_shape = scene_shape
        self.background = np.ones((self.scene_shape[0], self.scene_shape[1], 3)) * 255
        self.hist_scene = self.background.copy()
        self.live_scene = self.background.copy()
        
    def add_food(self, num_food):
        self.num_food = num_food

        for i in range(num_food):
            position = [np.random.randint(0, self.scene_shape[0]),
                        np.random.randint(0, self.scene_shape[1])]
            colour = (0, 120, 120)
            new_food = Food(position, 5, colour)
            self.food.append(new_food)

    def show_with_trails(self):
        frame = 0
        t = 0
        while True:
            frame += 1
            
            #Show Colony
            self.colony.update(self.food)
            self.live_scene = self.hist_scene.copy()
            for ant in self.colony.ants:
                ant.draw_body(self.live_scene)
                ant.draw_trail(self.hist_scene)
                
            #Show food
            for food in self.food:
                food.draw(self.live_scene)
            
            if frame % 30 == 0:
                dt = time.time() - t
                print("FPS: ", round(30*1/dt))
                t = time.time()
            
            cv.imshow("ants with trails", self.live_scene)
            if cv.waitKey(1) == ord('q'):
                # press q to terminate the loop
                cv.destroyAllWindows()
                break

    def show(self):
        frame = 0
        t = 0
        while True:
            frame += 1
            
            #Show Colony
            self.colony.update(self.food)
            self.live_scene = self.background.copy()
            for ant in self.colony.ants:
                ant.draw_body(self.live_scene)
                
            #Show food
            for food in self.food:
                food.draw(self.live_scene)

            if frame % 30 == 0:
                dt = time.time() - t
                print("FPS: ", round(30*1/dt))
                t = time.time()

            cv.imshow("ants", self.live_scene)
            if cv.waitKey(1) == ord('q'):
                # press q to terminate the loop
                cv.destroyAllWindows()
                break



def main():
    scene_shape = (800, 1000)
    num_ants = 50
    num_food = 10
    
    colony = Colony(scene_shape)
    colony.add_ants(num_ants)
    
    scene = Scene(colony)
    scene.add_background(scene_shape)
    scene.add_food(num_food)
 
    scene.show_with_trails()
    scene.show()


if __name__ == '__main__':
    main()

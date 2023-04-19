import cv2 as cv
import numpy as np
import time

from helpers import find_closest_food, distance_between

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
        for i, ant in enumerate(self.ants):
            #find nearest food
            closest_food_index = find_closest_food(ant, food)
            closest_food = food[closest_food_index]
            
            ant.think(limits, closest_food)
            ant.move(limits)
            
            # decrease health over time and add score
            ant.starve()
            ant.score += 1
            
            # eat food if close enough
            min_dist = ant.size + closest_food.size
            if distance_between(ant, closest_food) < min_dist:
                #food.pop(closest_food_index)
                closest_food.position = [np.random.randint(0, limits[0]),
                                 np.random.randint(0, limits[1])]
                ant.regen()
                print("Ant ", i, " ate food. Health remainig: ", round(ant.health))
            
            # die if zero health
            if ant.health < 1:
                self.ants.pop(i)
                print("Ant ", i, " died. Ants remaining: ",  len(self.ants))
                


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
            colour = (0, 0, 255)
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
            for i, ant in enumerate(self.colony.ants):
                ant.draw_body(self.live_scene, i)
                ant.draw_trail(self.hist_scene)
                
            #Show food
            for i, food in enumerate(self.food):
                food.draw(self.live_scene, i)
            
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
            for i, ant in enumerate(self.colony.ants):
                ant.draw_body(self.live_scene, i)
                
            #Show food
            for i, food in enumerate(self.food):
                food.draw(self.live_scene, i)

            if frame % 30 == 0:
                dt = time.time() - t
                #print("FPS: ", round(30*1/dt))
                t = time.time()

            cv.imshow("ants", self.live_scene)
            if cv.waitKey(1) == ord('q'):
                # press q to terminate the loop
                cv.destroyAllWindows()
                break
    
    def run_without_showing(self):
        frame = 0
        t = 0
        while True:
            frame += 1
            #Show Colony
            self.colony.update(self.food)
            # if frame % 30 == 0:
            #     dt = time.time() - t
            #     print("FPS: ", round(30*1/dt))
            #     t = time.time()

    def training_loop_and_show(self):
        frame = 0
        t = 0
        while True:
            frame += 1
            
            #Show Colony
            self.colony.update(self.food)
            self.live_scene = self.background.copy()
            for i, ant in enumerate(self.colony.ants):
                ant.draw_body(self.live_scene, i)
                
            #Show food
            for i, food in enumerate(self.food):
                food.draw(self.live_scene, i)

            if frame > 200 == 0:
                dt = time.time() - t
                #print("FPS: ", round(30*1/dt))
                t = time.time()

            cv.imshow("ants", self.live_scene)
            if cv.waitKey(1) == ord('q'):
                # press q to terminate the loop
                cv.destroyAllWindows()
                break
    

def main():
    scene_shape = (800, 800)
    num_ants = 100
    num_food = 20
    
    colony = Colony(scene_shape)
    colony.add_ants(num_ants)
    
    scene = Scene(colony)
    scene.add_background(scene_shape)
    scene.add_food(num_food)
 
    # scene.show_with_trails()
    # scene.show()
    # scene.run_without_showing()
    
    scene.training_loop_and_show()


if __name__ == '__main__':
    main()

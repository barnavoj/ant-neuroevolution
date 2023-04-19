import cv2 as cv
import numpy as np
import time

from helpers import find_closest_food, distance_between
from config import FRAMES_TO_RESET, NUM_ANTS, NUM_FOOD, SCENE_SHAPE, SCORE_PER_FRAME, SCORE_PER_FOOD

from ant import Ant
from food import Food

class Colony:
    def __init__(self, scene_shape):
        self.num_ants = 0
        self.ants = []
        self.scene_shape = scene_shape

    def add_ants(self, num_ants, brain=None):
        self.num_ants = num_ants

        for i in range(num_ants):
            position = [np.random.randint(0, self.scene_shape[0]),
                        np.random.randint(0, self.scene_shape[1])]
            
            if brain is not None:
                new_ant = Ant(position, brain=brain)
            else:
                new_ant = Ant(position)
            
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
            ant.score += SCORE_PER_FRAME
            
            # eat food if close enough
            min_dist = ant.size + closest_food.size
            if distance_between(ant, closest_food) < min_dist:
                #food.pop(closest_food_index)
                closest_food.position = [np.random.randint(0, limits[0]),
                                 np.random.randint(0, limits[1])]
                ant.regen()
                ant.score += SCORE_PER_FOOD
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
            
            new_food = Food(position)
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
        generation = 0       
        t = time.time()
        frame = 0
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

            if frame%50 == 0:
                dt = time.time() - t
                print("FPS: ", round(50/dt))
                t = time.time()

            cv.imshow("ants", self.live_scene)
            if cv.waitKey(1) == ord('q'):
                # press q to terminate the loop
                cv.destroyAllWindows()
                break
            
            if frame > FRAMES_TO_RESET:
                generation += 1
                print("\nGeneration ", generation," spawning\n")
                frame = 0
                
                # sort ants based on score and use best ant's brain
                self.colony.ants.sort(key=lambda x: x.score, reverse=True)
                best_ant = self.colony.ants[0]
                #possibly implement crossover here
                #best_ant_2 = self.colony.ants[1]
                
                self.colony.ants = []
                self.colony.add_ants(NUM_ANTS, best_ant.brain)

            

def main():  
    colony = Colony(SCENE_SHAPE)
    colony.add_ants(NUM_ANTS)
    
    scene = Scene(colony)
    scene.add_background(SCENE_SHAPE)
    scene.add_food(NUM_FOOD)
 
    # scene.show_with_trails()
    # scene.show()
    # scene.run_without_showing()
    
    scene.training_loop_and_show()


if __name__ == '__main__':
    main()

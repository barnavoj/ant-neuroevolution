import cv2 as cv
import numpy as np
import time

from ant import Ant


class Colony:
    def __init__(self):
        self.num_ants = 0
        self.ants = []

    def add_background(self, h, w):
        self.background = np.ones((h, w, 3)) * 255
        self.hist_scene = self.background.copy()
        self.live_scene = self.background.copy()

    def add_ants(self, num_ants):
        self.num_ants = num_ants

        for i in range(num_ants):
            position = [np.random.randint(0, self.background.shape[0]),
                        np.random.randint(0, self.background.shape[1])]
            colour = (0, 0, 0)
            new_ant = Ant(position, 3, colour)
            self.ants.append(new_ant)

    def update(self):
        limits = (self.background.shape[0], self.background.shape[1])
        for ant in self.ants:
            ant.move(limits)

    def show_with_trails(self):
        frame = 0
        t = 0
        while True:
            frame += 1
            self.update()
            self.live_scene = self.hist_scene.copy()
            for ant in self.ants:
                ant.draw_body(self.live_scene)
                ant.draw_trail(self.hist_scene)

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
            self.update()
            self.live_scene = self.background.copy()
            for ant in self.ants:
                ant.draw_body(self.live_scene)

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
    colony = Colony()
    colony.add_background(800, 1000)
    colony.add_ants(50)
    colony.show_with_trails()
    colony.show()


if __name__ == '__main__':
    main()

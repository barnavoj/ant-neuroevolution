import cv2 as cv
import numpy as np
import time


MAX_SPEED = 0.6
ACCELERATION_STD = 0.041


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


class Ant:
    def __init__(self, position, size, colour):
        self.position = position
        self.colour = colour
        self.size = size
        self.speed = 0
        self.acceleration = 0

    def move(self, limits):
        self.acceleration = np.random.normal(0, 1, 2) * ACCELERATION_STD
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


def main():
    colony = Colony()
    colony.add_background(800, 1000)
    colony.add_ants(50)
    colony.show_with_trails()
    colony.show()


if __name__ == '__main__':
    main()

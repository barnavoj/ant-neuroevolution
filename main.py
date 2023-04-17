import cv2 as cv
import numpy as np


MAX_SPEED = 1
ACCELERATION_STD = 0.01


class Colony:
    def __init__(self):
        self.num_ants = 0
        self.ants = []

    def add_background(self, h, w):
        self.background = np.ones((h, w, 3)) * 255
        self.scene = self.background.copy()

    def add_ants(self, num_ants):
        self.num_ants = num_ants

        for i in range(num_ants):
            position = [np.random.randint(0, self.scene.shape[0]),
                        np.random.randint(0, self.scene.shap[1])]
            colour = (0, 0, 0)
            new_ant = Ant(position, 5, 5, colour)
            self.ants.append(new_ant)

    def draw_ants(self):
        self.scene = self.background.copy()
        for ant in self.ants:
            ant.move()
            ant.draw(self.scene)

    def draw_ant_trails(self):
        for ant in self.ants:
            ant.draw(self.scene)

    def show(self):
        while True:
            self.draw_ants()
            self.draw_ant_trails()
            cv.imshow("scene", self.scene)
            if cv.waitKey(10) == ord('q'):
                # press q to terminate the loop
                cv.destroyAllWindows()
                break


class Ant:
    def __init__(self, position, width, height, colour):
        self.position = position
        self.colour = colour
        self.width = width
        self.height = height
        self.speed = 0
        self.acceleration = 0

    def move(self):
        self.acceleration = np.random.normal(0, 1, 2) * ACCELERATION_STD
        self.speed += self.acceleration

        if np.linalg.norm(self.speed) > MAX_SPEED:
            self.speed = MAX_SPEED

        self.position += self.speed

    def draw(self, scene):
        # pt1 = (int(self.position[0]), int(self.position[1]))
        # pt2 = (int(self.position[0] + self.width),
        #        int(self.position[1] + self.height))
        # scene = cv.rectangle(scene, pt1, pt2, self.colour, -1)

        pt1 = (int(self.position[0]), int(self.position[1]))
        scene = cv.circle(scene, pt1, self.width, self.colour, -1)

        return


def main():
    colony = Colony()
    colony.add_background(400, 400)
    colony.add_ants(20)
    colony.show()


if __name__ == '__main__':
    main()

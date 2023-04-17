import cv2 as cv
import numpy as np


class Colony:
    def __init__(self):
        self.num_ants = 0
        self.ants = []
        self.scene = None

    def add_background(self, h, w):
        self.scene = np.ones((h, w, 3)) * 255

    def add_ants(self, num_ants):
        self.num_ants = num_ants

        for i in range(num_ants):
            position = (np.random.randint(0, self.scene.shape[0]),
                        np.random.randint(0, self.scene.shape[1]))
            colour = (0, 0, 0)
            new_ant = Ant(position, 5, 5, colour)
            self.ants.append(new_ant)

    def draw_ants(self):
        for ant in self.ants:
            self.scene = ant.draw(self.scene)

    def show(self):
        while True:
            cv.imshow("scene", self.scene)
            if cv.waitKey(1) == ord('q'):
                # press q to terminate the loop
                cv.destroyAllWindows()
                break


class Ant:
    def __init__(self, position, width, height, colour):
        self.position = position
        self.colour = colour
        self.width = width
        self.height = height

    def draw(self, scene):
        pt1 = (self.position[0], self.position[1])
        pt2 = (self.position[0] + self.width, self.position[1] + self.height)
        scene = cv.rectangle(scene, pt1, pt2, self.colour, -1)
        return scene


def main():
    colony = Colony()
    colony.add_background(400, 400)
    colony.add_ants(20)
    colony.draw_ants()
    colony.show()


if __name__ == '__main__':
    main()

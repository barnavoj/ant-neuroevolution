import numpy as np

# def find_closest_food(ant, foods):
#     node = ant.position
#     nodes = [ food.position for food in foods ]
#     nodes = np.asarray(nodes)
#     deltas = nodes - node
#     dist_2 = np.einsum('ij,ij->i', deltas, deltas)
#     return np.argmin(dist_2)


def find_closest_food(ant, foods):
    node = ant.position
    nodes = [ food.position for food in foods ]
    nodes = np.asarray(nodes)
    dist_2 = np.sum((nodes - node)**2, axis=1)
    return np.argmin(dist_2)


# def distance_between(ant, food):
#     node_1 = np.asarray(ant.position)
#     node_2 = np.asarray(food.position)
#     dist = np.sum((node_1 - node_2)**2)
#     return np.sqrt(dist)

def distance_between(ant, food):
    node_1 = np.asarray(ant.position)
    node_2 = np.asarray(food.position)
    return np.linalg.norm(node_1 - node_2)
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
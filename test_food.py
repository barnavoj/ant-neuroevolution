import unittest
import numpy as np
from food import Food


class TestFood(unittest.TestCase):
    
    def setUp(self):
        self.food1 = Food((0,0), 5, (0,0,0))
        self.food2 = Food([0,0], 5, [0,0,0])

    def test_instance_init(self):
        self.assertEquals(self.food1.position, (0,0))
        self.assertEquals(self.food1.size, 5)
        self.assertEquals(self.food1.colour, (0,0,0))
        
        self.assertEquals(self.food2.position, (0,0))
        self.assertEquals(self.food2.size, 5)
        self.assertEquals(self.food2.colour, (0,0,0))
    
    def test_init_raises(self):
        with self.assertRaises(TypeError):
            Food(0, 5, (0,0,0)) 
        with self.assertRaises(ValueError):
            Food((0,0,0), 5, (0,0,0))
        with self.assertRaises(ValueError):
            Food((0,"0"), 5, (0,0,0))
            
        with self.assertRaises(TypeError):
            Food((0,0), 5, 0)
        with self.assertRaises(ValueError):
            Food((0,0), 5, (0,0,0,0,0))   
        with self.assertRaises(ValueError):
            Food((0,0), 5, (0,0,1.7))
            
        with self.assertRaises(ValueError):
            Food((0,0), "6", (0,0,0))
        with self.assertRaises(ValueError):
            Food((0,0), [5], (0,0,0))
        with self.assertRaises(ValueError):
            Food((0,0), 5.4, (0,0,0))                


if __name__ == "__main__":
    unittest.main()
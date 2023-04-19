import unittest
from ant import Ant

class TestAnt(unittest.TestCase):
    
    def setUp(self):
        self.ant1 = Ant((0,0), 5, (0,0,0))
        self.ant2 = Ant([0,0], 5, [0,0,0])

    def test_instance_init(self):
        self.assertEquals(self.ant1.position, (0,0))
        self.assertEquals(self.ant1.size, 5)
        self.assertEquals(self.ant1.colour, (0,0,0))
        
        self.assertEquals(self.ant2.position, (0,0))
        self.assertEquals(self.ant2.size, 5)
        self.assertEquals(self.ant2.colour, (0,0,0))
    
    def test_init_raises(self):
        with self.assertRaises(TypeError):
            Ant(0, 5, (0,0,0)) 
        with self.assertRaises(ValueError):
            Ant((0,0,0), 5, (0,0,0))
        with self.assertRaises(ValueError):
            Ant((0,"0"), 5, (0,0,0))
            
        with self.assertRaises(TypeError):
            Ant((0,0), 5, 0)
        with self.assertRaises(ValueError):
            Ant((0,0), 5, (0,0,0,0,0))   
        with self.assertRaises(ValueError):
            Ant((0,0), 5, (0,0,1.7))
            
        with self.assertRaises(ValueError):
            Ant((0,0), "6", (0,0,0))
        with self.assertRaises(ValueError):
            Ant((0,0), [5], (0,0,0))
        with self.assertRaises(ValueError):
            Ant((0,0), 5.4, (0,0,0))
            
    def test_think(self):
        self.assertEquals(self.ant1.brain.predict([[0,0,0,0]])[0], )
            
        

        


if __name__ == "__main__":
    unittest.main()
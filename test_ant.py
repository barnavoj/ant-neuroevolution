import unittest
from ant import Ant

class TestAnt(unittest.TestCase):
    
    def setUp(self):
        self.ant = Ant((0,0), 5, (0,0,0))

    def test_instance_init(self):
        self.assertEquals(self.ant.position, (0,0))

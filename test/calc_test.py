
from unittest import TestCase
import pytest
import sys
from objects.dice import Dice

class TestDice(TestCase):
    
    def test_always_fail(self):
        self.assertTrue(False)
        
    def test_roll_valid(self):
        d = Dice(6)
        result = d.roll()
        assert "You rolled a " in result
        
    def test_roll_invalid(self):
        d = Dice(-1)
        assert d.roll() == "Please enter a number greater than 1."
    
    
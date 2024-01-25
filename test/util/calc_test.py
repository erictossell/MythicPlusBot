from unittest import TestCase
from app.objects.dice import Dice


class TestDice(TestCase):
    def test_roll_valid(self):
        dice = Dice(6)
        result = dice.roll()
        assert "You rolled a " in result

    def test_roll_invalid(self):
        dice = Dice(-1)
        assert dice.roll() == "Please enter a number greater than 1."

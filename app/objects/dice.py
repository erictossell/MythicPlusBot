import random   

class Dice:
    """A class that represents a dice."""
    def __init__(self, num_sides):
        """The constructor for the Dice class.

        Args:
            num_sides (int): The number of sides on the dice.
        """
        self.num_sides = num_sides

    def roll(self):
        """Roll the dice.

        Returns:
            string: Returns a random number between 1 and the number of sides on the dice.
        """
        if self.num_sides <= 1:
            return "Please enter a number greater than 1."
        else:
            roll_result = random.randint(1, self.num_sides)
            return f"You rolled a {roll_result} (between 1 and {self.num_sides})."
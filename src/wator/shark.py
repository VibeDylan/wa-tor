from __future__ import annotations

import random
from typing import TYPE_CHECKING
from .fish import Fish

if TYPE_CHECKING:
    from .planet import Planet

class Shark(Fish):
    """
    A class representing a shark.

    Attributes :
        x (int): Shark coordinate x on the grid.
        y (int): Shark coordinate y on the grid.
        age (int): number of chronons survived by Shark.
        reproduction_time (int) : number of chronons between each reproduction of Shark.
        energy (int) : energy left before Shark dies.
    """
    def __init__(self, x: int, y: int, reproduction_time: int=5, energy: int=10):
        """
        Docstring for __init__
        
        Initialize a Shark object.

        Parameters:
            x (int): Shark coordinate x on the grid.
            y (int): Shark coordinate y on the grid.
        """
        super().__init__(x, y, age=0)
        self.reproduction_time = reproduction_time
        self.energy = energy

    def reproduce(self, planet: 'Planet', old_position: tuple[int, int]) -> None:
        """Adds a new Shark entity on the grid."""
        if self.age > 0 and self.age % self.reproduction_time == 0:
            baby_shark = Shark(x=old_position[0], y=old_position[1])
            planet.add(baby_shark, baby_shark.x, baby_shark.y)

    def eat(self, planet: 'Planet', new_position: tuple[int, int]) -> None:
        """Regenerates shark's energy when it moves to a cell containing a fish."""
        self.move(planet, new_position)
        if self.energy >= 7:
            self.energy = 10
        else:
            self.energy += 3

    def check_if_dead(self, planet: 'Planet') -> None:
        """Removes the shark when it reaches 0 energy."""
        if self.energy <= 0:
            planet.remove(self.x, self.y)

    def search_fish(self, planet: 'Planet') -> None:
        """Checks if the cells surrounding the shark contain any fish."""
        adjacent_fishes = planet.fish_neighbors(self.x, self.y)
        if adjacent_fishes:
            self.move(planet, random.choice(adjacent_fishes))
        else:
            self.ask_direction(planet)
            self.energy -= 1
            self.check_if_dead(planet)

    def __str__(self) -> str:
        return f"The shark at coordinates ({self.x}, {self.y}) is {self.age} chronons old and has {self.energy} energy."

    def __repr__(self) -> str:
        return f"Shark, (x={self.x}, y={self.y}), age={self.age}, energy={self.energy}, reproduction_time={self.reproduction_time}"
    

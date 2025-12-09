from __future__ import annotations

import random
from typing import TYPE_CHECKING
from .fish import Fish

if TYPE_CHECKING:
    from .planet import Planet

from .config import shark_reproduction, shark_energy, shark_energy_gain

class Shark(Fish):
    """
        Represent a Shark, inherited from Fish.
    """
    def __init__(self, x: int, y: int, reproduction_time: int=shark_reproduction, energy: int=shark_energy):
        """ Initialize a new Shark object

            Args:
                x (int): x coordinate of Shark.
                y (int): y coordinate of Shark.
                reproduction_time (int, optional): reproduction time of Shark.
                energy (int, optional): energy of Shark.
        """
        super().__init__(x, y, age=0, reproduction_time=reproduction_time)
        self.energy = energy


    def reproduce(self, planet: 'Planet', old_position: tuple[int, int]) -> None:
        """
            Make the shark reproduces.

            Create a new Shark and add it to the grid, just after the old Shark.

            Args:
                planet (Planet): The planet
                old_position (tuple[int, int]): The current position (x, y)
        """
        if self.age > 0 and self.energy > 0 and self.age % self.reproduction_time == 0:
            baby = Shark(x=old_position[0], y=old_position[1])
            planet.add(baby, baby.x, baby.y)


    def eat(self, planet: 'Planet', new_position: tuple[int, int]) -> None:
        """
            Move and increase the shark energy.

            Args:
                planet (Planet): The planet
                new_position (tuple[int, int]): the position of the eaten fish (x, y)
        """
        self.move(planet, new_position)
        self.energy = min(self.energy + shark_energy_gain, shark_energy)


    def check_if_dead(self, planet: 'Planet') -> None:
        """
            Remove shark from grid if its dead

            Args:
                planet (Planet): The planet
        """
        if self.energy <= 0:
            planet.remove(self.x, self.y)


    def search_fish(self, planet: 'Planet') -> None:
        """
            Search available fish in grid and eat it

            Args:
                planet (Planet): The planet
        """
        fishes = planet.fish_neighbors(self.x, self.y)
        
        if fishes:
            self.age += 1
            target = random.choice(fishes)
            self.eat(planet, target)
            return

        self.search_free(planet)
        
        self.energy -= 1
        
        self.check_if_dead(planet)


    def __str__(self):
        return f"Shark(x={self.x}, y={self.y}, age={self.age}, energy={self.energy})"

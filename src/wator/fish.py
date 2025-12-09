from __future__ import annotations

import random
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .planet import Planet

from .config import fish_reproduction


class Fish:
    def __init__(self, x : int, y : int, age: int=0, reproduction_time: int=fish_reproduction, alive: bool=True):
        self.x = x
        self.y = y
        self.age = age
        self.reproduction_time = reproduction_time
        self.alive = alive


    def move(self, planet: 'Planet', new_position: tuple[int, int]) -> None:
        old_position = (self.x, self.y)
        move_allowed = planet.move(self.x, self.y, new_position[0], new_position[1])
        
        if move_allowed:
            self.reproduce(planet, old_position)


    def reproduce(self, planet: 'Planet', old_position: tuple[int, int]) -> None:
        if self.age > 0 and self.age % self.reproduction_time == 0:
            baby = Fish(old_position[0], old_position[1])
            planet.add(baby, baby.x, baby.y)

            
    def step(self, planet: 'Planet') -> None:
        # Le poisson vieillit au début du tour (logique Wa-Tor)
        self.age += 1

        free_cells = planet.free_neighbors(self.x, self.y)
    
        if free_cells:
            new_position = random.choice(free_cells)
            self.move(planet, new_position)

    def search_free(self, planet: 'Planet') -> None:
        self.age += 1
        free_cells = planet.free_neighbors(self.x, self.y)
        
        if free_cells:
            new_position = random.choice(free_cells)
            self.move(planet, new_position)

    def __str__(self):
        return f"Fish(x={self.x}, y={self.y}, age={self.age})"

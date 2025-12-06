from __future__ import annotations
import random
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .planet import Planet

from .fish import Fish


class Shark(Fish):
    
    def __init__(self, x: int, y: int, reproduction_time: int = 5, energy: int = 10):
        super().__init__(x, y, age=0, reproduction_time=reproduction_time)
        self.energy = energy
        self.max_energy = energy

    def try_reproduce(self, planet: Planet, x: int, y: int) -> None:
        if self.reproduction_counter >= self.reproduction_time:
            if planet.is_free(x, y):
                baby = Shark(x, y, self.reproduction_time, self.max_energy)
                planet.add_entity(baby, x, y)
                planet.register_newborn(baby)
                self.reproduction_counter = 0

    def eat(self, planet: Planet, target_x: int, target_y: int) -> None:
        if self.move(planet, target_x, target_y):
            self.energy = min(self.energy + 3, self.max_energy)

    def step(self, planet: Planet) -> None:
        if planet.get(self.x, self.y) is not self or self.has_moved:
            return
        
        self.has_moved = True
        self.age += 1
        self.reproduction_counter += 1

        fish_neighbors = planet.get_fish_neighbors(self.x, self.y)
        if fish_neighbors:
            target_x, target_y = random.choice(fish_neighbors)
            self.eat(planet, target_x, target_y)
        else:
            free_cells = planet.get_free_neighbors(self.x, self.y)
            if free_cells:
                new_x, new_y = random.choice(free_cells)
                self.move(planet, new_x, new_y)

        self.energy -= 1
        
        if self.energy <= 0:
            planet.remove_entity(self.x, self.y)

    def __repr__(self):
        return f"Shark(x={self.x}, y={self.y}, age={self.age}, energy={self.energy})"

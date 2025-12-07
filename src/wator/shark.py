from __future__ import annotations

import random
from typing import TYPE_CHECKING
from .fish import Fish

if TYPE_CHECKING:
    from .planet import Planet

class Shark(Fish):
    def __init__(self, x: int, y: int, reproduction_time: int=5, energy: int=10):
        super().__init__(x, y, age=0, reproduction_time=reproduction_time)
        self.energy = energy


    def reproduce(self, planet: 'Planet', old_position: tuple[int, int]) -> None:
        if self.age > 0 and self.age % self.reproduction_time == 0:
            baby = Shark(x=old_position[0], y=old_position[1])
            planet.add(baby, baby.x, baby.y)


    def eat(self, planet: 'Planet', new_position: tuple[int, int]) -> None:
        self.move(planet, new_position)
        self.energy = min(self.energy + 3, 10)


    def check_if_dead(self, planet: 'Planet') -> None:
        if self.energy <= 0:
            planet.remove(self.x, self.y)


    def search_fish(self, planet: 'Planet') -> None:
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
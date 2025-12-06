from __future__ import annotations

import random
from typing import TYPE_CHECKING

from .fish import Fish

if TYPE_CHECKING:
    from .planet import Planet


class Shark(Fish):
    def __init__(self, x: int, y: int, reproduction_time: int = 5, energy: int = 10):
        super().__init__(x, y, age=0, reproduction_time=reproduction_time)
        self.energy = energy
        self.max_energy = 10

    def reproduce(self, planet: 'Planet', old_position: tuple[int, int]) -> None:
        if self.age > 0 and self.age % self.reproduction_time == 0:
            ox, oy = old_position
            if planet.is_free(ox, oy):
                baby = Shark(ox, oy, reproduction_time=self.reproduction_time, energy=self.max_energy)
                planet.add(baby, ox, oy)
                if planet.simulation:
                    planet.simulation.newborns_shark.append(baby)

    def eat(self, planet: 'Planet', target: tuple[int, int]) -> None:
        self.move(planet, target)
        self.energy = min(self.energy + 3, self.max_energy)

    def step(self, planet: 'Planet') -> None:
        if planet.get(self.x, self.y) is not self:
            return

        if self.has_moved:
            return
        self.has_moved = True

        self.age += 1

        fishes = planet.fish_neighbors(self.x, self.y)
        if fishes:
            target = random.choice(fishes)
            self.eat(planet, target)
        else:
            free_cells = planet.free_neighbors(self.x, self.y)
            if free_cells:
                new_pos = random.choice(free_cells)
                self.move(planet, new_pos)

            self.energy -= 1

        if self.energy <= 0:
            planet.remove(self.x, self.y)

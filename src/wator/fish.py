from __future__ import annotations
import random
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .planet import Planet


class Fish:
    def __init__(self, x: int, y: int, age: int = 0, reproduction_time: int = 3):
        self.x = x
        self.y = y
        self.age = age
        self.reproduction_time = reproduction_time
        self.reproduction_counter = 0
        self.has_moved = False

    def move(self, planet: Planet, new_x: int, new_y: int) -> bool:
        """Déplace le poisson et tente de se reproduire."""
        old_x, old_y = self.x, self.y
        if planet.move_entity(old_x, old_y, new_x, new_y):
            self.try_reproduce(planet, old_x, old_y)
            return True
        return False

    def try_reproduce(self, planet: Planet, x: int, y: int) -> None:
        """Tente de créer un bébé à la position donnée."""
        if self.reproduction_counter >= self.reproduction_time:
            if planet.is_free(x, y):
                baby = self.__class__(x, y)
                planet.add_entity(baby, x, y)
                planet.register_newborn(baby)
                self.reproduction_counter = 0  # Réinitialiser le compteur

    def step(self, planet: Planet) -> None:
        """Exécute un tour de simulation pour ce poisson."""
        if planet.get(self.x, self.y) is not self or self.has_moved:
            return
        
        self.has_moved = True
        self.age += 1
        self.reproduction_counter += 1
        
        free_cells = planet.get_free_neighbors(self.x, self.y)
        if free_cells:
            new_x, new_y = random.choice(free_cells)
            self.move(planet, new_x, new_y)

    def __repr__(self):
        return f"{self.__class__.__name__}(x={self.x}, y={self.y}, age={self.age})"

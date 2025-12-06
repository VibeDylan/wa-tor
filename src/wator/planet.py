from __future__ import annotations
from typing import Union

from .fish import Fish
from .shark import Shark


class Planet:
    
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self._grid: list[list[Union[Fish, Shark, None]]] = [
            [None] * width for _ in range(height)
        ]
        self.simulation = None

    def get(self, x: int, y: int) -> Union[Fish, Shark, None]:
        return self._grid[y][x]

    def set(self, x: int, y: int, entity: Union[Fish, Shark, None]) -> None:
        self._grid[y][x] = entity

    def wrap_coordinates(self, x: int, y: int) -> tuple[int, int]:
        return x % self.width, y % self.height

    def is_free(self, x: int, y: int) -> bool:
        return self.get(x, y) is None

    def get_neighbors(self, x: int, y: int) -> list[tuple[int, int]]:
        neighbors = [(x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y)]
        return [self.wrap_coordinates(nx, ny) for nx, ny in neighbors]

    def get_free_neighbors(self, x: int, y: int) -> list[tuple[int, int]]:
        return [(nx, ny) for nx, ny in self.get_neighbors(x, y) if self.is_free(nx, ny)]

    def get_fish_neighbors(self, x: int, y: int) -> list[tuple[int, int]]:
        return [
            (nx, ny) for nx, ny in self.get_neighbors(x, y)
            if isinstance(self.get(nx, ny), Fish) and not isinstance(self.get(nx, ny), Shark)
        ]

    def move_entity(self, old_x: int, old_y: int, new_x: int, new_y: int) -> bool:
        entity = self.get(old_x, old_y)
        if entity is None:
            return False

        new_x, new_y = self.wrap_coordinates(new_x, new_y)
        target = self.get(new_x, new_y)

        if target is None:
            self.set(new_x, new_y, entity)
            self.set(old_x, old_y, None)
            entity.x, entity.y = new_x, new_y
            return True

        if isinstance(entity, Shark) and isinstance(target, Fish) and not isinstance(target, Shark):
            if self.simulation and target in self.simulation.fishes:
                self.simulation.fishes.remove(target)
            
            self.set(new_x, new_y, entity)
            self.set(old_x, old_y, None)
            entity.x, entity.y = new_x, new_y
            return True

        return False

    def add_entity(self, entity: Union[Fish, Shark], x: int, y: int) -> None:
        self.set(x, y, entity)

    def remove_entity(self, x: int, y: int) -> None:
        self.set(x, y, None)

    def register_newborn(self, baby: Union[Fish, Shark]) -> None:
        if self.simulation:
            if isinstance(baby, Shark):
                self.simulation.newborns_shark.append(baby)
            else:
                self.simulation.newborns_fish.append(baby)

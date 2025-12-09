from __future__ import annotations

from typing import Union
from .fish import Fish
from .shark import Shark

class Planet:    
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        
        self._grid: list[list[Union[Fish, Shark, None]]] = [
            [None for _ in range(width)]
            for _ in range(height)
        ]
        
    def get(self, x: int, y: int) -> Union[Fish, Shark, None]:
        return self._grid[y][x]
    
    def set(self, x: int, y: int, entity: Union[Fish, Shark, None]) -> None:
        self._grid[y][x] = entity
       
    def wrap(self, x: int, y: int) -> tuple[int, int]: 
        return x % self.width, y % self.height
    
    def is_free(self, x: int, y: int) -> bool:
        return self.get(x, y) is None 
    
    def neighbors(self, x: int, y: int) -> list[tuple[int, int]]:
        positions = [
            (x, y - 1),  
            (x, y + 1),  
            (x - 1, y),  
            (x + 1, y), 
        ]
        return [self.wrap(nx, ny) for nx, ny in positions] 
    
    def free_neighbors(self, x: int, y: int) -> list[tuple[int, int]]:
        return [(nx, ny) for nx, ny in self.neighbors(x, y)
                if self.is_free(nx, ny)]

    def fish_neighbors(self, x: int, y: int) -> list[tuple[int, int]]:
        return [
            (nx, ny)
            for nx, ny in self.neighbors(x, y)
            if type(self.get(nx, ny)) == Fish
        ]
    

    def move(self, old_x: int, old_y: int, new_x: int, new_y: int) -> bool:
        entity = self.get(old_x, old_y)
        if entity is None:
            return False

        # 👉 Déplacement normal
        if self.is_free(new_x, new_y):
            self.set(new_x, new_y, entity)
            self.set(old_x, old_y, None)

            entity.x = new_x
            entity.y = new_y
            return True

        if isinstance(entity, Shark):
            target = self.get(new_x, new_y)
            if type(target) is Fish:
                self.remove(new_x, new_y)
                target.alive = False
                self.set(new_x, new_y, entity)
                self.set(old_x, old_y, None)

                entity.x = new_x
                entity.y = new_y
                return True

        return False

    def add(self, entity: Union[Fish, Shark], x: int, y: int) -> None:
        self.set(x, y, entity)

    def remove(self, x: int, y: int) -> None:
        self.set(x, y, None)

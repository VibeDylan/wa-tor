from __future__ import annotations

from typing import Union
from .fish import Fish
from .shark import Shark

class Planet:
    """
    Represent a Planet with its grid

    Attributes:
        _grid (list[list[Union[Fish, Shark, None]]]): grid of fish who contains a Fish, Shark, or None
    """
    def __init__(self, width: int, height: int):
        """ Initialize a new Planet object.

            Args:
                width (int): width of the planet
                height (int): height of the planet
        """
        self.width = width
        self.height = height
        
        self._grid: list[list[Union[Fish, Shark, None]]] = [
            [None for _ in range(width)]
            for _ in range(height)
        ]
        
    def get(self, x: int, y: int) -> Union[Fish, Shark, None]:
        """ Return the entity found at the given position
            Args:
                x (int): x position
                y (int): y position

            Returns: Fish, Shark, or None
        """
        return self._grid[y][x]
    
    def set(self, x: int, y: int, entity: Union[Fish, Shark, None]) -> None:
        """ Set a new entity at the given position
            Args:
                x (int): x position
                y (int): y position
                entity (Union[Fish, Shark, None]): the new entity
        """
        self._grid[y][x] = entity
       
    def wrap(self, x: int, y: int) -> tuple[int, int]:
        """ Simulate toroidal shape and handle boundaries

            Managing the toroidal shape of the grid, by making entities
            that exceed the boundaries reappear at the opposite.

            Args:
                x (int): actual x position
                y (int): actual y position
            Returns:
                tuple[int, int]: the news coordinates
        """
        return x % self.width, y % self.height
    
    def is_free(self, x: int, y: int) -> bool:
        """ Return True if the given position is free
            Args:
                x (int): x position
                y (int): y position

            Returns:
                True if the given position is None, False otherwise
        """
        return self.get(x, y) is None
    
    def neighbors(self, x: int, y: int) -> list[tuple[int, int]]:
        """ Return all neighboring entities
            Args:
                x (int): x position
                y (int): y position

            Returns:
                list[tuple[int, int]]: all the neighboring entities position
        """
        positions = [
            (x, y - 1),
            (x, y + 1),
            (x - 1, y),
            (x + 1, y),
        ]
        return [self.wrap(nx, ny) for nx, ny in positions]
    
    def free_neighbors(self, x: int, y: int) -> list[tuple[int, int]]:
        """ Return all free neighboring entities

            Args:
                 x (int): x position
                 y (int): y position

            Returns: list[tuple[int, int]]: all the free neighboring entities position
        """
        return [(nx, ny) for nx, ny in self.neighbors(x, y)
                if self.is_free(nx, ny)]

    def fish_neighbors(self, x: int, y: int) -> list[tuple[int, int]]:
        """
        Return all neighboring fish entities

            Args:
                x (int): x position
                y (int): y position

            Returns: list[tuple[int, int]]: all the neighboring fish entities position
        """
        return [
            (nx, ny)
            for nx, ny in self.neighbors(x, y)
            if type(self.get(nx, ny)) == Fish
        ]
    

    def move(self, old_x: int, old_y: int, new_x: int, new_y: int) -> bool:
        """
        Move the given entity position to a new position

            Args:
                old_x (int): previous x position
                old_y (int): previous y position
                new_x (int): new x position
                new_y (int): new y position

            Returns:
                bool: True if the movement was successful, False otherwise
        """
        entity = self.get(old_x, old_y)
        if entity is None:
            return False

        new_x, new_y = self.wrap(new_x, new_y)

        # Déplacement normal
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
        """
        Add a Fish or a Shark to the grid

            Args: entity (Union[Fish, Shark]): the entity to add, only a Fish or a Shark
        """
        self.set(x, y, entity)

    def remove(self, x: int, y: int) -> None:
        """
        Remove a Fish or a Shark from the grid

            Args:
                x (int): x position
                y (int): y position
        """
        self.set(x, y, None)
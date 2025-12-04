import random
from .planet import Planet


class Fish:
    def __init__(self, x : int, y : int, age=0, reproduction_time=3):
        self.x = x
        self.y = y
        self.age = age
        self.reproduction_time = reproduction_time


    def move(self, planet: Planet, new_position: tuple[int, int]) -> None:
        old_position = (self.x, self.y)
        move_allowed = planet.move(self.x, self.y, new_position[0], new_position[1])
        if move_allowed:
            self.age += 1
            self.x = new_position[0]
            self.y = new_position[1]
            self.reproduce(planet, old_position)


    def ask_direction(self, planet: Planet)  -> None:
        free_cells = planet.free_neighbors(self.x, self.y)
        if free_cells:
            free_random = random.choice(free_cells)
            self.move(planet, free_random)
        self.age += 1


    def reproduce(self, planet: Planet, old_position: tuple[int, int]) -> None:
        if self.age > 0 and self.age % self.reproduction_time == 0:
            baby_fish = Fish(x=old_position[0], y=old_position[1], age=0, reproduction_time=self.reproduction_time)
            planet.add(baby_fish, baby_fish.x, baby_fish.y)


    def __str__(self):
        return f"Fish(x={self.x}, y={self.y}, age={self.age})"


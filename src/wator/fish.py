import random
from .planet import Planet


class Fish:
    def __init__(self, x, y, age=0, reproduction_time=3):
        self.x = x
        self.y = y
        self.age = age
        self.reproduction_time = reproduction_time

    def ask_direction(self, planet: Planet) -> tuple[int, int] | None: 
        free_cells = planet.free_neighbors(self.x, self.y)
        if free_cells:
            return random.choice(free_cells)
        return None

    def move(self, planet: Planet):
        new_position = self.ask_direction(planet)
        if new_position:
            new_x, new_y = new_position
            moved = planet.move(self.x, self.y, new_x, new_y)
            if moved:
                self.x, self.y = new_x, new_y

    def reproduce(self, planet: Planet): 
        self.age += 1
        if self.age >= self.reproduction_time:
            free_cells = planet.free_neighbors(self.x, self.y)
            if free_cells:
                new_x, new_y = random.choice(free_cells)
                baby_fish = Fish(new_x, new_y, age=0, reproduction_time=self.reproduction_time)
                planet.add(baby_fish, new_x, new_y)
                self.age = 0
                return baby_fish
        return None

    def is_alive(self) -> bool:
        return True

    def __str__(self):
        return f"Fish(x={self.x}, y={self.y}, age={self.age})"
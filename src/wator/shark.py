import random
from .planet import Planet

class Shark:
    def __init__(self, x: int, y:int, reproduction_time: int=5, energy: int=10, age: int=0):
        self.x = x
        self.y = y
        self.age = age
        self.reproduction_time = reproduction_time
        self.energy = energy
    
    def update_stats(self, energy: int):
        self.age += 1
        self.energy += energy

    def reproduce(self, planet: Planet, old_position: tuple[int, int]) -> None:
        if self.age % self.reproduction_time == 0:
            baby_shark = Shark(x=old_position[0], y=old_position[1])
            planet.add(baby_shark, baby_shark.x, baby_shark.y)

    def change_position(self, planet: Planet, new_position:tuple[int, int], eating: bool) -> None:
        old_position = (self.x, self.y)
        move_allowed = planet.move(self.x, self.y, new_position[0], new_position[1])
        energy = 5 if eating else -1
        if move_allowed:
            self.update_stats(energy)
            self.x = new_position[0]
            self.y = new_position[1]
            self.reproduce(planet, old_position)
        else:
            self.ask_direction(planet)

    def move(self, planet: Planet, new_position: tuple[int, int]) -> None:
        eating = False
        self.change_position(planet, new_position, eating)

    def eat(self, planet: Planet, new_position: tuple[int, int]) -> None:
        eating = True
        self.change_position(planet, new_position, eating)

    def ask_direction(self, planet: Planet) -> None:
        def generate_random_index(liste: list) -> int:
            i = random.randint(0, len(liste) - 1)
            return i

        adjacent_fishes = planet.fish_neighbors(self.x, self.y)
        if len(adjacent_fishes) == 1:
            self.eat(planet, adjacent_fishes[0])
        elif len(adjacent_fishes) > 1:
            fish_random = generate_random_index(adjacent_fishes)
            self.eat(planet, adjacent_fishes[fish_random])
        else:
            adjacent_free = planet.free_neighbors(self.x, self.y)
            if len(adjacent_free) == 1:
                self.move(planet, adjacent_free[0])
            elif len(adjacent_free) > 1:
                free_random = generate_random_index(adjacent_free)
                self.move(planet, adjacent_free[free_random])
            else:
                self.update_stats(-1)

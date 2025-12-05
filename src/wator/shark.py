import random
from .planet import Planet
from .fish import Fish

class Shark(Fish):
    def __init__(self, x, y, age, reproduction_time: int=5, energy: int=10):
        super().__init__(x, y, age=0)
        self.reproduction_time = reproduction_time
        self.energy = energy

    def reproduce(self, planet: Planet, old_position: tuple[int, int]) -> None:
        if self.age > 0 and self.age % self.reproduction_time == 0:
            baby_shark = Shark(x=old_position[0], y=old_position[1])
            planet.add(baby_shark, baby_shark.x, baby_shark.y)

    def eat(self, planet: Planet, new_position: tuple[int, int]) -> None:
        self.move(planet, new_position)
        if self.energy >= 7:
            self.energy = 10
        else:
            self.energy += 3

    def check_if_dead(self, planet: Planet) -> None:
        if self.energy <= 0:
            planet.remove(self.x, self.y)

    def search_fish(self, planet: Planet) -> None:
        adjacent_fishes = planet.fish_neighbors(self.x, self.y)
        if adjacent_fishes:
            self.move(planet, random.choice(adjacent_fishes))
        else:
            self.ask_direction(planet)
            self.energy -= 1
            self.check_if_dead(planet)

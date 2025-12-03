import random

class Shark:
    def __init__(self, id: int, position: tuple, reproduction_time: int=5, energy: int=10, age: int=0):
        self.id = id
        self.position = position
        self.age = age
        self.reproduction_time = reproduction_time
        self.energy = energy
    
    def move(self, planet: object, new_position: tuple[int, int]) -> None:
        move_allowed = planet.allow_move(new_position)
        if move_allowed:
            planet.update_position(self, new_position)
            self.energy -= 1
            self.age += 1
            self.position = new_position
        else:
            self.ask_direction()
    
    def eat(self, planet: object, new_position: tuple[int, int]) -> None:
        move_allowed = planet.move(new_position)
        if move_allowed:
            planet.remove(new_position)
            planet.set(self, new_position)
            self.energy += 5
            self.age += 1
            self.position = new_position
        else:
            self.ask_direction()

    def ask_direction(self, planet: object) -> None:
        def generate_random_index(liste: list) -> int:
            i = random.randint(0, len(liste))
            return i

        adjacent_fishes = planet.fish_neighbors(self.position)
        if len(adjacent_fishes) == 1:
            self.eat(adjacent_fishes[0])
        elif len(adjacent_fishes) > 1:
            fish_random = generate_random_index(adjacent_fishes)
            self.eat(adjacent_free[fish_random])
        else:
            adjacent_free = planet.free_neighbors(self.position)
            if len(adjacent_free) == 1:
                self.move(adjacent_free[0])
            elif len(adjacent_free) > 1:
                free_random = generate_random_index(adjacent_free)
                self.move(adjacent_free[free_random])
            else:
                self.energy -= 1
                self.age += 1
        

my_shark = Shark(id=1, position=(0,2), age=2)
my_shark.ask_direction()
from .planet import Planet
from .fish import Fish
from .shark import Shark
import random

class Simulation():
    def __init__(self, width: int, height: int, nb_fish: int, nb_shark: int):
        self.turn = 0
        self.width = width
        self.height = height
        self.nb_fish = nb_fish
        self.nb_shark = nb_shark
        self.cases = []
        
        self.planet = Planet(self.width, self.height)
        self._prepare_cases()
        self._populate_random()

        
    def _prepare_cases(self):
        for y in range(self.height):
            for x in range(self.width):
                self.cases.append((x, y))
    
    def _populate_random(self):
        random.shuffle(self.cases)
        
        if(self.nb_fish + self.nb_shark > len(self.cases)):
            raise ValueError("Too much animal for the torus size")
        
        F = self.nb_fish
        S = self.nb_shark
        
        for case in self.cases[0 : F]: 
            fish = Fish(case[0], case[1])
            self.planet.add(fish, case[0], case[1])
        
        for case in self.cases[F : F+S]:
            shark = Shark(case[0], case[1])
            self.planet.add(shark, case[0], case[1])
        
    def display(self):
        for y in range(self.height):
            line = ""
            for x in range(self.width):
                entity = self.planet.get(x, y)
                if entity is None:
                    line += ". "
                elif entity.__class__.__name__ == "Fish":
                    line += "🐟 "
                elif entity.__class__.__name__ == "Shark":
                    line += "🦈 "
            print(line)
        print()

    


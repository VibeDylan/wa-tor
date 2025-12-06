from __future__ import annotations

import random

from .planet import Planet
from .fish import Fish
from .shark import Shark


class Simulation:
    def __init__(self, width: int, height: int, nb_fish: int, nb_shark: int):
        self.turn = 0
        self.width = width
        self.height = height
        self.nb_fish = nb_fish
        self.nb_shark = nb_shark

        # listes d'agents
        self.fishes: list[Fish] = []
        self.sharks: list[Shark] = []

        # buffers pour bébés
        self.newborns_fish: list[Fish] = []
        self.newborns_shark: list[Shark] = []

        # planète
        self.planet = Planet(self.width, self.height)
        self.planet.simulation = self

        self._prepare_cases()
        self._populate_random()


    def _prepare_cases(self) -> None:
        self.cases = [(x, y) for y in range(self.height) for x in range(self.width)]

    def _populate_random(self) -> None:
        random.shuffle(self.cases)

        if self.nb_fish + self.nb_shark > len(self.cases):
            raise ValueError("Too many animals for the torus size")

        F = self.nb_fish
        S = self.nb_shark

        for (x, y) in self.cases[:F]:
            fish = Fish(x, y)
            self.fishes.append(fish)
            self.planet.add(fish, x, y)

        # requins
        for (x, y) in self.cases[F:F + S]:
            shark = Shark(x, y)
            self.sharks.append(shark)
            self.planet.add(shark, x, y)


    def display(self) -> None:
        for y in range(self.height):
            line = ""
            for x in range(self.width):
                entity = self.planet.get(x, y)
                if entity is None:
                    line += ". "
                elif isinstance(entity, Fish) and not isinstance(entity, Shark):
                    line += "🐟 "
                elif isinstance(entity, Shark):
                    line += "🦈 "
            print(line)
        print()


    def step(self) -> None:
        for f in self.fishes:
            f.has_moved = False
        for s in self.sharks:
            s.has_moved = False

        for fish in list(self.fishes):
            fish.step(self.planet)

        for shark in list(self.sharks):
            shark.step(self.planet)

        self.sharks = [
            s for s in self.sharks
            if s.energy > 0 and self.planet.get(s.x, s.y) is s
        ]

        self.fishes = [
            f for f in self.fishes
            if self.planet.get(f.x, f.y) is f
        ]

        self.fishes.extend(self.newborns_fish)
        self.sharks.extend(self.newborns_shark)

        self.newborns_fish = []
        self.newborns_shark = []

        self.turn += 1


if __name__ == "__main__":
    sim = Simulation(3, 3, 1, 1)
    for _ in range(15):
        sim.display()
        print("----------")
        sim.step()

import random
from .fish import Fish
from .shark import Shark
from .planet import Planet


class Simulation:
    
    def __init__(self, width: int, height: int, nb_fish: int, nb_shark: int):
        self.turn = 0
        self.width = width
        self.height = height
        
        self.fishes: list[Fish] = []
        self.sharks: list[Shark] = []
        self.newborns_fish: list[Fish] = []
        self.newborns_shark: list[Shark] = []
        
        self.planet = Planet(width, height)
        self.planet.simulation = self
        
        self._initialize_population(nb_fish, nb_shark)

    def _initialize_population(self, nb_fish: int, nb_shark: int) -> None:
        all_positions = [(x, y) for y in range(self.height) for x in range(self.width)]
        
        if nb_fish + nb_shark > len(all_positions):
            raise ValueError(f"Trop d'animaux ({nb_fish + nb_shark}) pour la grille ({len(all_positions)} cases)")
        
        random.shuffle(all_positions)
        
        for x, y in all_positions[:nb_fish]:
            fish = Fish(x, y)
            self.fishes.append(fish)
            self.planet.add_entity(fish, x, y)
        
        for x, y in all_positions[nb_fish:nb_fish + nb_shark]:
            shark = Shark(x, y)
            self.sharks.append(shark)
            self.planet.add_entity(shark, x, y)

    def step(self) -> None:
        for fish in self.fishes:
            fish.has_moved = False
        for shark in self.sharks:
            shark.has_moved = False

        for fish in list(self.fishes):
            fish.step(self.planet)
        
        for shark in list(self.sharks):
            shark.step(self.planet)

        self.fishes.extend(self.newborns_fish)
        self.sharks.extend(self.newborns_shark)
        self.newborns_fish.clear()
        self.newborns_shark.clear()

        self.sharks = [s for s in self.sharks if s.energy > 0 and self.planet.get(s.x, s.y) is s]
        self.fishes = [f for f in self.fishes if self.planet.get(f.x, f.y) is f]

        self.turn += 1

    def display(self) -> None:
        print(f"Tour {self.turn} - Poissons: {len(self.fishes)} - Requins: {len(self.sharks)}")
        for y in range(self.height):
            line = ""
            for x in range(self.width):
                entity = self.planet.get(x, y)
                if entity is None:
                    line += ". "
                elif isinstance(entity, Shark):
                    line += "🦈 "
                else:
                    line += "🐟 "
            print(line)
        print()

    def get_stats(self) -> dict:   
        return {
            "turn": self.turn,
            "fish_count": len(self.fishes),
            "shark_count": len(self.sharks),
            "total_population": len(self.fishes) + len(self.sharks)
        }


if __name__ == "__main__":
    sim = Simulation(width=10, height=10, nb_fish=20, nb_shark=5)
    
    for _ in range(30):
        sim.display()
        sim.step()
        
        stats = sim.get_stats()
        if stats["fish_count"] == 0:
            print("❌ Tous les poissons ont disparu !")
            break
        if stats["shark_count"] == 0:
            print("❌ Tous les requins ont disparu !")
            break

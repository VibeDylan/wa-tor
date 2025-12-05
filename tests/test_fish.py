from src.wator.fish import Fish
from src.wator.planet import Planet
import random

class TestFishMove:
    def test_move_fish_and_update_position_and_age(self):
        planet = Planet(5, 5)
        fish = Fish(1, 1, age=0)

        planet.set(1, 1, fish)
        
        fish.move(planet, (1, 2))
        
        
        assert fish.x == 1
        assert fish.y == 2
        
        assert fish.age == 1
        
        assert planet.get(1, 1) is None
        assert planet.get(1, 2) is fish
        
        
class TestFishAskDirection:
    def test_ask_direction_moves_to_free_cell(self, monkeypatch):
        planet = Planet(5, 5)
        fish = Fish(2, 2, age=0)
        planet.set(2, 2, fish)
        
        def fake_choise(seq):
            return (2 , 3)
        
        monkeypatch.setattr(random, "choice", fake_choise)
        fish.ask_direction(planet)
        
        assert fish.x == 2
        assert fish.y == 3
        
        assert planet.get(2 ,2) is None
        assert planet.get(2, 3) is fish
        
        assert fish.age == 2
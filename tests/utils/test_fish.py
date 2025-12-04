from src.wator.fish import Fish
from src.wator.planet import Planet

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
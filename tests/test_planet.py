from src.wator.planet import Planet
from src.wator.fish import Fish

class TestPlanetInitialisation:
    def test_grid_dimensions(self):
        planet = Planet(width=5, height=5)
        grid = planet._grid
        
        assert len(grid) == 5, "La grille doit avoir 5 lignes"
        assert len(grid[0]) == 5, "Chaque ligne doit avoir 5 colonnes"
        
class TestPlanetWrap:
    def test_wrap_negative(self):
        planet = Planet(5, 5)
        
        result = planet.wrap(-1, 2)
        assert result == (4, 2)
        
    def test_wrap_overflow(self):
        planet = Planet(5, 5)
        result = planet.wrap(5, 3)
        
        assert result == (0, 3)
        
    def test_wrap_inside_bounds(self):
        planet = Planet(5,5)
        
        result = planet.wrap(3, 2)
        
        assert result == (3,2)
        
class TestPlanetIsFree:
    def test_empty_cell_is_free(self):
        planet = Planet(5, 5)
        
        result = planet.is_free(2, 3)
        
        assert result == True
        
    def test_occupied_cell_is_not_free(self):
        planet = Planet(5,5)
        fish = Fish(1, 2)
        planet.set(1, 2, fish)
        
        result = planet.is_free(1, 2)
        
        assert result == False
        
class TestPlanetNeighbors:
    def test_neighbors_center(self):
        planet = Planet(5, 5)

        result = planet.neighbors(2, 2)
        assert result == [(2, 1), (2, 3), (1, 2), (3,2)]
        
    def test_neighbors_with_wrap(self):
        planet = Planet(5,5)
        
        result = planet.neighbors(0, 0)
        assert result == [(0, 4), (0, 1), (4, 0), (1, 0)]
        

class TestPlanetFreeNeighbors:
    def test_all_neighbors_free(self):
        planet = Planet(5, 5)
         
        result = planet.free_neighbors(2, 2)
        assert result == [(2, 1), (2, 3), (1, 2), (3,2)]
        
    def test_some_neighbors_occupied(self):
        planet = Planet(5, 5)
        
        fish = Fish(2, 1)
        planet.set(2, 1, fish)
        
        result = planet.free_neighbors(2, 2)
        assert result == [(2, 3), (1, 2), (3,2)]
        
    def test_no_free_neighbors(self):
        planet = Planet(5,5)
        planet.set(2,1, Fish(2,1))
        planet.set(2,3, Fish(2,3))
        planet.set(1,2, Fish(1,2))
        planet.set(3,2, Fish(3,2))
        
        result = planet.free_neighbors(2, 2)
        assert result == []
        
class TestPlanetMove:
    def test_move_into_empty_cell(self):
        planet = Planet(5, 5)
        fish = Fish(1, 1)
        
        planet.set(1, 1, fish)
        
        result = planet.move(1 , 1, 2, 2)
        
        assert result == True
        assert planet.get(1 , 1) is None
        assert planet.get(2, 2) is fish
        
    def test_move_into_occupied_cell_by_fish(self):
        planet = Planet(5, 5)
        fish = Fish(1, 1)
        fish2 = Fish(1, 2)
        
        planet.set(1, 1, fish)
        planet.set(1, 2, fish2)
        
        result = planet.move(1,1, 1, 2)
        
        assert result == False
        assert planet.get(1 , 1) is fish
        assert planet.get(1, 2) is fish2
         
        
    
        
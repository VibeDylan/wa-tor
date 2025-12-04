from src.wator.planet import Planet

class TestPlanetInitialisation():
    def test_grid_dimensions(self):
        planet = Planet(width=5, height=5)
        grid = planet._grid
        
        assert len(grid) == 5, "La grille doit avoir 5 lignes"
        assert len(grid[0]) == 5, "Chaque ligne doit avoir 5 colonnes"
        
class TestPlanetWrap():
    def test_wrap_negative(self):
        planet = Planet(5, 5)
        
        result = planet.wrap(-1, 2)
        assert(result == (4, 2))
        
    def test_wrap_overflow(self):
        planet = Planet(5, 5)
        result = planet.wrap(5, 3)
        
        assert(result == (0, 3))
        
    def test_wrap_inside_bounds(self):
        planet = Planet(5,5)
        
        result = planet.wrap(3, 2)
        
        assert(result == (3,2))
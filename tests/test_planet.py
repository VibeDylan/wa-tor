from src.wator.planet import Planet

class TestPlanetInitialisation():
    def test_grid_dimensions(self):
        planet = Planet(width=5, height=5)
        grid = planet._grid
        
        assert len(grid) == 5, "La grille doit avoir 5 lignes"
        assert len(grid[0]) == 5, "Chaque ligne doit avoir 5 colonnes"
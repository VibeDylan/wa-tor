class Planet:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        
        self._grid: list[list[object | None]] = [
            [None for _ in range(width)]
            for _ in range(height)
        ]
        
    # ----- ACCÈS BASIQUE -----
    def get(self, x: int, y: int):
        """Retourne le contenu de la case."""
        return self._grid[x][y]
    
    def set(self, x: int, y: int, entity) -> None:
        """Place une entité dans la case (ou None)."""
        self._grid[y][x] = entity
       
    # ---- OUTILS INTERNE -----
    def wrap(self, x: int, y: int) -> tuple[int, int]: 
        """Applique les règles toroïdales."""
        return x % self.width, y % self.height
    
    def is_free(self, x: int, y: int) -> bool:
        """Vrai si la case est vide."""
        return self.get(x, y) is None 
    
        
    

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
    
    # ---- ANALYSE DE VOISINAGE -----
    def neighbors(self, x: int, y: int) -> list[tuple[int, int]]:
        """Renvoie les 4 positions voisines (avec wrap)."""
        positions = [
            (x, y - 1),  # haut
            (x, y + 1),  # bas
            (x - 1, y),  # gauche
            (x + 1, y),  # droite
        ]
        return [self.wrap(nx, ny) for nx, ny in positions] 
    
    def free_neighbors(self, x: int, y: int) -> list[tuple[int, int]]:
        """Renvoie les positions voisines libres."""
        return [(nx, ny) for nx, ny in self.neighbors(x, y)
                if self.is_free(nx, ny)]

    def fish_neighbors(self, x: int, y: int) -> list[tuple[int, int]]:
        """Renvoie les positions où se trouvent des poissons."""
        return [(nx, ny) for nx, ny in self.neighbors(x, y)
                if self.get(nx, ny).__class__.__name__ == "Fish"]
    

    # ----- DÉPLACEMENT -----

    def move(self, old_x: int, old_y: int, new_x: int, new_y: int) -> bool:
        """Effectue un déplacement si possible."""
        entity = self.get(old_x, old_y)
        if entity is None:
            return False

        # Si la case est libre → autorisé
        if self.is_free(new_x, new_y):
            self.set(new_x, new_y, entity)
            self.set(old_x, old_y, None)
            return True

        # Si c’est un requin qui mange un poisson
        if entity.__class__.__name__ == "Shark":
            target = self.get(new_x, new_y)
            if target.__class__.__name__ == "Fish":
                self.set(new_x, new_y, entity)
                self.set(old_x, old_y, None)
                return True

        return False

    # ----- AJOUT / SUPPRESSION -----

    def add(self, entity, x: int, y: int) -> None:
        self.set(x, y, entity)

    def remove(self, x: int, y: int) -> None:
        self.set(x, y, None)
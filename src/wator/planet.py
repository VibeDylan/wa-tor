class Planet:
    
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        
        self._grid: list[list[object | None]] = [
            [None for _ in range(width)]
            for _ in range(height)
        ]
        
    def get(self, x: int, y: int):
        return self._grid[x][y]
    
    def set(self, x: int, y: int, entity: object) -> None:
        self._grid[y][x] = entity
       
    def wrap(self, x: int, y: int) -> tuple[int, int]: 
        return x % self.width, y % self.height
    
    def is_free(self, x: int, y: int) -> bool:
        return self.get(x, y) is None 
    
    def neighbors(self, x: int, y: int) -> list[tuple[int, int]]:
        positions = [
            (x, y - 1),  
            (x, y + 1),  
            (x - 1, y),  
            (x + 1, y), 
        ]
        return [self.wrap(nx, ny) for nx, ny in positions] 
    
    def free_neighbors(self, x: int, y: int) -> list[tuple[int, int]]:
        return [(nx, ny) for nx, ny in self.neighbors(x, y)
                if self.is_free(nx, ny)]

    def fish_neighbors(self, x: int, y: int) -> list[tuple[int, int]]:
        return [(nx, ny) for nx, ny in self.neighbors(x, y)
                if self.get(nx, ny).__class__.__name__ == "Fish"]
    

    def move(self, old_x: int, old_y: int, new_x: int, new_y: int) -> bool:
        entity = self.get(old_x, old_y)
        if entity is None:
            return False

        
        if self.is_free(new_x, new_y):
            self.set(new_x, new_y, entity)
            self.set(old_x, old_y, None)
            return True

        if entity.__class__.__name__ == "Shark":
            target = self.get(new_x, new_y)
            if target and target.__class__.__name__ == "Fish":
                self.remove(new_x, new_y)  
                self.set(new_x, new_y, entity)
                self.set(old_x, old_y, None)
                return True
        return False


    def add(self, entity, x: int, y: int) -> None:
        self.set(x, y, entity)

    def remove(self, x: int, y: int) -> None:
        self.set(x, y, None)
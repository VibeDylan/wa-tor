class Planet():
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        
        self._grid: list[list[object | None]] = [
            [None for _ in range(width)]
            for _ in range(height)
        ]
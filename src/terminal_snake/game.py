import enum

class Direction(enum.Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

    def __getitem__(self, i):
        return self.value[i]

class Snake:
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

    def __init__(self, x: int, y: int, direction: Direction):

        # List representing the coordinates
        # of tiles occupied by the snake.
        # snake[-1] is the snake's head.
        self.snake: list[tuple[int, int]] = [(x, y)]

        self.direction: Direction = direction

    # Moves snake based on direction, returns (old tail, old head)
    def update(self) -> tuple[tuple[int, int], tuple[int, int]]:
        old_head: tuple[int, int] = self.head()
        head: tuple[int, int] = (self.head()[0] + self.direction[0], 
                                self.head()[1] + self.direction[1])
        old_tail: tuple[int, int] = self.snake.pop(0)

        self.snake.append(head)
        return old_tail, old_head

    def head(self) -> tuple[int, int]:
        return self.snake[-1]
    
    def set_direction(self, new_direction: Direction) -> None:
        self.direction = new_direction
    
class World:
    def __init__(self, width: int, height: int):
        self.width: int = width
        self.height: int = height
        self.snakes: list[Snake] = []

    # Returns (list of old snake tiles, list of old heads)
    def update(self) -> tuple[list[tuple], list[tuple]]:
        old_tiles = []
        old_heads = []
        for s in self.snakes:
            old_tail, old_head = s.update()
            old_tiles.append(old_tail)
            old_heads.append(old_head)
        
        # Remove dead snakes
        dead: list[Snake] = self.get_dead_snakes()
        for d in dead:
            old_tiles.extend(d.snake)
        self.snakes = [s for s in self.snakes if s not in dead]

        return old_tiles, old_heads
        
    # Returns list of snakes that have collided
    # with a wall or with another snake (TODO).
    def get_dead_snakes(self) -> list[Snake]:
        dead: list[Snake] = []

        for s in self.snakes:
            x, y = s.head()
            if self.width - 1 <= x <= 0 or self.height - 1 <= y <= 0:
                dead.append(s)

        return dead
    

    # Spawns a new snake at x, y, moving in direction
    def spawn_snake(self, x: int, y: int, direction: Direction) -> Snake:
        self.snakes.append(Snake(x, y, direction))
        return self.snakes[-1]




    







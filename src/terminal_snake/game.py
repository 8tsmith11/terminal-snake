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

    # Moves snake based on direction, returns (tail, head)
    def update(self) -> tuple[tuple[int, int], tuple[int, int]]:
        head: tuple[int, int] = (self.head()[0] + self.direction[0], 
                                self.head()[1] + self.direction[1])
        tail: tuple[int, int] = self.snake.pop(0)
        self.snake.append(head)
        return tail, head

    def head(self) -> tuple[int, int]:
        return self.snake[-1]
    
    def set_direction(self, new_direction: Direction) -> None:
        self.direction = new_direction
    
class World:
    def __init__(self, width: int, height: int):
        self.width: int = width
        self.height: int = height
        self.snakes: list[Snake] = [Snake(0, 0, Direction.RIGHT)]

    def update(self) -> None:
        for s in self.snakes:
            s.update()
        
        # Remove dead snakes
        self.snakes = [s for s in self.snakes if s not in self.get_dead_snakes()]
        
    # Returns list of snakes that have collided
    # with a wall or with another snake (TODO).
    def get_dead_snakes(self) -> list[Snake]:
        dead: list[Snake] = []

        for s in self.snakes:
            x, y = s.head()
            if self.width <= x < 0 or self.height <= y < 0:
                dead.append(s)

        return dead




    







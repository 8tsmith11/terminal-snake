import enum
import random
from typing import Optional

class Direction(enum.Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

    def __getitem__(self, i):
        return self.value[i]

class Snake:
    def __init__(self, x: int, y: int, direction: Direction):

        # List representing the coordinates
        # of tiles occupied by the snake.
        # snake[-1] is the snake's head.
        self.snake: list[tuple[int, int]] = [(x, y)]

        self.direction: Direction = direction

    def update(self, is_fed: bool) -> tuple[Optional[tuple[int, int]], tuple[int, int]]:
        """Moves snake based on direction, returns (old tail, old head)"""

        old_head: tuple[int, int] = self.head()
        head: tuple[int, int] = self.next_tile()
        
        # Move tail tile only if the snake was not fed (effectively grow if fed).
        old_tail: tuple[int, int] = self.snake.pop(0) if not is_fed else None

        self.snake.append(head)
        return old_tail, old_head

    def head(self) -> tuple[int, int]:
        return self.snake[-1]
    
    def set_direction(self, new_direction: Direction) -> None:
        self.direction = new_direction

    def next_tile(self) -> tuple[int, int]:
        """Returns the next tile that the snake will move to."""
        return (self.head()[0] + self.direction[0], self.head()[1] + self.direction[1])

    
class World:
    TOTAL_FOOD = 10

    def __init__(self, width: int, height: int):
        self.width: int = width
        self.height: int = height
        self.snakes: list[Snake] = []
        self.food: list[tuple[int, int]] = []
        self.food = [self.random_empty() for _ in range(World.TOTAL_FOOD)]

    # Returns (list of old snake tiles, list of old heads)
    def update(self) -> tuple[list[tuple], list[tuple]]:
        old_tiles = []
        old_heads = []
        food_eaten: int = 0
        for s in self.snakes:
            next: tuple[int, int] = s.next_tile()
            is_fed: bool = False
            i: int = 0
            while not is_fed and i < len(self.food):
                is_fed = self.food[i] == next    
                i += 1

            if is_fed:
                old_heads.append(self.food.pop(i - 1))
                food_eaten += 1

            old_tail, old_head = s.update(is_fed)
            if not is_fed:
                old_tiles.append(old_tail)
            old_heads.append(old_head)

        # Respawn eaten food
        for _ in range(food_eaten):
            self.food.append(self.random_empty())
        
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
            if self.width - 1 <= x or x <= 0 or self.height - 1 <= y or y <= 0:
                dead.append(s)
                s.snake.clear()

        return dead

    # Spawns a new snake at x, y, moving in direction
    def spawn_snake(self, x: int, y: int, direction: Direction) -> Snake:
        self.snakes.append(Snake(x, y, direction))
        return self.snakes[-1]
    
    def random_empty(self) -> tuple[int, int]:
        """Returns coordinates not occupied by food, walls, or snakes."""
        x: int = random.randint(1, self.width - 2)
        y: int = random.randint(1, self.height - 2)
        while self.is_snake_tile(x, y) or (x, y) in self.food:
            x = random.randint(1, self.width - 2)
            y = random.randint(1, self.height - 2)
        return (x, y)

    def is_snake_tile(self, x: int, y: int) -> bool:
        """Returns true if a snake contains (x, y), false otherwise."""
        for s in self.snakes:
            for t in s.snake:
                if x == t[0] and y == t[1]:
                    return True
        return False
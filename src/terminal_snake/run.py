import curses
import time
from typing import Optional
from . import game

HEAD_CHAR = '@'
BODY_CHAR = '#'
FOOD_CHAR = 'F'

SECONDS_PER_TICK: float = 0.1

class GameRunner:
    def __init__(self, stdscr: curses.window):
        self.stdscr: curses.window = stdscr

        # Dont wait for input
        stdscr.nodelay(True)

        # Hide the cursor
        curses.curs_set(0)
    
    def run(self) -> None:
        world: game.World = game.World(curses.COLS - 2, curses.LINES - 2)
        player: game.Snake = world.spawn_snake(1, 1, game.Direction.RIGHT)

        last_tick: float = time.time()
        direction: game.Direction = player.direction

        self.draw_walls(world)

        # Game loop
        while True:
            # User input
            input = self.stdscr.getch()
            if input == ord('q'):
                break

            # Change direction
            if input == curses.KEY_UP or input == ord('w') or input == ord('W'):
                direction = game.Direction.UP
            elif input == curses.KEY_DOWN or input == ord('s') or input == ord('S'):
                direction = game.Direction.DOWN
            elif input == curses.KEY_LEFT or input == ord('a') or input == ord('A'):
                direction = game.Direction.LEFT
            elif input == curses.KEY_RIGHT or input == ord('d') or input == ord('D'):
                direction = game.Direction.RIGHT

            # Tick (update world) every SECONDS_PER_TICK seconds.
            if time.time() - last_tick > SECONDS_PER_TICK:
                # Update world
                player.set_direction(direction)
                old_tiles, old_heads = world.update()
                self.draw_food(world)
                self.draw_snakes(world, old_tiles, old_heads)
                # Reset timer
                last_tick = time.time()


    def draw_walls(self, world: game.World) -> None:
        w, h = world.width, world.height

        # Horizontal walls
        for x in range(1, w - 1):
            self.stdscr.addch(0, x, "-")
            self.stdscr.addch(h - 1, x, "-")

        # Vertical walls
        for y in range(1, h - 1):
            self.stdscr.addch(y, 0, "|")
            self.stdscr.addch(y, w - 1, "|")

        # Corners
        self.stdscr.addch(0, 0, "+")
        self.stdscr.addch(h - 1, 0, "+")
        self.stdscr.addch(h - 1, w - 1, "+")
        self.stdscr.addch(0, w - 1, "+")

        self.stdscr.refresh()

    def draw_snakes(self, world: game.World, old_tiles, old_heads) -> None:
        # Draw heads
        for s in world.snakes:
            x, y = s.snake[-1]
            self.stdscr.addch(y, x, HEAD_CHAR)

        # Draw bodies
        for tile in old_heads:
            self.stdscr.addch(tile[1], tile[0], BODY_CHAR)

        # Clear old tiles
        for tile in old_tiles:
            self.stdscr.addch(tile[1], tile[0], ' ')

    def draw_food(self, world: game.World) -> None:
        for f in world.food:
            x, y = f
            self.stdscr.addch(y, x, FOOD_CHAR)

def main(stdscr: curses.window):
    game_runner = GameRunner(stdscr)
    game_runner.run()
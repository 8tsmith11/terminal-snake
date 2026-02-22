import curses
import time
from . import game

HEAD_CHAR = '@'
BODY_CHAR = '#'

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

        self.draw_walls(world)

        # Game loop
        while True:
            # User input
            input = self.stdscr.getch()
            if input == ord('q'):
                break

            # Change direction
            elif input == curses.KEY_UP or input == ord('w'):
                player.set_direction(game.Direction.UP)
            elif input == curses.KEY_DOWN or input == ord('s'):
                player.set_direction(game.Direction.DOWN)
            elif input == curses.KEY_LEFT or input == ord('a'):
                player.set_direction(game.Direction.LEFT)
            elif input == curses.KEY_RIGHT or input == ord('d'):
                player.set_direction(game.Direction.RIGHT)
            
            old_tiles, old_heads = world.update()

            self.draw_snakes(world, old_tiles, old_heads)

            time.sleep(0.1)

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

def main(stdscr: curses.window):
    game_runner = GameRunner(stdscr)
    game_runner.run()
from curses import wrapper
from . import run

if __name__ == "__main__":
    wrapper(run.main)
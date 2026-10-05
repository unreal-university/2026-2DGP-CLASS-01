"""Play the Sonic animations stored in sonic-sprite.png."""

from pico2d import open_canvas, close_canvas

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800


def main():
    """Run the animation viewer."""
    open_canvas(WINDOW_WIDTH, WINDOW_HEIGHT)
    close_canvas()


if __name__ == '__main__':
    main()

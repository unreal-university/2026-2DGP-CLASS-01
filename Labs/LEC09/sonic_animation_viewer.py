"""Play the Sonic animations stored in sonic-sprite.png."""

from pico2d import open_canvas, close_canvas, get_events, SDL_QUIT

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800


def main():
    """Run the animation viewer."""
    open_canvas(WINDOW_WIDTH, WINDOW_HEIGHT)
    try:
        running = True
        while running:
            for event in get_events():
                if event.type == SDL_QUIT:
                    running = False
    finally:
        close_canvas()


if __name__ == '__main__':
    main()

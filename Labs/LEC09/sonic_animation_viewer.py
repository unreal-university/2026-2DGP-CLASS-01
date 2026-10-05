"""Play the Sonic animations stored in sonic-sprite.png."""

from pathlib import Path

from pico2d import open_canvas, close_canvas, get_events, SDL_QUIT

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
IMAGE_PATH = Path(__file__).resolve().with_name('sonic-sprite.png')


def main():
    """Run the animation viewer."""
    if not IMAGE_PATH.is_file():
        raise FileNotFoundError(f'스프라이트 이미지를 찾을 수 없습니다: {IMAGE_PATH}')

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

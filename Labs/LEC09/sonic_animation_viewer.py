"""Play the Sonic animations stored in sonic-sprite.png."""

from pathlib import Path

from pico2d import open_canvas, close_canvas, get_events, load_image, SDL_QUIT

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
IMAGE_PATH = Path(__file__).resolve().with_name('sonic-sprite.png')

# 시트 위에서 아래로 배치된 소닉 동작. 마지막 장식/크레딧 행은 제외한다.
# 각 항목은 (이름, 시트 행, 시작 프레임, 끝 프레임[미포함], 초당 프레임 수)이다.
ANIMATION_PLAN = (
    ('자세 변화', 0, 0, 11, 8),
    ('달리기', 1, 0, 12, 12),
    ('질주', 2, 0, 6, 10),
    ('회전 진입', 3, 0, 9, 12),
    ('볼 회전', 4, 0, 6, 10),
    ('스핀 대시', 5, 0, 6, 12),
    ('고속 대시', 6, 0, 6, 12),
    ('방향 전환', 7, 0, 6, 8),
    ('공중 포즈', 7, 6, 8, 6),
    ('정면 동작', 8, 0, 8, 8),
    ('환호', 9, 0, 2, 4),
    ('착지', 9, 2, 4, 4),
)


def main():
    """Run the animation viewer."""
    if not IMAGE_PATH.is_file():
        raise FileNotFoundError(f'스프라이트 이미지를 찾을 수 없습니다: {IMAGE_PATH}')

    open_canvas(WINDOW_WIDTH, WINDOW_HEIGHT)
    try:
        sprite_sheet = load_image(str(IMAGE_PATH))
        running = True
        while running:
            for event in get_events():
                if event.type == SDL_QUIT:
                    running = False
    finally:
        close_canvas()


if __name__ == '__main__':
    main()

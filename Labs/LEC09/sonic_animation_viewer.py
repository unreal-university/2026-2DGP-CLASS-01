"""Play the Sonic animations stored in sonic-sprite.png."""

from pathlib import Path

from pico2d import (
    SDL_QUIT, clear_canvas, close_canvas, delay, get_events, get_time, load_image,
    open_canvas, update_canvas,
)

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
SHEET_HEIGHT = 525
SPRITE_SCALE = 8
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

# (시트에서의 위쪽 y, 아래쪽 y, 프레임 간 x 경계)
# 각 프레임은 이 경계 안에서 잘라 인접한 그림을 포함하지 않는다.
ROW_LAYOUTS = (
    (36, 75, (0, 29, 57, 85, 115, 145, 175, 205, 235, 265, 299, 334)),
    (76, 117, (0, 34, 64, 96, 128, 160, 193, 225, 258, 291, 327, 366, 399)),
    (118, 165, (0, 37, 84, 127, 176, 222, 265)),
    (166, 204, (0, 33, 65, 97, 130, 161, 192, 226, 265, 300)),
    (205, 238, (0, 34, 68, 102, 137, 171, 210)),
    (239, 276, (0, 34, 70, 108, 145, 182, 220)),
    (279, 320, (0, 34, 69, 115, 167, 213, 260)),
)


def draw_frame(sprite_sheet, row_index, frame_index):
    """Draw a frame around the same screen center regardless of its width."""
    top, bottom, edges = ROW_LAYOUTS[row_index]
    left, right = edges[frame_index:frame_index + 2]
    sprite_sheet.clip_draw(
        left, SHEET_HEIGHT - bottom, right - left, bottom - top,
        WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2,
        (right - left) * SPRITE_SCALE, (bottom - top) * SPRITE_SCALE,
    )


def main():
    """Run the animation viewer."""
    if not IMAGE_PATH.is_file():
        raise FileNotFoundError(f'스프라이트 이미지를 찾을 수 없습니다: {IMAGE_PATH}')

    open_canvas(WINDOW_WIDTH, WINDOW_HEIGHT)
    try:
        sprite_sheet = load_image(str(IMAGE_PATH))
        last_time = get_time()
        frame_elapsed = 0.0
        frame_index = 0
        running = True
        while running:
            now = get_time()
            frame_elapsed += now - last_time
            last_time = now
            frame_duration = 1.0 / ANIMATION_PLAN[0][4]
            while frame_elapsed >= frame_duration:
                frame_elapsed -= frame_duration
                frame_index = (frame_index + 1) % ANIMATION_PLAN[0][3]
            for event in get_events():
                if event.type == SDL_QUIT:
                    running = False
            clear_canvas()
            draw_frame(sprite_sheet, 0, frame_index)
            update_canvas()
            delay(0.01)
    finally:
        close_canvas()


if __name__ == '__main__':
    main()

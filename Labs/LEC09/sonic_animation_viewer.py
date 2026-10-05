"""Play the Sonic animations stored in sonic-sprite.png."""

from pathlib import Path

from pico2d import (
    SDL_QUIT, clear_canvas, close_canvas, delay, get_events, get_time, load_image,
    open_canvas, update_canvas,
)

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
SHEET_WIDTH = 399
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
    (36, 75, (0, 29, 57, 85, 115, 145, 182, 211, 238, 265, 299, 334)),
    (80, 117, (0, 34, 64, 96, 132, 169, 203, 236, 264, 295, 334, 370, 399)),
    (118, 165, (0, 37, 84, 127, 176, 222, 265)),
    (166, 204, (0, 33, 65, 97, 130, 161, 192, 226, 265, 300)),
    (205, 238, (0, 34, 68, 102, 137, 171, 210)),
    (239, 276, (0, 34, 70, 108, 145, 182, 220)),
    (279, 320, (0, 34, 69, 115, 167, 213, 260)),
    (324, 374, (0, 29, 62, 87, 117, 146, 178, 228, 275)),
    (376, 421, (0, 30, 63, 97, 134, 172, 212, 251, 290)),
    (423, 468, (0, 44, 93, 123, 150)),
)

# 맞닿아 있는 그림의 잔상을 피하기 위해 일부 프레임만 별도로 좁힌다.
FRAME_BOUNDS = {
    (0, 7): (211, 235),
    (1, 4): (136, 169),
}


def validate_animation_data():
    """Check every Sonic frame is included exactly once in the plan."""
    available = set()
    for row, (top, bottom, edges) in enumerate(ROW_LAYOUTS):
        if not (0 <= top < bottom <= SHEET_HEIGHT):
            raise ValueError(f'{row}번 행의 세로 좌표가 잘못되었습니다.')
        if edges[0] < 0 or edges[-1] > SHEET_WIDTH or any(
            left >= right for left, right in zip(edges, edges[1:])
        ):
            raise ValueError(f'{row}번 행의 가로 좌표가 잘못되었습니다.')
        available.update((row, frame) for frame in range(len(edges) - 1))

    planned = []
    for name, row, start, end, fps in ANIMATION_PLAN:
        if row >= len(ROW_LAYOUTS) or fps <= 0 or start < 0 or start >= end:
            raise ValueError(f'{name} 동작 설정이 잘못되었습니다.')
        planned.extend((row, frame) for frame in range(start, end))
    if len(planned) != len(available) or set(planned) != available:
        raise ValueError('동작 목록에 빠지거나 중복된 프레임이 있습니다.')


def draw_frame(sprite_sheet, row_index, frame_index):
    """Draw a frame around the same screen center regardless of its width."""
    top, bottom, edges = ROW_LAYOUTS[row_index]
    left, right = FRAME_BOUNDS.get(
        (row_index, frame_index), edges[frame_index:frame_index + 2]
    )
    sprite_sheet.clip_draw(
        left, SHEET_HEIGHT - bottom, right - left, bottom - top,
        WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2,
        (right - left) * SPRITE_SCALE, (bottom - top) * SPRITE_SCALE,
    )


def main():
    """Run the animation viewer."""
    validate_animation_data()
    if not IMAGE_PATH.is_file():
        raise FileNotFoundError(f'스프라이트 이미지를 찾을 수 없습니다: {IMAGE_PATH}')

    open_canvas(WINDOW_WIDTH, WINDOW_HEIGHT)
    try:
        sprite_sheet = load_image(str(IMAGE_PATH))
        if (sprite_sheet.w, sprite_sheet.h) != (SHEET_WIDTH, SHEET_HEIGHT):
            raise ValueError(
                f'스프라이트 이미지 크기가 다릅니다: '
                f'{sprite_sheet.w}x{sprite_sheet.h} (필요: {SHEET_WIDTH}x{SHEET_HEIGHT})'
            )
        last_time = get_time()
        frame_elapsed = 0.0
        animation_index = 0
        frame_index = 0
        completed_loops = 0
        playing = True
        pause_started = None
        running = True
        while running:
            now = get_time()
            frame_elapsed += now - last_time
            last_time = now
            name, row, start, end, fps = ANIMATION_PLAN[animation_index]
            frame_duration = 1.0 / fps
            while playing and frame_elapsed >= frame_duration:
                frame_elapsed -= frame_duration
                if frame_index == end - start - 1:
                    completed_loops += 1
                    if completed_loops == 5:
                        playing = False
                        pause_started = now
                        frame_elapsed = 0.0
                    else:
                        frame_index = 0
                else:
                    frame_index += 1
            pause_ready = not playing and now - pause_started >= 1.0
            if pause_ready:
                animation_index = (animation_index + 1) % len(ANIMATION_PLAN)
                frame_index = 0
                completed_loops = 0
                frame_elapsed = 0.0
                playing = True
                pause_started = None
                _, row, start, _, _ = ANIMATION_PLAN[animation_index]
            for event in get_events():
                if event.type == SDL_QUIT:
                    running = False
            clear_canvas()
            draw_frame(sprite_sheet, row, start + frame_index)
            update_canvas()
            delay(0.01)
    finally:
        close_canvas()


if __name__ == '__main__':
    main()

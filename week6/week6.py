import time
import random
import spidev
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

# OLED.py
i2c = board.I2C()
# 해상도 128x64 및 I2C 통신 설정
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)

WIDTH = oled.width
HEIGHT = oled.height

image = Image.new("1", (WIDTH, HEIGHT))
draw = ImageDraw.Draw(image)
font = ImageFont.load_default()

# MCP3008.py
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1000000

SW_CHANNEL = 0
VRX_CHANNEL = 1
VRY_CHANNEL = 2


def readadc(adcnum):
    if adcnum < 0 or adcnum > 7:
        return -1
    r = spi.xfer2([1, (8 + adcnum) << 4, 0])
    data = ((r[1] & 3) << 8) + r[2]
    return data


CELL_SIZE = 4
GRID_WIDTH = WIDTH // CELL_SIZE
GRID_HEIGHT = HEIGHT // CELL_SIZE

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


def draw_text_center(text, y):
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    x = (WIDTH - text_width) // 2
    draw.text((x, y), text, font=font, fill=255)


def spawn_food(snake):
    while True:
        food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        if food not in snake:
            return food


def reset_game():
    snake = [
        (GRID_WIDTH // 2, GRID_HEIGHT // 2),
        (GRID_WIDTH // 2 - 1, GRID_HEIGHT // 2),
        (GRID_WIDTH // 2 - 2, GRID_HEIGHT // 2),
    ]
    direction = RIGHT
    next_direction = RIGHT
    food = spawn_food(snake)
    score = 0
    game_over = False
    return snake, direction, next_direction, food, score, game_over


def show_start_screen():
    draw.rectangle((0, 0, WIDTH, HEIGHT), outline=0, fill=0)
    draw_text_center("Mini Snake", 12)
    draw_text_center("Joystick: Move", 28)
    draw_text_center("Press SW to Start", 44)
    oled.image(image)
    oled.show()


def show_game_over(score):
    draw.rectangle((0, 0, WIDTH, HEIGHT), outline=0, fill=0)
    draw_text_center("GAME OVER", 14)
    draw_text_center(f"Score: {score}", 30)
    draw_text_center("Press SW", 46)
    oled.image(image)
    oled.show()


def show_countdown():
    for n in ["3", "2", "1"]:
        draw.rectangle((0, 0, WIDTH, HEIGHT), outline=0, fill=0)
        draw_text_center(n, 24)
        oled.image(image)
        oled.show()
        time.sleep(0.5)


def read_joystick_direction(current_direction):
    vrx = readadc(VRX_CHANNEL)  # L R
    vry = readadc(VRY_CHANNEL)  # T B

    # 기준값은 조이스틱마다 다를 수 있음 (0~1023 사이, 중간값 약 512)
    if vrx < 400 and current_direction != RIGHT:
        return LEFT
    elif vrx > 600 and current_direction != LEFT:
        return RIGHT
    elif vry < 400 and current_direction != DOWN:
        return UP
    elif vry > 600 and current_direction != UP:
        return DOWN

    return current_direction


def wait_for_button_press():
    while True:
        sw = readadc(SW_CHANNEL)
        if sw < 100:  # 모듈에 따라 기준값 조정 (눌렀을 때 보통 0에 가까워짐)
            time.sleep(0.25)  # 디바운싱
            return
        time.sleep(0.05)


# starting screen
show_start_screen()
wait_for_button_press()
show_countdown()

snake, direction, next_direction, food, score, game_over = reset_game()

last_move_time = time.time()
move_interval = 0.18  # 작을수록 뱀이 빨라짐

# main loop
while True:
    if not game_over:
        # 조이스틱 입력 반영
        next_direction = read_joystick_direction(direction)

        now = time.time()
        if now - last_move_time >= move_interval:
            direction = next_direction
            head_x, head_y = snake[0]
            dx, dy = direction
            new_head = (head_x + dx, head_y + dy)

            # 벽 충돌 체크
            if (
                new_head[0] < 0
                or new_head[0] >= GRID_WIDTH
                or new_head[1] < 0
                or new_head[1] >= GRID_HEIGHT
            ):
                game_over = True

            # 자기 몸 충돌 체크
            elif new_head in snake:
                game_over = True

            else:
                snake.insert(0, new_head)

                # 사과 먹음
                if new_head == food:
                    score += 1
                    food = spawn_food(snake)

                    # 점수가 올라가면 조금씩 빨라짐
                    if move_interval > 0.07:
                        move_interval -= 0.005
                else:
                    snake.pop()  # 사과를 못 먹었으면 꼬리 자르기

            last_move_time = now

            # 화면 그리기 초기화
            draw.rectangle((0, 0, WIDTH, HEIGHT), outline=0, fill=0)

            # 점수 표시
            draw.text((0, 0), f"S:{score}", font=font, fill=255)

            # 사과 그리기
            fx, fy = food
            draw.rectangle(
                (
                    fx * CELL_SIZE,
                    fy * CELL_SIZE,
                    fx * CELL_SIZE + CELL_SIZE - 1,
                    fy * CELL_SIZE + CELL_SIZE - 1,
                ),
                outline=255,
                fill=255,
            )

            # 뱀 그리기
            for i, (x, y) in enumerate(snake):
                x0 = x * CELL_SIZE
                y0 = y * CELL_SIZE
                x1 = x0 + CELL_SIZE - 1
                y1 = y0 + CELL_SIZE - 1

                # 머리는 꽉 채우고, 몸통은 테두리만
                if i == 0:
                    draw.rectangle((x0, y0, x1, y1), outline=255, fill=255)
                else:
                    draw.rectangle((x0, y0, x1, y1), outline=255, fill=0)

            oled.image(image)
            oled.show()

    else:
        # game over state
        show_game_over(score)
        wait_for_button_press()
        show_countdown()
        snake, direction, next_direction, food, score, game_over = reset_game()
        move_interval = 0.18
        last_move_time = time.time()

    time.sleep(0.01)

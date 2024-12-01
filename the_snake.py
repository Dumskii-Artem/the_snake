from random import randint, choice

import pygame as pg

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

BOARD_BACKGROUND_COLOR = (225, 225, 225)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (50, 150, 50)
COLOR_BLACK = (0, 0, 0)

# Скорость движения змейки:
SPEED = 2
current_speed = SPEED

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка. Поиграем!')

# Настройка времени:
clock = pg.time.Clock()


turns = {
    (UP, pg.K_RIGHT): RIGHT,
    (DOWN, pg.K_RIGHT): RIGHT,
    (RIGHT, pg.K_RIGHT): RIGHT,
    (LEFT, pg.K_LEFT): LEFT,
    (UP, pg.K_LEFT): LEFT,
    (DOWN, pg.K_LEFT): LEFT,
    (LEFT, pg.K_UP): UP,
    (UP, pg.K_UP): UP,
    (RIGHT, pg.K_UP): UP,
    (LEFT, pg.K_DOWN): DOWN,
    (DOWN, pg.K_DOWN): DOWN,
    (RIGHT, pg.K_DOWN): DOWN,
}

ALL_CELLS = set((x * GRID_SIZE, y * GRID_SIZE)
                for x in range(GRID_WIDTH) for y in range(GRID_HEIGHT))


class GameObject:
    """Класс GameObject"""

    def __init__(self, bg_color=COLOR_BLACK):
        """инициализируем Объект"""
        self.body_color = bg_color
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    def draw_cell(self, position, bg_color=None):
        """закраска одной клеточки"""
        rect = (pg.Rect(position, (GRID_SIZE, GRID_SIZE)))
        pg.draw.rect(screen, bg_color or self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 5)

    def clear_cell(self, position):
        """закраска одной клеточки"""
        rect = (pg.Rect(position, (GRID_SIZE, GRID_SIZE)))
        pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, rect)

    def draw(self):
        """Метод должен быть перегружен"""
        raise NotImplementedError('There isn\'t draw() method in class'
                                  f' {type(self).__name__}')


class Apple(GameObject):
    """Класс Apple"""

    def __init__(self, bg_color=APPLE_COLOR, ocupied_seats=[]):
        super().__init__(bg_color)
        self.randomize_position(ocupied_seats)

    def randomize_position(self, ocupied_seats):
        """Создаем новое яблоко. Нельзя класть яблоко на змею"""
        self.position = choice(tuple(ALL_CELLS - set(ocupied_seats)))

    def draw(self):
        """Метод draw класса Apple"""
        # **********************************************
        self.draw_cell(self.position)


class Snake(GameObject):
    """Класс Snake"""

    score = 1

    def __init__(self, bg_color=SNAKE_COLOR):
        super().__init__(bg_color)
        self.reset()

    def reset(self):
        """создаем маленькую змейку"""
        self.positions = [(randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                          randint(0, GRID_HEIGHT - 1) * GRID_SIZE)]
        self.last = None
        self.length = 1
        self.direction = RIGHT

    def get_head_position(self):
        """Ищем змеиную голову"""
        return self.positions[0]

    def move(self):
        """Кладем голову змеи на новое место"""
        head_pos_x, head_pos_y = self.get_head_position()
        direction_x, direction_y = self.direction
        self.positions.insert(0, ((head_pos_x + direction_x * GRID_SIZE
                                  + SCREEN_WIDTH) % (SCREEN_WIDTH),
                                  (head_pos_y + direction_y * GRID_SIZE
                                  + SCREEN_HEIGHT) % (SCREEN_HEIGHT)))

    def draw(self):
        """Рисуем змею (надо только кончики) тушка неподвижна"""
        # Отрисовка головы змейки
        self.draw_cell(self.get_head_position())
        # Затирание последнего сегмента
        if self.last:
            self.clear_cell(self.last)

    def check_apple(self, apple_position):
        """Здесь меняется длина змеи."""
        if self.get_head_position() == apple_position:
            self.last = None
            self.length += 1
            # фиксируем достижения
            if self.length > self.score:
                self.score = self.length
            return True
        else:
            # удалить хвост
            self.last = self.positions.pop()
            return False

    def update_direction(self, event_key):
        """кнопками меняем направление движения змеи"""
        self.direction = turns.get((self.direction, event_key), self.direction)


def handle_keys(snake_object):
    """Функция обработки действий пользователя"""
    global current_speed
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                pg.quit()
                raise SystemExit
            elif event.key == pg.K_1:
                current_speed *= 1.5
            elif event.key == pg.K_2:
                current_speed /= 1.5
            else:
                snake_object.update_direction(event.key)


def main():
    """The mainest of main function"""
    global current_speed
    # Инициализация pygame:
    pg.init()
    screen.fill(BOARD_BACKGROUND_COLOR)
    snake = Snake()
    apple = Apple(ocupied_seats=snake.positions)

    while True:
        handle_keys(snake)

        snake.move()

        if snake.get_head_position() in snake.positions[1:]:
            # Если укусили себя
            # Game Over. New Game!
            screen.fill(BOARD_BACKGROUND_COLOR)
            snake.reset()
            apple.randomize_position(snake.positions)
        elif snake.check_apple(apple.position):
            # Укусили яблоко
            apple.randomize_position(snake.positions)

        snake.draw()
        apple.draw()

        pg.display.set_caption(f'Змейка. Рекорд: {snake.score}'
                               f' (сейчас: {snake.length}).'
                               ' SPEED(1/2) Стрелочки-игра. ESC - конец!')

        pg.display.flip()

        clock.tick(current_speed)


if __name__ == '__main__':
    main()

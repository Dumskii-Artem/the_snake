from random import randint

# choice,

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

# Скорость движения змейки:
SPEED = 2
current_speed = SPEED

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка. Поиграем!')

# Настройка времени:
clock = pg.time.Clock()


where_to_go = {
    (LEFT, pg.K_RIGHT): LEFT,
    (UP, pg.K_RIGHT): RIGHT,
    (DOWN, pg.K_RIGHT): RIGHT,
    (RIGHT, pg.K_RIGHT): RIGHT,
    (LEFT, pg.K_LEFT): LEFT,
    (UP, pg.K_LEFT): LEFT,
    (DOWN, pg.K_LEFT): LEFT,
    (RIGHT, pg.K_LEFT): RIGHT,
    (LEFT, pg.K_UP): UP,
    (UP, pg.K_UP): UP,
    (DOWN, pg.K_UP): DOWN,
    (RIGHT, pg.K_UP): UP,
    (LEFT, pg.K_DOWN): DOWN,
    (UP, pg.K_DOWN): UP,
    (DOWN, pg.K_DOWN): DOWN,
    (RIGHT, pg.K_DOWN): DOWN,
}


class CodeError(Exception):
    """Обработка ошибок в коде"""

    pass


class GameObject:
    """Класс GameObject"""

    def __init__(self, bg_color=(0, 0, 0)):
        """инициализируем Объект"""
        self.body_color = bg_color
        self.position = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    def draw_cell(self, position, border_color, bg_color=None):
        """закраска одной клеточки"""
        if bg_color is None:
            bg_color = self.body_color
        rect = (pg.Rect(position, (GRID_SIZE, GRID_SIZE)))
        pg.draw.rect(screen, bg_color, rect)
        pg.draw.rect(screen, border_color, rect, 1)

    def draw(self):
        """Метод должен быть перегружен"""
        raise CodeError('There isn\'t draw() method in class'
                        f' {type(self).__name__}')


class Apple(GameObject):
    """Класс Apple"""

    def __init__(self, ocupied_seats=[]):
        GameObject.__init__(self, APPLE_COLOR)
        self.randomize_position(ocupied_seats)

    def randomize_position(self, ocupied_seats):
        """Создаем новое яблоко. Нельзя класть яблоко на змею"""
        while True:
            self.position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                             randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
            if self.position not in ocupied_seats:
                break
        self.draw()

    def draw(self):
        """Метод draw класса Apple"""
        self.draw_cell(self.position, BORDER_COLOR)


class Snake(GameObject):
    """Класс Snake"""

    max_length = 1

    def __init__(self):
        GameObject.__init__(self, SNAKE_COLOR)
        self.reset()
        self.draw()

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

    def add_head_ahead(self):
        """Вычисляем, где будет голова змеи"""
        head = self.get_head_position()
        head_pos_x = (head[0] + self.direction[0] * GRID_SIZE
                      + SCREEN_WIDTH) % (SCREEN_WIDTH)

        head_pos_y = (head[1] + self.direction[1] * GRID_SIZE
                      + SCREEN_HEIGHT) % (SCREEN_HEIGHT)

        self.positions.insert(0, (head_pos_x, head_pos_y))

    def draw(self):
        """Рисуем змею (надо только кончики) тушка неподвижна"""
        self.draw_cell(self.positions[-1], BORDER_COLOR)
        # Отрисовка головы змейки
        self.draw_cell(self.positions[0], BORDER_COLOR)
        # Затирание последнего сегмента
        if self.last:
            self.draw_cell(self.last,
                           BOARD_BACKGROUND_COLOR,
                           BOARD_BACKGROUND_COLOR)

    def move_tail(self, just_eat):
        """Здесь меняется длина змеи"""
        if just_eat:
            self.last = None
            self.length += 1
            if self.length > self.max_length:
                self.max_length = self.length
        else:
            # удалить хвост
            self.last = self.positions.pop()


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
                snake_object.direction = where_to_go.get(
                    (snake_object.direction, event.key),
                    snake_object.direction)


def main():
    """The mainest of main function"""
    global current_speed
    # Инициализация pygame:
    pg.init()
    screen.fill(BOARD_BACKGROUND_COLOR)
    snake = Snake()
    apple = Apple(snake.positions)

    while True:
        handle_keys(snake)

        snake.add_head_ahead()

        if snake.get_head_position() in snake.positions[1:]:
            # Если укусили себя
            # Game Over. New Game!
            screen.fill(BOARD_BACKGROUND_COLOR)
            snake.reset()
            apple.randomize_position(snake.positions)
        elif snake.get_head_position() == apple.position:
            # если скушали яблоко
            snake.move_tail(True)
            apple.randomize_position(snake.positions)
        else:
            snake.move_tail(False)

        snake.draw()

        pg.display.set_caption(f'Змейка. Рекорд: {snake.max_length}'
                               f' (сейчас: {snake.length}).'
                               ' SPEED(1/2) Стрелочки-игра. ESC - конец!')

        pg.display.flip()

        clock.tick(current_speed)


if __name__ == '__main__':
    main()

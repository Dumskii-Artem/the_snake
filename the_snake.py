from random import randint

# choice,

import pygame

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

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Класс GameObject"""

    body_color = None
    position = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    def __init__(self):
        """инициализируем Объект"""
        pass

    def draw(self):
        """Рисуем Объект"""
        pass


class Apple(GameObject):
    """Класс Apple"""

    def __init__(self):
        self.randomize_position()
        self.body_color = APPLE_COLOR

    def reset(self):
        """новая игра - новое яблоко"""
        # закрашиваем старое яблоко
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, rect)
        pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, rect, 1)
        self.randomize_position()
        self.draw()

    def randomize_position(self):
        """создаем новое яблоко"""
        # self.position = aaa.__next__()
        self.position = (randint(0, 31) * GRID_SIZE,
                         randint(0, 23) * GRID_SIZE)

    def draw(self):
        """Метод draw класса Apple"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс Snake"""

    def __init__(self):
        """создаем маленькую змейку"""
        self.body_color = SNAKE_COLOR
        self.positions = [(randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                          randint(0, GRID_HEIGHT - 1) * GRID_SIZE)]
        self.last = None
        self.next_head = self.positions[0]
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None

    def calc_next_head(self):
        """Вычисляем, где будет голова змеи"""
        # сейчас в self.next_head текущая голова змеи
        head_pos_x = self.next_head[0] + self.direction[0] * GRID_SIZE
        head_pos_y = self.next_head[1] + self.direction[1] * GRID_SIZE

        if head_pos_x > SCREEN_WIDTH - GRID_SIZE:
            head_pos_x = 0
        elif head_pos_x < 0:
            head_pos_x = SCREEN_WIDTH - GRID_SIZE

        if head_pos_y > SCREEN_HEIGHT - GRID_SIZE:
            head_pos_y = 0
        elif head_pos_y < 0:
            head_pos_y = SCREEN_HEIGHT - GRID_SIZE

        self.next_head = (head_pos_x, head_pos_y)

    def bite_snake(self):
        """А не укусила ли змея себя?"""
        try:
            self.positions.index(self.next_head)
        except ValueError:
            # не укусили себя
            return False
        else:
            print('Bite itself. Game over')

        return True

    def draw(self):
        """Рисуем змею (надо только кончики) тушка неподвижна"""
        rect = (pygame.Rect(self.positions[-1], (GRID_SIZE, GRID_SIZE)))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def reset(self):
        """новая игра - новая змея"""
        # закрашиваем старую змею
        for position in self.positions:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, rect)
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, rect, 1)
        self.__init__()

    def move(self, just_eat):
        """Здесь меняется длина змеи"""
        self.positions.insert(0, self.next_head)

        # удалить хвост
        if just_eat:
            self.last = None
            self.length += 1
        else:
            self.last = self.positions[-1]
            del self.positions[-1]


def handle_keys(game_object):
    """Функция обработки действий пользователя"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """The mainest of main function"""
    # Инициализация PyGame:
    pygame.init()
    snake = Snake()
    apple = Apple()

    apple.draw()
    snake.draw()

    while True:
        handle_keys(snake)
        if snake.next_direction:
            snake.direction = snake.next_direction

        snake.calc_next_head()

        if snake.bite_snake():
            print('******************************************')
            # Restart Game
            apple.reset()
            snake.reset()

        if snake.next_head == apple.position:
            apple.randomize_position()
            apple.draw()
            snake.move(True)
        else:
            snake.move(False)

        snake.draw()
        pygame.display.flip()

        clock.tick(SPEED / 5)


if __name__ == '__main__':
    main()




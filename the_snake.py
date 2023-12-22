
from random import randint

import pygame


pygame.init()

CELL_SIZE = 20

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
GRID_HEIGHT = SCREEN_HEIGHT
GRID_WIDTH = SCREEN_WIDTH
GRID_SIZE = CELL_SIZE
UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'
SCREEN_CENTER = {
    'x': SCREEN_WIDTH / 2 - CELL_SIZE,
    'y': SCREEN_HEIGHT / 2 - CELL_SIZE
}
SNAKE_COLOR = (0, 255, 0)
APPLE_COLOR = (255, 0, 0)
BOARD_BACKGROUND_COLOR = (0, 0, 0)
SPEED = 10


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Змейка')

clock = pygame.time.Clock()


class GameObject:
    """Создаем класс GameObject"""

    def __init__(self, position, body_color):
        self.position = position
        self.body_color = body_color

    @staticmethod
    def random_axis(cell_size):
        """создаём случайные координаты"""
        x = randint(0, cell_size) * cell_size
        y = randint(0, cell_size) * cell_size

        return x, y


class Snake(GameObject):
    """Создаем класс Snake"""

    direction = RIGHT

    def __init__(self, position, body_color):
        super().__init__(position, body_color)
        self.head = self.position[0]

    def update_direction(self):
        """Update"""
        if self.direction == LEFT:
            self.position.insert(0,
                                 (self.position[0][0] - CELL_SIZE,
                                  self.position[0][1]))
        elif self.direction == RIGHT:
            self.position.insert(0,
                                 (self.position[0][0] + CELL_SIZE,
                                  self.position[0][1]))
        elif self.direction == DOWN:
            self.position.insert(0,
                                 (self.position[0][0],
                                  self.position[0][1] + CELL_SIZE))
        elif self.direction == UP:
            self.position.insert(0,
                                 (self.position[0][0],
                                  self.position[0][1] - CELL_SIZE))
        else:
            pass

    def if_out_of_bounds(self):
        """если вне игрового поля"""
        if self.position[0][0] > SCREEN_WIDTH:

            self.position.insert(0, (0, self.position[0][1]))
            self.position.pop(1)

        elif self.position[0][0] < 0:

            self.position.insert(0, (SCREEN_WIDTH, self.position[0][1]))
            self.position.pop(1)

        elif self.position[0][1] > SCREEN_HEIGHT:

            self.position.insert(0, (self.position[0][0], 0))
            self.position.pop(1)

        elif self.position[0][1] < 0:

            self.position.insert(0, (self.position[0][0], SCREEN_HEIGHT))
            self.position.pop(1)

    def move(self):
        """Функция движения змейки"""
        self.update_direction()
        self.if_out_of_bounds()


class Apple(GameObject):
    """Создаем класс Apple"""

    def __init__(self, position, body_color):
        super().__init__(position, body_color)

    def randomize_position(self):
        """Определяем случайное место для яблока"""
        x, y = Snake.random_axis(CELL_SIZE)

        self.position.insert(0, (x, y,
                                 CELL_SIZE, CELL_SIZE))


screen.fill(BOARD_BACKGROUND_COLOR)


def get_head_position(snake):
    """-"""
    return snake.position[0]


def draw(screen, color, axis):
    """Рисуем объекты"""
    pygame.draw.rect(screen, color, pygame.Rect(axis))


def draw_grid():
    """Рисуем сетку"""
    for x in range(0, GRID_WIDTH, GRID_SIZE):

        for y in range(0, GRID_HEIGHT, GRID_SIZE):

            Line = pygame.Rect(x, y, GRID_SIZE, GRID_SIZE)

            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, Line, 1)


def main():
    """Main"""
    snake = Snake([(SCREEN_CENTER['x'], SCREEN_CENTER['y'])], SNAKE_COLOR)

    apple_x, apple_y = GameObject.random_axis(CELL_SIZE)
    apple = Apple([(apple_x, apple_y)], APPLE_COLOR)

    while True:

        clock.tick(SPEED)

        handle_keys(snake)

        snake.move()

        for x_axis, y_axis in snake.position:

            draw(screen, snake.body_color, [x_axis,
                                            y_axis,
                                            CELL_SIZE,
                                            CELL_SIZE])

        one = True if apple.position[0][0] == snake.position[0][0] else False
        two = True if apple.position[0][1] == snake.position[0][1] else False
        apple_is_eaten = True if one and two else False

        if apple_is_eaten is False:

            draw(screen, BOARD_BACKGROUND_COLOR, [snake.position[-1][0],
                                                  snake.position[-1][1],
                                                  CELL_SIZE,
                                                  CELL_SIZE])

            snake.position.pop()
        else:

            apple.randomize_position()

        draw(screen, apple.body_color, [apple.position[0][0],
                                        apple.position[0][1],
                                        CELL_SIZE,
                                        CELL_SIZE])

        if snake.position.count(snake.position[0]) > 1:

            reset(snake)

        draw_grid()

        pygame.display.update()


def reset(snake):
    """ресет"""
    snake.position.insert(-1,
                          (SCREEN_CENTER['x'],
                           SCREEN_CENTER['y']))

    for x, y in snake.position:

        draw(screen, BOARD_BACKGROUND_COLOR, [x, y, CELL_SIZE, CELL_SIZE])

    del snake.position[:-1]


def handle_keys(object):
    """Нажатия кнопок"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and object.direction != DOWN:
                object.direction = UP
            elif event.key == pygame.K_DOWN and object.direction != UP:
                object.direction = DOWN
            elif event.key == pygame.K_LEFT and object.direction != RIGHT:
                object.direction = LEFT
            elif event.key == pygame.K_RIGHT and object.direction != LEFT:
                object.direction = RIGHT
            else:
                pass


main()

if __name__ == '__main__':
    main()

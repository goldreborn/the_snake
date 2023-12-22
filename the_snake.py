
from random import randint

import pygame


pygame.init()

GRID_SIZE = 20

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
GRID_HEIGHT = SCREEN_HEIGHT
GRID_WIDTH = SCREEN_WIDTH
UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'
SCREEN_CENTER = {
    'x': SCREEN_WIDTH / 2 - GRID_SIZE,
    'y': SCREEN_HEIGHT / 2 - GRID_SIZE
}
SNAKE_COLOR = (0, 255, 0)
APPLE_COLOR = (255, 0, 0)
BOARD_BACKGROUND_COLOR = (0, 0, 0)
SPEED = 10


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen.fill(BOARD_BACKGROUND_COLOR)
pygame.display.set_caption('Змейка')

clock = pygame.time.Clock()


class GameObject:
    """Создаем класс GameObject"""

    def __init__(self: object, positions=None, body_color=None) -> None:
        self.positions = positions
        self.position = None
        self.body_color = body_color

    @staticmethod
    def random_axis(grid_size: int):
        """создаём случайные координаты"""
        x = randint(0, grid_size) * grid_size
        y = randint(0, grid_size) * grid_size

        return x, y
    
    @staticmethod
    def draw(screen: pygame.display, color: tuple, axis: list) -> None:
        """Рисуем объекты"""
        pygame.draw.rect(screen, color, pygame.Rect(axis))

class Snake(GameObject):
    """Создаем класс Snake"""

    direction = RIGHT

    def __init__(self, positions=None, body_color=SNAKE_COLOR):
        super().__init__(positions, body_color)
        self.positions = positions
        self.position = None
        self.length = None
        self.body_color = body_color

    def get_head_position(self):
        """-"""
        pass

    def update_direction(self) -> None:
        """Update"""
        if self.direction == LEFT:
            self.positions.insert(0,
                                  (self.positions[0][0] - GRID_SIZE,
                                   self.positions[0][1]))
        elif self.direction == RIGHT:
            self.positions.insert(0,
                                  (self.positions[0][0] + GRID_SIZE,
                                   self.positions[0][1]))
        elif self.direction == DOWN:
            self.positions.insert(0,
                                  (self.positions[0][0],
                                   self.positions[0][1] + GRID_SIZE))
        elif self.direction == UP:
            self.positions.insert(0,
                                  (self.positions[0][0],
                                   self.positions[0][1] - GRID_SIZE))
        else:
            pass

    def if_out_of_bounds(self) -> None:
        """если вне игрового поля"""
        if self.positions[0][0] > SCREEN_WIDTH:

            self.positions.insert(0, (0, self.positions[0][1]))
            self.positions.pop(1)

        elif self.positions[0][0] < 0:

            self.positions.insert(0, (SCREEN_WIDTH, self.positions[0][1]))
            self.positions.pop(1)

        elif self.positions[0][1] > SCREEN_HEIGHT:

            self.positions.insert(0, (self.positions[0][0], 0))
            self.positions.pop(1)

        elif self.positions[0][1] < 0:

            self.positions.insert(0, (self.positions[0][0], SCREEN_HEIGHT))
            self.positions.pop(1)

    def reset(self) -> None:
        """ресет"""
        self.positions.insert(-1,
                              (SCREEN_CENTER['x'],
                               SCREEN_CENTER['y']))

        for x, y in self.positions:

            GameObject.draw(screen, BOARD_BACKGROUND_COLOR,
                            [x, y, GRID_SIZE, GRID_SIZE])

        del self.positions[:-1]

    def move(self) -> None:
        """Функция движения змейки"""
        self.update_direction()
        self.if_out_of_bounds()


class Apple(GameObject):
    """Создаем класс Apple"""

    def __init__(self, positions=None, body_color=APPLE_COLOR):
        super().__init__(positions, body_color)
        self.positions = positions
        self.position = None
        self.body_color = body_color

    def randomize_position(self) -> None:
        """Определяем случайное место для яблока"""
        x, y = Snake.random_axis(GRID_SIZE)

        self.positions.insert(0,
                              (x, y,
                               GRID_SIZE, GRID_SIZE))


def draw_grid() -> None:
    """Рисуем сетку"""
    for x in range(0, GRID_WIDTH, GRID_SIZE):

        for y in range(0, GRID_HEIGHT, GRID_SIZE):

            Line = pygame.Rect(x, y, GRID_SIZE, GRID_SIZE)

            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, Line, 1)


def main() -> None:
    """Main"""
    snake = Snake([(SCREEN_CENTER['x'], SCREEN_CENTER['y'])], SNAKE_COLOR)

    apple_x, apple_y = GameObject.random_axis(GRID_SIZE)
    apple = Apple([(apple_x, apple_y)], APPLE_COLOR)

    while True:

        clock.tick(SPEED)

        handle_keys(snake)

        snake.move()

        for x_axis, y_axis in snake.positions:

            Snake.draw(screen, snake.body_color, [x_axis,
                                                  y_axis,
                                                  GRID_SIZE,
                                                  GRID_SIZE])

        one = True if apple.positions[0][0] == snake.positions[0][0] else False
        two = True if apple.positions[0][1] == snake.positions[0][1] else False
        apple_is_eaten = True if one and two else False

        if apple_is_eaten is False:

            GameObject.draw(screen, BOARD_BACKGROUND_COLOR,
                            [snake.positions[-1][0],
                             snake.positions[-1][1],
                             GRID_SIZE,
                             GRID_SIZE])

            snake.positions.pop()
        else:

            apple.randomize_position()

        Apple.draw(screen, apple.body_color, [apple.positions[0][0],
                                              apple.positions[0][1],
                                              GRID_SIZE,
                                              GRID_SIZE])

        if snake.positions.count(snake.positions[0]) > 1:

            snake.reset()

        draw_grid()

        pygame.display.update()


def handle_keys(object: Snake) -> None:
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


if __name__ == '__main__':
    main()

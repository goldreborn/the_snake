from random import randint

import pygame as pg


pg.init()

GRID_SIZE = 20

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
GRID_HEIGHT = SCREEN_HEIGHT
GRID_WIDTH = SCREEN_WIDTH
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
SCREEN_CENTER = ((
    SCREEN_WIDTH / 2 - GRID_SIZE,
    SCREEN_HEIGHT / 2 - GRID_SIZE
))
SNAKE_COLOR = (0, 255, 0)
APPLE_COLOR = (255, 0, 0)
BOARD_BACKGROUND_COLOR = (0, 0, 0)
SPEED = 10


screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen.fill(BOARD_BACKGROUND_COLOR)
pg.display.set_caption('Змейка')

clock = pg.time.Clock()


class GameObject:
    """Создаем класс GameObject"""

    def __init__(self, position=None, body_color=None) -> None:
        self.position = position
        self.body_color = body_color

    def draw(self):
        pass


class Grid(GameObject):
    """Класс Сетки"""

    def __init__(self, color: tuple) -> None:
        self.color = color

    def draw(self):
        """Рисуем Сетку"""
        for x in range(0, GRID_WIDTH, GRID_SIZE):

            for y in range(0, GRID_HEIGHT, GRID_SIZE):

                Line = pg.Rect(x, y, GRID_SIZE, GRID_SIZE)

                pg.draw.rect(screen, self.color, Line, 1)


class Snake(GameObject):
    """Создаем класс Snake"""

    direction = RIGHT

    def __init__(self, position=None, body_color=SNAKE_COLOR):
        super().__init__(position, body_color)
        self.positions = [position]
        self.position = position
        self.length = 1
        self.body_color = body_color
        self.next_direction = RIGHT
        self.tail = position

    def get_head_position(self) -> tuple:
        """Получаем и возвращаем кортеж с
        координатами головы змейки
        """
        return self.positions[0]

    def reset(self) -> None:
        """Сбрасываем настройки змейки в начальное состояние"""
        self.positions = [SCREEN_CENTER]
        self.length = 1

    def hide_tail(self):
        """Зарисовываем хвост змейки"""
        pg.draw.rect(screen, BOARD_BACKGROUND_COLOR,
                     [self.tail[0], self.tail[1],
                      GRID_SIZE, GRID_SIZE])

    def draw(self):
        """Отрисовываем змейку"""
        for x_axis, y_axis in self.positions:

            pg.draw.rect(screen, self.body_color, [x_axis,
                                                   y_axis,
                                                   GRID_SIZE,
                                                   GRID_SIZE])

    def update_direction(self):
        """Обновляем направление движения змейки"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self) -> None:
        """Функция движения змейки.
        Получаем координаты головы и обновляем.
        Хвост подтираем
        """
        head = self.get_head_position()

        self.tail = self.positions[-1]

        def in_bounds(pointer, edge, path):
            """Проверяем если голова вне поля"""
            if path == 'd' or path == 'r':
                if pointer / edge < 1:
                    return pointer + GRID_SIZE
                else:
                    return 0
            else:
                if pointer / edge > 0:
                    return pointer - GRID_SIZE
                else:
                    return SCREEN_WIDTH if path == 'l' else SCREEN_HEIGHT

        if self.direction == LEFT:
            self.positions.insert(0,
                                  (in_bounds(head[0], SCREEN_WIDTH, 'l'),
                                   head[1]))
        elif self.direction == RIGHT:
            self.positions.insert(0,
                                  (in_bounds(head[0], SCREEN_WIDTH, 'r'),
                                   head[1]))
        elif self.direction == DOWN:
            self.positions.insert(0,
                                  (head[0],
                                   in_bounds(head[1], SCREEN_HEIGHT, 'd')))
        elif self.direction == UP:
            self.positions.insert(0,
                                  (head[0],
                                   in_bounds(head[1], SCREEN_HEIGHT, 'u')))
        else:
            pass

        self.update_direction()


class Apple(GameObject):
    """Создаем класс Apple"""

    def __init__(self, position=None, body_color=APPLE_COLOR):
        super().__init__(position, body_color)
        self.position = position
        self.body_color = body_color

    def randomize_position(self) -> None:
        """Определяем случайное место для яблока"""
        x = randint(0, GRID_SIZE) * GRID_SIZE
        y = randint(0, GRID_SIZE) * GRID_SIZE

        self.position = (x, y)

    def draw(self):
        """Функци отрисовки яблока"""
        pg.draw.rect(screen, self.body_color,
                     [self.position[0],
                      self.position[1],
                      GRID_SIZE,
                      GRID_SIZE])


def main() -> None:
    """Main"""
    snake = Snake(SCREEN_CENTER, SNAKE_COLOR)

    apple = Apple([], APPLE_COLOR)
    apple.randomize_position()

    while True:

        clock.tick(SPEED)

        handle_keys(snake)

        snake.update_direction()
        snake.move()
        snake.draw()

        head = snake.get_head_position()

        if apple.position == head:
            apple.randomize_position()
        else:
            snake.hide_tail()
            snake.positions.pop()

            apple.draw()

        if snake.positions.count(snake.positions[0]) > 1:

            screen.fill(BOARD_BACKGROUND_COLOR)

            snake.reset()

        grid = Grid(BOARD_BACKGROUND_COLOR)
        grid.draw()

        pg.display.update()


def handle_keys(object: Snake) -> None:
    """Нажатия кнопок"""
    for event in pg.event.get():
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and object.direction != DOWN:
                object.direction = UP
            elif event.key == pg.K_DOWN and object.direction != UP:
                object.direction = DOWN
            elif event.key == pg.K_LEFT and object.direction != RIGHT:
                object.direction = LEFT
            elif event.key == pg.K_RIGHT and object.direction != LEFT:
                object.direction = RIGHT
            elif event.key == pg.K_ESCAPE:
                pg.quit()
            else:
                pass
        elif event.type == pg.QUIT:
            pg.quit()


if __name__ == '__main__':
    main()

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
SCREEN_CENTER = (
    SCREEN_WIDTH / 2 - GRID_SIZE,
    SCREEN_HEIGHT / 2 - GRID_SIZE
)
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

    @classmethod
    def draw(cls, board, color, axis):
        """Рисуем по координатам"""
        if hasattr(GameObject, 'draw'):
            pg.draw.rect(board, color, axis)
        else:
            raise NotImplementedError


class Snake(GameObject):
    """Создаем класс Snake"""

    def __init__(self, position=None, body_color=SNAKE_COLOR):
        super().__init__(position, body_color)
        self.reset()
        self.next_direction = RIGHT

    def get_head_position(self):
        """Получаем и возвращаем кортеж с
        координатами головы змейки
        """
        return self.positions[0]

    def reset(self) -> None:
        """Сбрасываем настройки змейки в начальное состояние"""
        self.positions = [SCREEN_CENTER]
        self.length = 1
        self.direction = RIGHT

    def hide_tail(self):
        """Прячем хвост"""
        tail = self.positions[-1]

        GameObject.draw(screen, BOARD_BACKGROUND_COLOR,
                        [tail[0], tail[1],
                         GRID_SIZE, GRID_SIZE])

        self.positions.pop()

    def draw(self):
        """Отрисовываем змейку"""
        head = self.get_head_position()

        for x, y in self.positions:
            Line = pg.Rect(x, y, GRID_SIZE, GRID_SIZE)

            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, Line, 1)

        GameObject.draw(screen, self.body_color,
                        [head[0],
                         head[1],
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

        x, y = self.direction

        new_x_axis = (head[0] + x * GRID_SIZE) % SCREEN_WIDTH
        new_y_axis = (head[1] + y * GRID_SIZE) % SCREEN_HEIGHT

        if self.direction == LEFT or self.direction == RIGHT:

            self.positions.insert(0, (new_x_axis, head[1]))
        elif self.direction == DOWN or self.direction == UP:

            self.positions.insert(0, (head[0], new_y_axis))


class Apple(GameObject):
    """Создаем класс Apple"""

    def __init__(self, position=None, body_color=APPLE_COLOR):
        super().__init__(position, body_color)
        self.randomize_position()

    def randomize_position(self) -> None:
        """Определяем случайное место для яблока"""
        self.position = (randint(0, GRID_SIZE) * GRID_SIZE,
                         randint(0, GRID_SIZE) * GRID_SIZE)

    def draw(self):
        """Функция отрисовки яблока"""
        GameObject.draw(screen,
                        self.body_color,
                        [self.position[0], self.position[1],
                         GRID_SIZE,
                         GRID_SIZE])


def main() -> None:
    """Main"""
    snake = Snake()
    apple = Apple()

    while True:

        clock.tick(SPEED)

        handle_keys(snake)

        head = snake.get_head_position()

        snake.move()

        if snake.positions.count(head) > 1:

            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)

        if head == apple.position:

            apple.randomize_position()
            snake.length += 1
        else:
            snake.hide_tail()
            apple.draw()

        snake.draw()
        snake.update_direction()

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

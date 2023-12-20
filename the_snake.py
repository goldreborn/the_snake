
from random import randint

import pygame


pygame.init()

CELL_SIZE = 20

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
GRID_HEIGHT = 0
GRID_WIDTH = 0
GRID_SIZE = 0
UP = 0
DOWN = 0
LEFT = 0
RIGHT = 0

screen_CENTER = {
    'x': SCREEN_WIDTH / 2 - CELL_SIZE,
    'y': SCREEN_HEIGHT / 2 - CELL_SIZE
}
SNAKE_COLOR = (0, 255, 0)
APPLE_COLOR = (255, 0, 0)
BOARD_BACKGROUND_COLOR = (0, 0, 0)
SPEED = 25


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

    direction = 'right'

    def __init__(self, position, body_color):
        super().__init__(position, body_color)

    def move(self):
        """Функция движения змейки"""
        global direction

        if self.direction == 'left':

            self.position.insert(0,
                                 (self.position[0][0] - CELL_SIZE,
                                  self.position[0][1]))
        elif self.direction == 'right':
            self.position.insert(0,
                                 (self.position[0][0] + CELL_SIZE,
                                  self.position[0][1]))
        elif self.direction == 'down':
            self.position.insert(0,
                                 (self.position[0][0],
                                  self.position[0][1] + CELL_SIZE))
        elif self.direction == 'up':
            self.position.insert(0,
                                 (self.position[0][0],
                                  self.position[0][1] - CELL_SIZE))
        else:
            pass

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

def update_direction():
    pass

def get_head_position():
    pass

def draw(screen, color, axis):
    """Рисуем объекты"""
    pygame.draw.rect(screen, color, pygame.Rect(axis))

def draw_grid():
    """Рисуем сетку"""
    for x in range(0, SCREEN_WIDTH, CELL_SIZE):

        for y in range(0, SCREEN_HEIGHT, CELL_SIZE):

            Line = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)

            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, Line, 1)

def main():
    """Main"""
    snake = Snake([(screen_CENTER['x'], screen_CENTER['y'])], SNAKE_COLOR)

    apple_x, apple_y = GameObject.random_axis(CELL_SIZE)
    apple = Apple([(apple_x, apple_y)], APPLE_COLOR)
    
    while True:

        clock.tick(SPEED)

        handle_keys(snake)

        snake.move()

        for x_axis, y_axis in snake.position:

            draw(screen, snake. body_color, [x_axis,
                                            y_axis,
                                            CELL_SIZE,
                                            CELL_SIZE])

        one = True if apple.position[0][0] == snake.position[0][0] else False
        two = True if apple.position[0][1] == snake.position[0][1] else False
        apple_is_eaten = True if one and two else False

        if apple_is_eaten is not True:
            draw(screen, BOARD_BACKGROUND_COLOR, [snake.position[-1][0],
                                   snake.position[-1][1],
                                   CELL_SIZE,
                                   CELL_SIZE])

            snake.position.pop()

        if apple_is_eaten:
            apple.randomize_position()

        draw(screen, apple. body_color, [apple.position[0][0],
                                        apple.position[0][1],
                                        CELL_SIZE,
                                        CELL_SIZE])

        if snake.position.count(snake.position[0]) > 1:

            reset(snake)
        
        draw_grid()

        pygame.display.update()

def reset(snake):
    """ресет"""
    snake.position.insert(-1, (screen_CENTER['x'],
                                screen_CENTER['y']))

    for x, y in snake.position:

        draw(screen, BOARD_BACKGROUND_COLOR, [x, y, CELL_SIZE, CELL_SIZE])
    
    del snake.position[1:]

def handle_keys(object):
    """Нажатия кнопок"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and object.direction != 'down':
                object.direction = 'up'
            elif event.key == pygame.K_DOWN and object.direction != 'up':
                object.direction = 'down'
            elif event.key == pygame.K_LEFT and object.direction != 'right':
                object.direction = 'left'
            elif event.key == pygame.K_RIGHT and object.direction != 'left':
                object.direction = 'right'
            else:
                pass


main()

if __name__ == '__main__':
    main()

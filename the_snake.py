
from random import randint, choice

import pygame


pygame.init()

CELL_SIZE = 20

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
FIELD_CENTER = {
    'x': SCREEN_WIDTH / 2 - CELL_SIZE,
    'y': SCREEN_HEIGHT / 2 - CELL_SIZE
}
SNAKE_COLOR = (0, 255, 0)
APPLE_COLOR = (255, 0, 0)
BG_COLOR = (0, 0, 0)
SPEED = 10

field = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Змейка')

clock = pygame.time.Clock()

# Создаем класс GameObject


class GameObject:

    def __init__(self, position, body_color):
        self.position = position
        self.body_color = body_color

    # создаём случайные координаты

    @staticmethod
    def random_axis(cell_size):

        x = randint(0, cell_size) * cell_size
        y = randint(0, cell_size) * cell_size

        return x, y


# Создаем класс Snake


class Snake(GameObject):

    direction = 'right'

    def __init__(self, position, body_color):
        super().__init__(position, body_color)

    # Функция движения змейки

    def move(self):

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
        elif self.position[0][0] < 0:
            self.position.insert(0, (SCREEN_WIDTH, self.position[0][1]))
        elif self.position[0][1] > SCREEN_HEIGHT:
            self.position.insert(0, (self.position[0][0], 0))
        elif self.position[0][1] < 0:
            self.position.insert(0, (self.position[0][0], SCREEN_HEIGHT))


# Создаем класс Apple


class Apple(GameObject):

    def __init__(self, position, body_color):
        super().__init__(position, body_color)

    # Определяем случайное место для яблока

    def randomize_position(self):

        x, y = Snake.random_axis(CELL_SIZE)

        self.position.insert(0, (x, y,
                                 CELL_SIZE, CELL_SIZE))

        print('apple has been eaten')


field.fill(BG_COLOR)



def draw(field, color, axis):
    pygame.draw.rect(field, color, pygame.Rect(axis))


def main():

    snake = Snake([(FIELD_CENTER['x'], FIELD_CENTER['y'])], SNAKE_COLOR)

    apple_x, apple_y = GameObject.random_axis(CELL_SIZE)
    apple = Apple([(apple_x, apple_y)], APPLE_COLOR)

    while True:

        clock.tick(SPEED)

        handle_keys(snake)

        snake.move()

        for x_axis, y_axis in snake.position:

            draw(field, snake. body_color, [x_axis,
                                            y_axis,
                                            CELL_SIZE,
                                            CELL_SIZE])

        one = True if apple.position[0][0] == snake.position[0][0] else False
        two = True if apple.position[0][1] == snake.position[0][1] else False
        apple_is_eaten = True if one and two else False

        if apple_is_eaten is not True:
            draw(field, BG_COLOR, [snake.position[-1][0],
                                   snake.position[-1][1],
                                   CELL_SIZE,
                                   CELL_SIZE])

            snake.position.pop()

        if apple_is_eaten:
            apple.randomize_position()

        draw(field, apple. body_color, [apple.position[0][0],
                                        apple.position[0][1],
                                        CELL_SIZE,
                                        CELL_SIZE])

        if snake.position.count(snake.position[0]) > 1:

            snake.position.insert(-1, (FIELD_CENTER['x'],
                                       FIELD_CENTER['y']))

            for x, y in snake.position:

                draw(field, BG_COLOR, [x, y, CELL_SIZE, CELL_SIZE])

            del snake.position[1:]

        print(snake.position)
        pygame.display.update()


def handle_keys(game_object):
    for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and game_object.direction != 'down':
                    game_object.direction = 'up'
                elif event.key == pygame.K_DOWN and game_object.direction != 'up':
                    game_object.direction = 'down'
                elif event.key == pygame.K_LEFT and game_object.direction != 'right':
                    game_object.direction = 'left'
                elif event.key == pygame.K_RIGHT and game_object.direction != 'left':
                    game_object.direction = 'right'
                else:
                    pass


main()

if __name__ == '__main__':
    main()

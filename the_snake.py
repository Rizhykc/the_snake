from random import randint

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


# Тут опишите все классы игры.
class GameObject:
    """Родительский класс"""

    # Инициализация позиции и цвета.
    def __init__(self):
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = None

    # Отрисовка объектов на экране по умол. pass.
    def draw(self):
        pass


class Apple(GameObject):
    """Дочерний класс отвечающий за создание и прорисовки яблока."""

    def __init__(self):
        super().__init__() 
        self.randomize_position()
        self.body_color = APPLE_COLOR

    # Рандомноые позиции яблочка.
    def randomize_position(self):
        self.position = (randint(0, GRID_WIDTH) * GRID_SIZE,
                         randint(0, GRID_HEIGHT) * GRID_SIZE)
        
    # Отрисовка яблочка.
    def draw(self):
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)
    
        
class Snake(GameObject):
    """Дочерний класс отвечающий за создание, прорисовку, движение змейки."""

    def __init__(self) -> None:
        super().__init__()
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = SNAKE_COLOR
        self.positions = [(self.position[0], self.position[0])]
        self.last = None    

    # Возвращает позицию головы змейки.
    def get_head_position(self):
        return self.positions[0]
    
    # Метод обновления направления после нажатия на кнопку
    def update_direction(self):
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        self.update_direction()
        head = self.get_head_position()
        x, y = self.direction
        new_head = (
            (head[0] + x * GRID_SIZE) % SCREEN_WIDTH,
            (head[1] + y * GRID_SIZE) % SCREEN_HEIGHT
        )
        if new_head in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0, new_head)
            if len(self.positions) > self.length:
                self.last = self.positions.pop()

    def draw(self):
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
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
        self.length = 1
        self.positions = [(self.position[0], self.position[0])]
        

def handle_keys(game_object):
    """Функционал движения змейки."""
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
    """Главнаый цикл игры 'Змейка'."""
    # Инициализация PyGame:
    pygame.init()
    apple = Apple()
    snake = Snake()
    # Тут нужно создать экземпляры классов.
    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.move()
        snake.draw()  # Рисуем змейку
        apple.draw()  # Рисуем яблоко
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()
        pygame.display.update()

    pygame.quit()


if __name__ == '__main__': 
    main()  
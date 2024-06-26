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
SPEED = 10
# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Родительский класс."""

    # Инициализация позиции и цвета.
    def __init__(self, position=None, body_color=None) -> None:
        self.position = (position if position is not None
                         else ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2)))
        self.body_color = body_color

    def draw(self):
        """Отрисовка объектов на экране"""
        raise NotImplementedError

    def _draw_rect(self):
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Дочерний класс отвечающий за создание и прорисовки яблока."""

    def __init__(self, occupated_positions=None) -> None:
        super().__init__(body_color=APPLE_COLOR)
        self.occupated_positions = occupated_positions
        if occupated_positions is None:
            occupated_positions = []
        self.randomize_position(occupated_positions)

    def randomize_position(self, occupated_positions):
        """Рандомноые позиции яблочка"""
        while True:
            position = (randint(0, GRID_WIDTH) * GRID_SIZE,
                        randint(0, GRID_HEIGHT) * GRID_SIZE)
            if position not in occupated_positions:
                self.position = position
                return

    def draw(self):
        """Отрисовка яблочка."""
        self._draw_rect()


class Snake(GameObject):
    """Дочерний класс отвечающий за создание, прорисовку, движение змейки."""

    def __init__(self) -> None:
        super().__init__(position=None, body_color=SNAKE_COLOR)
        self.reset()
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def get_head_position(self):
        """Возвращает позицию головы змейки"""
        return self.positions[0]

    def update_direction(self):
        """Метод обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """
        Обновляет позицию змейки (координаты каждой секции),
        добавляя новую голову в начало списка positions
        и удаляя последний элемент,
        если длина змейки не увеличилась.
        """
        self.update_direction()
        head = self.get_head_position()
        x, y = self.direction
        new_head = (
            (head[0] + x * GRID_SIZE) % SCREEN_WIDTH,
            (head[1] + y * GRID_SIZE) % SCREEN_HEIGHT
        )
        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.last = self.positions.pop()

    def draw(self):
        """Отрисовка змейки."""
        # Отрисовка головы змейки
        self.position = self.positions[0]
        self._draw_rect()

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def reset(self):
        """Сбрасывает змейку в начальное состояние после столкновения."""
        self.length = 1
        self.positions = [self.position]
        screen.fill(BOARD_BACKGROUND_COLOR)  # Очищаем экран


def handle_keys(game_object):
    """
    Обрабатывает нажатия клавиш,
    чтобы изменить направление движения змейки.
    """
    direction_list = {
        (pygame.K_UP, DOWN): UP,
        (pygame.K_DOWN, UP): DOWN,
        (pygame.K_LEFT, RIGHT): LEFT,
        (pygame.K_RIGHT, LEFT): RIGHT,
    }
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            for keys, value in direction_list.items():
                if event.key == keys[0] and game_object.direction != keys[1]:
                    game_object.next_direction = value


def main():
    """Главнаый цикл игры 'Змейка'."""
    # Инициализация PyGame:
    pygame.init()
    snake = Snake()
    apple = Apple(snake.position)
    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.move()
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple = Apple(snake.positions)
        if len(snake.positions) > 2:
            if snake.get_head_position() in snake.positions[2:]:
                snake.reset()
                apple = Apple(snake.positions)

        snake.draw()
        apple.draw()

        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    main()

# the_snake

1.1
changes:
    added method "_draw_rect" - drawing each square
    The randomize method has been changed - now the method generates apples correctly
    The control func. has been changed - removed the extra "if/elif"
    redesigned the 'main' and removed the method of adding apples n-pieces

изменения:
    добавлен метод "_draw_rect" - рисует каждый квадрата
    Изменен метод рандом - теперь метод генерирует яблоки корректно
    Изменена функция управления - удалены лишние "if/elif"
    переработан "main" и убран способ добавления яблок n-штук

1.2 (after 1 review)
changes:
    removed checking of positions in objects - transferring them to main
    the drawing of the snake has been corrected - the position of the head
    the update_direction method - corrected
    recycling handle_keys - the dictionary has been changed and iteration on it has been removed. Using the dictionary as your own tool

изменения:
    убрана проверка позиций в объектах - перенос их в main
    поправлена прорисовка змейки - позиция головы
    поправлен update_direction метод
    переработан handle_keys - изменен словарь, убрана итерация по нему. Использования словаря как собственный инструмент
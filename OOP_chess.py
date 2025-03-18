class Figure:
    """
    Базовый класс для шахматных и шашечных фигур.

    Атрибуты:
    color : str
        Цвет фигуры ('white' или 'black').
    position : tuple[int, int]
        Текущее положение фигуры на доске в формате (x, y).
    kill : bool, по умолчанию False
        Флаг, указывающий, может ли фигура продолжать атаку (актуально для шашек).

    Методы:
    get_possible_moves():
        Абстрактный метод, который должен быть переопределен в дочерних классах.
        Должен возвращать список возможных ходов для конкретной фигуры.
    """
    def __init__(self, color, position, kill = False):
        """
        Инициализация фигуры.

        Параметры:
        color : str
            Цвет фигуры ('white' или 'black').
        position : tuple[int, int]
            Начальное положение фигуры на доске.
        kill : bool, по умолчанию False
            Флаг для обозначения возможности продолжения атаки (актуально для шашек).
        """
        self.color = color
        self.position = position
        self.kill = kill

    def get_possible_moves(self):
        """
        Абстрактный метод, который должен быть реализован в дочерних классах.

        Вызывает исключение, если не переопределён.
        """
        raise NotImplementedError("Метод должен быть переопределен в дочернем классе")

class CheckersFigure(Figure):
    """
    Класс CheckersFigure представляет фигуру для игры в шашки.
    Наследуется от класса Figure и реализует специфические для шашек методы.

    Атрибуты:
        color (str): Цвет фигуры ('white' или 'black').
        position (tuple): Координаты фигуры на доске в формате (x, y).
        kill (bool): Флаг, указывающий, может ли фигура бить другие фигуры.

    Методы:
        __str__(): Возвращает строковое представление фигуры ('O' для белых, 'o' для черных).
        get_possible_moves(): Определяет список возможных ходов фигуры.
    """
    def __str__(self):
        """Возвращает строковое представление фигуры."""
        return 'O' if self.color == 'white' else 'o'

    def get_possible_moves(self):
        """
        Определяет список возможных ходов для шашки в зависимости от ее цвета.

        Белые шашки могут ходить по диагонали вверх.
        Черные шашки могут ходить по диагонали вниз.

        Возвращает:
            list[tuple]: Список возможных координат для хода.
        """
        possible_moves = []
        x, y = self.position
        if self.color == 'white':
            possible_moves.append((x - 1, y + 1))
            possible_moves.append((x - 1, y - 1))
        else:
            possible_moves.append((x + 1, y + 1))
            possible_moves.append((x + 1, y - 1))
        return possible_moves

class Ghost(Figure):
    """
    Класс Ghost представляет специальную шахматную фигуру "Призрак".
    Наследуется от класса Figure и имеет уникальный способ передвижения.

    Атрибуты:
        color (str): Цвет фигуры ('white' или 'black').
        position (tuple): Координаты фигуры на доске в формате (x, y).
        kill (bool): Флаг, указывающий, может ли фигура бить другие фигуры.

    Методы:
        __str__(): Возвращает строковое представление фигуры ('G' для белых, 'g' для черных).
        get_possible_moves(): Определяет список возможных ходов фигуры, двигаясь по горизонтали и вертикали.
    """
    def __str__(self):
        """Возвращает строковое представление фигуры."""
        return 'G' if self.color == 'white' else 'g'

    def get_possible_moves(self):
        """
        Определяет список возможных ходов для фигуры "Призрак".
        Фигура может двигаться на любое количество клеток по вертикали и горизонтали.

        Возвращает:
            list[tuple]: Список возможных координат для хода.
        """
        x, y = self.position
        moves = []
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            for i in range(1, 8):
                nx, ny = x + dx * i, y + dy * i
                if 0 <= nx < 8 and 0 <= ny < 8:
                    moves.append((nx, ny))
                else:
                    break
        return moves

class Pawn(Figure):
    """
    Класс Pawn представляет шахматную фигуру "Пешка".
    Наследуется от класса Figure и реализует правила передвижения пешки.

    Атрибуты:
        color (str): Цвет фигуры ('white' или 'black').
        position (tuple): Координаты фигуры на доске в формате (x, y).
        kill (bool): Флаг, указывающий, может ли фигура бить другие фигуры.

    Методы:
        __str__(): Возвращает строковое представление фигуры ('P' для белых, 'p' для черных).
        get_possible_moves(): Определяет список возможных ходов фигуры в зависимости от ее цвета.
    """
    def __str__(self):
        """Возвращает строковое представление фигуры."""
        return 'P' if self.color == 'white' else 'p'

    def get_possible_moves(self):
        """
        Определяет список возможных ходов для пешки.
        Пешка движется на одну клетку вперед, а если стоит на стартовой позиции, может пойти на две клетки.

        Возвращает:
            list[tuple]: Список возможных координат для хода.
        """
        possible_moves = []
        x, y = self.position
        possible_moves.append((x - 1, y)) if self.color == 'white' else possible_moves.append((x + 1, y))
        if x == 6 and self.color == 'white':
            possible_moves.append((x - 2, y))
        elif x == 1 and self.color == 'black':
            possible_moves.append((x + 2, y))
        for move in possible_moves:
            if move[0] < 0 or move[0] >= 8 or move[1] < 0 or move[1] >= 8:
                possible_moves.remove(move)
        return possible_moves

class Rook(Figure):
    """
    Класс Rook представляет шахматную фигуру "Ладья".
    Наследуется от класса Figure и реализует правила передвижения ладьи.

    Атрибуты:
        color (str): Цвет фигуры ('white' или 'black').
        position (tuple): Координаты фигуры на доске в формате (x, y).
        kill (bool): Флаг, указывающий, может ли фигура бить другие фигуры.

    Методы:
        __str__(): Возвращает строковое представление фигуры ('R' для белых, 'r' для черных).
        get_possible_moves(): Определяет список возможных ходов фигуры в зависимости от ее текущей позиции.
    """
    def __str__(self):
        """Возвращает строковое представление фигуры."""
        return 'R' if self.color == 'white' else 'r'

    def get_possible_moves(self):
        """
        Определяет список возможных ходов для ладьи.
        Ладья ходит по вертикали и горизонтали без ограничений по расстоянию, пока не встретит препятствие.

        Возвращает:
            list[tuple]: Список возможных координат для хода.
        """
        possible_moves = []
        x, y = self.position
        for i in range(8):
            if i != x:
                possible_moves.append((i, y))
            if i != y:
                possible_moves.append((x, i))

        return possible_moves

class Knight(Figure):
    """
    Класс Knight представляет шахматную фигуру "Конь".
    Наследуется от класса Figure и реализует правила передвижения коня.

    Атрибуты:
        color (str): Цвет фигуры ('white' или 'black').
        position (tuple): Координаты фигуры на доске в формате (x, y).
        kill (bool): Флаг, указывающий, может ли фигура бить другие фигуры.

    Методы:
        __str__(): Возвращает строковое представление фигуры ('N' для белых, 'n' для черных).
        get_possible_moves(): Определяет список возможных ходов фигуры в зависимости от ее текущей позиции.
    """
    def __str__(self):
        """Возвращает строковое представление фигуры."""
        return 'N' if self.color == 'white' else 'n'

    def get_possible_moves(self):
        """
        Определяет список возможных ходов для коня.
        Конь ходит буквой "Г": два поля в одном направлении и одно в перпендикулярном.

        Возвращает:
            list[tuple]: Список возможных координат для хода.
        """
        possible_moves = []
        x, y = self.position
        possible_moves = possible_moves + [(x + 1, y + 2), (x + 2, y + 1), (x + 1, y - 2), (x + 2, y - 1), (x - 1, y + 2),
                          (x - 2, y + 1), (x - 2, y - 1), ( x - 1, y - 2)]
        return possible_moves

class Bishop(Figure):
    """
    Класс Bishop представляет шахматную фигуру "Слон".
    Наследуется от класса Figure и реализует правила передвижения слона.

    Атрибуты:
        color (str): Цвет фигуры ('white' или 'black').
        position (tuple): Координаты фигуры на доске в формате (x, y).
        kill (bool): Флаг, указывающий, может ли фигура бить другие фигуры.

    Методы:
        __str__(): Возвращает строковое представление фигуры ('B' для белых, 'b' для черных).
        get_possible_moves(): Определяет список возможных ходов фигуры в зависимости от ее текущей позиции.
    """
    def __str__(self):
        """Возвращает строковое представление фигуры."""
        return 'B' if self.color == 'white' else 'b'

    def get_possible_moves(self):
        """
        Определяет список возможных ходов для слона.
        Слон ходит по диагоналям на любое количество клеток.

        Возвращает:
            list[tuple]: Список возможных координат для хода.
        """
        possible_moves = []
        x, y = self.position
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dx, dy in directions:
            step = 1
            while True:
                new_x, new_y = x + dx * step, y + dy * step
                if 0 <= new_x < 8 and 0 <= new_y < 8:
                    possible_moves.append((new_x, new_y))
                else:
                    break
                step += 1
        return possible_moves

class Queen(Figure):
    """
    Класс Queen представляет шахматную фигуру "Ферзь".
    Наследуется от класса Figure и реализует правила передвижения ферзя.

    Атрибуты:
        color (str): Цвет фигуры ('white' или 'black').
        position (tuple): Координаты фигуры на доске в формате (x, y).
        kill (bool): Флаг, указывающий, может ли фигура бить другие фигуры.

    Методы:
        __str__(): Возвращает строковое представление фигуры ('Q' для белых, 'q' для черных).
        get_possible_moves(): Определяет список возможных ходов фигуры в зависимости от ее текущей позиции.
    """
    def __str__(self):
        """Возвращает строковое представление фигуры."""
        return 'Q' if self.color == 'white' else 'q'

    def get_possible_moves(self):
        """
        Определяет список возможных ходов для ферзя.
        Ферзь ходит как ладья (по горизонтали и вертикали) и как слон (по диагонали) на любое количество клеток.

        Возвращает:
            list[tuple]: Список возможных координат для хода.
        """
        possible_moves = []
        x, y = self.position
        for i in range(8):
            if i != x:
                possible_moves.append((i, y))
            if i != y:
                possible_moves.append((x, i))

        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dx, dy in directions:
            step = 1
            while True:
                new_x, new_y = x + dx * step, y + dy * step
                if 0 <= new_x < 8 and 0 <= new_y < 8:
                    possible_moves.append((new_x, new_y))
                else:
                    break
                step += 1

        return possible_moves

class King(Figure):
    """
    Класс King представляет шахматную фигуру "Король".
    Наследуется от класса Figure и реализует правила передвижения короля.

    Атрибуты:
        color (str): Цвет фигуры ('white' или 'black').
        position (tuple): Координаты фигуры на доске в формате (x, y).
        kill (bool): Флаг, указывающий, может ли фигура бить другие фигуры.

    Методы:
        __str__(): Возвращает строковое представление фигуры ('K' для белых, 'k' для черных).
        get_possible_moves(): Определяет список возможных ходов фигуры в зависимости от ее текущей позиции.
    """
    def __str__(self):
        """Возвращает строковое представление фигуры."""
        return 'K' if self.color == 'white' else 'k'

    def get_possible_moves(self):
        """
        Определяет список возможных ходов для короля.
        Король может двигаться на одну клетку в любом направлении: вертикально, горизонтально и по диагонали.

        Возвращает:
            list[tuple]: Список возможных координат для хода.
        """
        possible_moves = []
        x, y = self.position
        possible_moves = possible_moves + [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1), (x + 1, y + 1),
                                           (x - 1, y - 1), (x + 1, y - 1), (x - 1, y + 1)]
        return possible_moves

class Snake(King):
    """
    Класс, представляющий фигуру "Змея", которая движется как король.

    Атрибуты:
        color (str): Цвет фигуры. Может быть "white" для белой фигуры и "black" для черной фигуры.
        position (tuple): Текущая позиция фигуры на доске, представлена кортежем (x, y).
        kill (bool): Параметр, который показывает, была ли сделана атака этой фигурой.
                     Если значение True, это значит, что фигура совершила атаку. По умолчанию False.

    Методы:
        __str__: Возвращает строковое представление фигуры ("S" для белой и "s" для черной).

        get_possible_moves: Возвращает список возможных ходов для фигуры "Змея".
                            Двигается как король, но также может проходить сквозь другие фигуры.
                            Все возможные ходы представлены как список кортежей (x, y), где
                            (x, y) — это координаты клетки на доске.
    """
    def __str__(self):
        """Строковое представление фигуры"""
        return 'S' if self.color == 'white' else 's'

class Board:
    """
    Класс, представляющий игровое поле для игры в шахматы.

    Атрибуты:
        letters (dict): Словарь для сопоставления буквенных координат столбцов (A-H) с числами (1-8).
        numbers (list): Список строковых значений для числовых координат (1-8).
        field (list): 2D список, представляющий игровое поле размером 8x8.
        history (list): Список для хранения истории состояния поля (для возможности отмены ходов).

    Методы:
        __init__: Инициализирует пустое поле размером 8x8, создает начальную расстановку фигур и сохраняет состояние поля.
        setup_board: Устанавливает начальную расстановку фигур на доске (пешки и фигуры на заднем ряду).
        display_current_board: Отображает текущее состояние поля на экране с координатами строк и столбцов.
        save_state: Сохраняет текущее состояние поля в истории.
        undo_move: Откатывает последний ход, восстанавливая предыдущее состояние поля.
        is_path_clear: Проверяет, свободен ли путь для хода фигуры от одной клетки до другой. Работает для горизонтальных, вертикальных и диагональных ходов.
        check_move: Проверяет, допустим ли ход фигуры с позиции step1 на позицию step2.
        if_rock_possible: Проверяет, возможен ли рокировка для игрока с указанным цветом.
        rock: Выполняет рокировку для игрока с указанным цветом.
        is_game_over: Проверяет, не окончена ли игра (шах или мат).
        make_move: Выполняет ход фигуры с позиции step1 на позицию step2, а также обрабатывает взятие фигуры противника.
    """
    letters = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8}
    numbers = ['1', '2', '3', '4', '5', '6', '7', '8']

    def __init__(self):
        """
        Инициализирует объект класса Board.

        Создает пустое игровое поле размером 8x8, устанавливает начальную расстановку фигур с помощью метода
        `setup_board` и сохраняет начальное состояние поля в истории для возможности отката ходов.

        Атрибуты:
            field (list): 2D список размером 8x8, представляющий игровое поле.
            history (list): История состояний поля, используемая для отката ходов.
        """
        self.field = [[None] * 8 for _ in range(8)]
        self.history = []
        self.setup_board()
        self.save_state()

    def setup_board(self):
        """
        Устанавливает начальную расстановку фигур на поле.
        """
        for col in range(8):
            self.field[1][col] = Pawn("black", (1, col))
            self.field[6][col] = Pawn("white", (6, col))
        back_row = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        for col, piece_class in enumerate(back_row):
            self.field[0][col] = piece_class("black", (0, col))
            self.field[7][col] = piece_class("white", (7, col))

    def display_current_board(self):
        """
        Отображает текущее состояние поля на экране.
        """
        print('\nТекущее состояние поля:\n')
        print('     ' + ' '.join([key for key in self.letters.keys()]), end='\n\n')
        for row in range(8):
            row_str = ' '.join(str(piece) if piece else '.' for piece in self.field[row])
            print(self.numbers[row] + '    ' + row_str + '    ' + self.numbers[row])
        print()
        print('     ' + ' '.join([key for key in self.letters.keys()]))
        print()

    def save_state(self):
        """
        Сохраняет текущее состояние поля в истории для возможности отката хода.
        """
        board_copy = [row.copy() for row in self.field]
        self.history.append(board_copy)

    def undo_move(self):
        """
        Откатывает последний ход, восстанавливая предыдущее состояние поля.
        """
        if len(self.history) > 1:
            self.history.pop()
            self.field = self.history[-1]
            print("Ход откатан.")
        else:
            print("Нет ходов для отката.")

    def is_path_clear(self, a1, b1, a2, b2):
        """
        Проверяет, свободен ли путь для хода фигуры от клетки (a1, b1) до клетки (a2, b2).
        Работает для горизонтальных, вертикальных и диагональных ходов.

        Параметры:
            a1, b1 (int): Координаты начальной клетки.
            a2, b2 (int): Координаты целевой клетки.

        Возвращает:
            bool: True, если путь свободен, иначе False.
        """
        if a1 == a2:
            for col in range(min(b1, b2) + 1, max(b1, b2)):
                if self.field[a1][col] is not None:
                    return False
            return True

        elif b1 == b2:
            for row in range(min(a1, a2) + 1, max(a1, a2)):
                if self.field[row][b1] is not None:
                    return False
            return True

        elif abs(a1 - a2) == abs(b1 - b2):
            row_step = 1 if a2 > a1 else -1
            col_step = 1 if b2 > b1 else -1
            row, col = a1 + row_step, b1 + col_step
            while row != a2 or col != b2:
                if self.field[row][col] is not None:
                    return False
                row += row_step
                col += col_step
            return True

    def check_move(self, step1, step2):
        """
        Проверяет, допустим ли ход фигуры с позиции step1 на позицию step2.

        Параметры:
            step1 (tuple): Начальная позиция (a1, b1).
            step2 (tuple): Целевая позиция (a2, b2).

        Возвращает:
            bool: True, если ход допустим, иначе False.
        """
        a1, b1 = step1
        a2, b2 = step2
        figure = self.field[a1][b1]
        enemy = self.field[a2][b2]

        if figure is None:
            return False
        if isinstance(figure, (Pawn, Rook, Bishop, Knight, King, Queen, Ghost, Snake)):
            possible_moves = figure.get_possible_moves()
            if isinstance(figure, Pawn) and isinstance(enemy, (Pawn, Rook, Bishop, Knight, King, Queen, Ghost, Snake)) and figure.color != enemy.color:
                possible_moves.clear()
                if figure.color == 'white':
                    possible_moves.append((a1 - 1, b1 + 1))
                    possible_moves.append((a1 - 1, b1 - 1))
                else:
                    possible_moves.append((a1 + 1, b1 + 1))
                    possible_moves.append((a1 + 1, b1 - 1))
            if (a2, b2) in possible_moves:
                if isinstance(figure, (Knight, Ghost)):
                    return True
                if self.is_path_clear(a1, b1, a2, b2):
                    return True
        return False

    def if_rock_possible(self, pl_color):
        """
        Проверяет, возможна ли рокировка для игрока с указанным цветом.

        Параметры:
            pl_color (str): Цвет игрока, который проверяет возможность рокировки ("white" или "black").

        Возвращает:
            bool: True, если рокировка возможна, иначе False.
        """
        if pl_color == 'white':
            if isinstance(self.field[0][4], King) and self.field[0][4].color == pl_color and isinstance(
                self.field[0][7], Rook) and self.field[0][7].color == pl_color and self.is_path_clear(0, 4, 0, 7):
                return True
        else:
            if isinstance(self.field[7][4], King) and self.field[7][4].color == pl_color and isinstance(self.field[7][7], Rook) and self.field[7][7].color == pl_color and self.is_path_clear(7, 4, 7, 7):
                return True
        return False

    def rock(self, pl_color):
        """
        Выполняет рокировку для игрока с указанным цветом.

        Параметры:
            pl_color (str): Цвет игрока, который выполняет рокировку ("white" или "black").
        """
        if pl_color == 'white':
            self.field[0][6] = self.field[0][4]
            self.field[0][4] = None
            self.field[0][5] = self.field[0][7]
            self.field[0][7] = None
        elif pl_color == 'black':
            self.field[7][6] = self.field[7][4]
            self.field[7][4] = None
            self.field[7][5] = self.field[7][7]
            self.field[7][7] = None

    def is_game_over(self):
        """
        Проверяет, не окончена ли игра (шах или мат).

        Возвращает:
            bool: True, если игра завершена, иначе False.
        """
        potential_risks_for_black = []
        potential_risks_for_white = []
        black_king_position = None
        white_king_position = None

        for row in range(8):
            for col in range(8):
                piece = self.field[row][col]
                if isinstance(piece, King):
                    if piece.color == 'black':
                        black_king_position = (row, col)
                    elif piece.color == 'white':
                        white_king_position = (row, col)

        for row in range(8):
            for col in range(8):
                piece = self.field[row][col]

                if isinstance(piece, (Pawn, Rook, Bishop, Knight, King, Queen)):
                    if piece.color == 'white':
                        if self.is_path_clear(row, col, black_king_position[0], black_king_position[1]):
                            potential_risks_for_black.extend(piece.get_possible_moves())
                    elif piece.color == 'black':
                        if self.is_path_clear(row, col, white_king_position[0], white_king_position[1]):
                            potential_risks_for_white.extend(piece.get_possible_moves())

        if black_king_position and black_king_position in potential_risks_for_black:
            print('Король "black", берегись!! (Шах)')
            black_king = self.field[black_king_position[0]][black_king_position[1]]
            if all(move in potential_risks_for_black for move in black_king.get_possible_moves()):
                return True
            return False

        if white_king_position and white_king_position in potential_risks_for_white:
            print('Король "white", берегись!! (Шах)')
            white_king = self.field[white_king_position[0]][white_king_position[1]]
            if all(move in potential_risks_for_white for move in white_king.get_possible_moves()):
                return True
            return False

        return False

    def make_move(self, step1, step2):
        """
        Выполняет ход фигуры с позиции step1 на позицию step2, обрабатывая взятие фигуры противника.

        Параметры:
            step1 (tuple): Начальная позиция (a1, b1).
            step2 (tuple): Целевая позиция (a2, b2).
        """
        a1, b1 = step1
        a2, b2 = step2
        figure = self.field[a1][b1]
        if isinstance(self.field[a2][b2], (Pawn, Rook, Knight, Bishop, King, Queen, Ghost, Snake, CheckersFigure)):
            print(f'\nИгрок бьет фигуру противника')
            if isinstance(figure, Snake):
                figure.kill = True
        self.field[a2][b2] = figure
        figure.position = (a2, b2)
        self.field[a1][b1] = None
        self.save_state()

class CheckersBoard(Board):
    """
    Класс для представления доски для игры в шашки.

    Наследует от класса `Board`, но переопределяет методы для работы с игрой в шашки, включая установку начальной
    расстановки фигур, проверку допустимости хода и выполнение ходов с возможностью взятия фигур.

    Атрибуты:
        field (list): 2D список размером 8x8, представляющий игровое поле.

    Методы:
        __init__: Инициализация игрового поля для шашек.
        setup_board: Установка начальной расстановки фигур для шашек.
        check_move: Проверка, является ли ход допустимым для шашки или слона.
        make_move: Выполнение хода, включая взятие фигуры противника.
        is_game_over: Проверка, завершена ли игра.
    """

    def __init__(self):
        """
        Инициализирует объект класса CheckersBoard.

        Вызывает инициализацию родительского класса `Board` и настраивает доску для игры в шашки.
        """
        super().__init__()

    def setup_board(self):
        """
        Устанавливает начальную расстановку фигур на поле.

        Черные фигуры располагаются на четных колонках первых трех строк, белые — на нечетных колонках
        трех последних строк. Фигуры черных и белых игроков размещаются только на черных клетках доски.
        """
        for col in range(8):
            if col % 2 != 0:
                self.field[0][col] = CheckersFigure("black", (0, col))
                self.field[2][col] = CheckersFigure("black", (2, col))
                self.field[6][col] = CheckersFigure("white", (6, col))
            else:
                self.field[7][col] = CheckersFigure("white", (6, col))
                self.field[1][col] = CheckersFigure("black", (1, col))
                self.field[5][col] = CheckersFigure("white", (5, col))

    def check_move(self, step1, step2):
        """
        Проверяет, является ли ход допустимым для выбранной фигуры.

        Параметры:
            step1 (tuple): Начальная позиция фигуры (a1, b1).
            step2 (tuple): Конечная позиция фигуры (a2, b2).

        Возвращает:
            bool: `True`, если ход допустим, иначе `False`.
        """
        a1, b1 = step1
        a2, b2 = step2
        figure = self.field[a1][b1]
        if figure is None or not isinstance(figure, (CheckersFigure, Bishop)):
            return False
        possible_moves = figure.get_possible_moves()

        if isinstance(figure, Bishop):
            if (a2, b2) in possible_moves:
                return True
        else:
            if abs(a2 - a1) == 2 and abs(b2 - b1) == 2 and not self.is_path_clear(a1, b1, a2, b2):
                return True

            if (a2, b2) in possible_moves and self.is_path_clear(a1, b1, a2, b2):
                return True

        return False

    def make_move(self, step1, step2):
        """
        Выполняет ход на доске, включая взятие фигуры противника.

        Параметры:
            step1 (tuple): Начальная позиция фигуры (a1, b1).
            step2 (tuple): Конечная позиция фигуры (a2, b2).
        """
        a1, b1 = step1
        a2, b2 = step2
        figure = self.field[a1][b1]

        if not self.is_path_clear(a1, b1, a2, b2):
            if isinstance(figure, CheckersFigure):
                mid_x = (a1 + a2) // 2
                mid_y = (b1 + b2) // 2
                print(f'\nИгрок бьет фигуру противника')
                figure.kill = True

                self.field[mid_x][mid_y] = None
            elif isinstance(figure, Bishop):
                col = 1
                if a1 < a2 and b1 < b2:
                    for row in range(a1 + 1, a2):
                        self.field[row][b1 + 1 * col] = None
                        col += 1
                elif a1 > a2 and b1 < b2:
                    for row in range(a1 + 1, a2):
                        self.field[row][b1 - 1 * col] = None
                        col += 1
                elif a1 < a2 and b1 > b2:
                    for row in range(a1 + 1, a2, -1):
                        self.field[row][b1 + 1 * col] = None
                        col += 1
                elif a1 < a2 and b1 < b2:
                    for row in range(a1 + 1, a2, -1):
                        self.field[row][b1 - 1 * col] = None
                        col += 1
                print(f'\nИгрок бьет фигуру противника')
                figure.kill = True

        self.field[a2][b2] = figure
        figure.position = (a2, b2)
        self.field[a1][b1] = None

        if (figure.color == 'white' and a2 == 0) or (figure.color == 'black' and a2 == 7):
            self.field[a2][b2] = Bishop(figure.color, (a2, b2))
            print(f'\nФигура {figure.color} стала дамкой!')

    def is_game_over(self):
        """
        Проверяет, завершена ли игра в шашки.

        Возвращает:
            bool: `True`, если игра завершена, иначе `False`.
        """
        black = False
        white = False
        for row in range(8):
            for col in range(8):
                figure = self.field[row][col]
                if isinstance(figure, CheckersFigure):
                    if figure.color == 'white':
                        white = True
                    elif figure.color == 'black':
                        black = True

                    for move in figure.get_possible_moves():
                        if self.check_move((row, col), move):
                            return False

        return not (black and white)

class ExtendedBoard(Board):
    """
    Класс для представления расширенной доски для игры в шашки с дополнительными фигурами.

    Наследует от класса `Board`, расширяя стандартную игру в шашки за счет добавления новых типов фигур:
    `Ghost` и `Snake`.

    Атрибуты:
        field (list): 2D список размером 8x8, представляющий игровое поле, на котором размещаются как стандартные
                      шашки, так и новые типы фигур (призраки и змеи).
        history (list): История состояний поля, используемая для отката ходов.

    Методы:
        __init__: Инициализация игрового поля для расширенной игры.
        setup_board: Установка начальной расстановки фигур на поле, включая стандартные шашки, а также призраков
                     и змей на специально выбранных клетках.
    """

    def __init__(self):
        """
        Инициализирует объект класса ExtendedBoard.

        Вызывает инициализацию родительского класса `Board` и настраивает расширенную доску с дополнительными
        фигурами для игры.
        """
        super().__init__()

    def setup_board(self):
        """
        Устанавливает начальную расстановку фигур на расширенной доске.

        На поле размещаются стандартные шашки, а также дополнительные фигуры:
        - Призраки (Ghost) на клетках (5, 1), (5, 6), (2, 1), (2, 6),
        - Змеи (Snake) на клетках (5, 0), (5, 7), (2, 0), (2, 7).
        """
        super().setup_board()
        self.field[5][2] = CheckersFigure("white", (5, 2))
        self.field[5][5] = CheckersFigure("white", (5, 5))
        self.field[2][2] = CheckersFigure("black", (2, 2))
        self.field[2][5] = CheckersFigure("black", (2, 5))
        self.field[5][1] = Ghost("white", (5, 1))
        self.field[5][6] = Ghost("white", (5, 6))
        self.field[2][1] = Ghost("black", (2, 1))
        self.field[2][6] = Ghost("black", (2, 6))
        self.field[5][0] = Snake("white", (5, 0))
        self.field[5][7] = Snake("white", (5, 7))
        self.field[2][0] = Snake("black", (2, 0))
        self.field[2][7] = Snake("black", (2, 7))


class Game:
    """
    Класс для управления игрой в шахматы или шашки.

    Атрибуты:
        board (Board): Объект класса `Board`, представляющий игровое поле.
        current_player (str): Текущий игрок (цвет), который ходит, например, "white" или "black".
        game_over (bool): Флаг, показывающий, завершена ли игра.
        moves (list): Список, хранящий координаты хода.
        is_rock (bool): Флаг, указывающий, выполняет ли игрок рокировку.
        is_chess (bool): Флаг, указывающий, играется ли шахматная партия. Если False — играются шашки.

    Методы:
        __init__: Инициализирует игру с доской и настраивает параметры.
        play: Запускает основной игровой процесс, чередуя ходы игроков, проверяя состояния игры и обрабатывая возможные действия.
    """

    def __init__(self, is_chess):
        """
        Инициализирует игру с настройками для игры в шахматы или шашки.

        Аргументы:
            is_chess (bool): Если True, игра будет в шахматы, иначе — в шашки.
        """
        self.board = Board()
        self.current_player = 'white'
        self.game_over = False
        self.moves = []
        self.is_rock = False
        self.is_chess = is_chess

    def play(self):
        """
        Запускает игровой процесс, чередуя ходы игроков, проверяя завершение игры и управляя действиями (например, рокировкой).

        В процессе игры:
        - Отображается текущее состояние доски.
        - Проверяется завершение игры.
        - Если возможно, предлагается выполнить рокировку (для шахмат).
        - Игроки делают ходы, которые проверяются на корректность.
        - В шахматах предоставляется возможность откатить последний ход.
        """
        while not self.game_over:
            self.board.display_current_board()
            if self.board.is_game_over():
                print(f"Конец игры!! Игрок {self.current_player} проиграл :(")
                self.game_over = True
            else:
                if self.board.if_rock_possible(self.current_player):
                    decision = input(
                        f'Игрок {self.current_player}, вы можете сделать рокировку. Напишите "да" или "нет":\n\n')
                    if decision.lower() == 'да':
                        self.is_rock = True
                        self.board.rock(self.current_player)
                        self.current_player = "black" if self.current_player == "white" else "white"
                        self.moves = []
                if not self.is_rock:
                    if self.is_chess:
                        undo_decision = input(
                            f'Игрок {self.current_player}, хотите откатить последний ход? (да/нет):\n\n')
                        if undo_decision.lower() == 'да':
                            self.board.undo_move()
                            self.current_player = "black" if self.current_player == "white" else "white"
                            continue
                    move = input(f'Игрок {self.current_player} делает ход:\n\n').split()
                    for step in move:
                        coords = tuple(step)
                        for coord in coords:
                            if coord.upper() in Board.letters:
                                y = Board.letters[coord.upper()] - 1
                            elif coord in Board.numbers:
                                x = int(coord) - 1
                            else:
                                print("Координаты введены неверно.")
                                self.moves = []
                        self.moves.append((x, y))
                    if self.board.check_move(self.moves[0], self.moves[1]):
                        self.board.make_move(self.moves[0], self.moves[1])
                        if not self.board.field[self.moves[1][0]][self.moves[1][1]].kill:
                            self.current_player = "black" if self.current_player == "white" else "white"
                            self.board.field[self.moves[1][0]][self.moves[1][1]].kill = False
                        else:
                            print(f'Игрок {self.current_player} продолжает ходить')
                            self.board.field[self.moves[1][0]][self.moves[1][1]].kill = False
                        self.moves = []
                    else:
                        print("Неверный ход, попробуйте снова.")
                        self.moves = []
            self.is_rock = False


class CheckersGame(Game):
    """
    Класс для управления игрой в шашки, наследующий от класса `Game`.

    Атрибуты:
        board (CheckersBoard): Объект класса `CheckersBoard`, представляющий игровое поле для шашек.
        current_player (str): Текущий игрок (цвет), который ходит, например, "white" или "black".
        game_over (bool): Флаг, показывающий, завершена ли игра.
        moves (list): Список, хранящий координаты хода.
        is_rock (bool): Флаг, указывающий, выполняет ли игрок рокировку. Не используется в шашках.
        is_chess (bool): Флаг, указывающий, играются ли шахматы. Для шашек всегда False.

    Методы:
        __init__: Инициализирует игру в шашки, создавая объект доски для шашек.
    """

    def __init__(self, is_chess):
        """
        Инициализирует игру в шашки, создавая игровое поле и устанавливая параметры игры.

        Аргументы:
            is_chess (bool): Флаг для указания, является ли игра шахматами. Для шашек всегда False.
        """
        super().__init__(is_chess)
        self.board = CheckersBoard()

class ExtendedGame(Game):
    """
    Класс для управления расширенной игрой, которая включает в себя дополнительные фигуры и элементы,
    унаследованный от класса `Game`.

    Атрибуты:
        board (ExtendedBoard): Объект класса `ExtendedBoard`, представляющий игровое поле с дополнительными фигурами.
        current_player (str): Текущий игрок (цвет), который ходит, например, "white" или "black".
        game_over (bool): Флаг, показывающий, завершена ли игра.
        moves (list): Список, хранящий координаты хода.
        is_rock (bool): Флаг, указывающий, выполняет ли игрок рокировку. Не используется в данной игре.
        is_chess (bool): Флаг, указывающий, играются ли шахматы. Для расширенной игры может быть True или False.

    Методы:
        __init__: Инициализирует расширенную игру, создавая объект доски с дополнительными фигурами.
    """

    def __init__(self, is_chess):
        """
        Инициализирует расширенную игру, создавая игровое поле с дополнительными фигурами и устанавливая параметры игры.

        Аргументы:
            is_chess (bool): Флаг для указания, является ли игра шахматами. Может быть True для шахмат или False для других игр.
        """
        super().__init__(is_chess)
        self.board = ExtendedBoard()


game_kind = input("Выберите в какую игру вы хотите поиграть: 'шахматы', 'шашки' или 'расширенные шахматы':\n\n").lower()

if game_kind == 'шахматы':
    game = Game(True)
    game.play()
elif game_kind == 'шашки':
    game = CheckersGame(False)
    game.play()
elif game_kind == 'расширенные шахматы':
    game = ExtendedGame(True)
    game.play()
else:
    print("Неверный ввод. Пожалуйста, выберите одну из предложенных игр: 'шахматы', 'шашки' или 'расширенные шахматы'.")


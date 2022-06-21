import pathlib
import random
import typing as tp

T = tp.TypeVar("T")


def read_sudoku(path: tp.Union[str, pathlib.Path]) -> tp.List[tp.List[str]]:
    """ Прочитать Судоку из указанного файла """
    path = pathlib.Path(path)
    with path.open() as f:
        puzzle = f.read()
    return create_grid(puzzle)


def create_grid(puzzle: str) -> tp.List[tp.List[str]]:
    digits = [c for c in puzzle if c in "123456789."]
    grid = group(digits, 9)
    return grid


def display(grid: tp.List[tp.List[str]]) -> None:
    """Вывод Судоку """
    width = 2
    line = "+".join(["-" * (width * 3)] * 3)
    for row in range(9):
        print(
            "".join(
                grid[row][col].center(width) + ("|" if str(col) in "25" else "") for col in range(9)
            )
        )
        if str(row) in "25":
            print(line)
    print()


def group(values: tp.List[T], n: int) -> tp.List[tp.List[T]]:
    """
    Сгруппировать значения values в список, состоящий из списков по n элементов

    >>> group([1,2,3,4], 2)
    [[1, 2], [3, 4]]
    >>> group([1,2,3,4,5,6,7,8,9], 3)
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    """
    return [values[i : i + n] for i in range(0, len(values), n)]


def get_row(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Возвращает все значения для номера строки, указанной в pos

    >>> get_row([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '2', '.']
    >>> get_row([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (1, 0))
    ['4', '.', '6']
    >>> get_row([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (2, 0))
    ['.', '8', '9']
    """
    row, col = pos
    return grid[row]


def get_col(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Возвращает все значения для номера столбца, указанного в pos

    >>> get_col([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '4', '7']
    >>> get_col([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (0, 1))
    ['2', '.', '8']
    >>> get_col([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (0, 2))
    ['3', '6', '9']
    """
    row, col = pos
    collumn = []
    for i in grid:
        collumn.append(i[col])
    return collumn


def get_block(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Возвращает все значения из квадрата, в который попадает позиция pos

    >>> grid = read_sudoku('puzzle1.txt')
    >>> get_block(grid, (0, 1))
    ['5', '3', '.', '6', '.', '.', '.', '9', '8']
    >>> get_block(grid, (4, 7))
    ['.', '.', '3', '.', '.', '1', '.', '.', '6']
    >>> get_block(grid, (8, 8))
    ['2', '8', '.', '.', '.', '5', '.', '7', '9']
    """
    row, col = pos
    block = []
    grid_size = 3

    v = (row // grid_size) * grid_size
    h = (col // grid_size) * grid_size

    for i in range(0, grid_size):
        for j in range(0, grid_size):
            block.append(grid[v + i][h + j])
    return block


def find_empty_positions(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.Tuple[int, int]]:
    """Найти первую свободную позицию в пазле

    >>> find_empty_positions([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']])
    (0, 2)
    >>> find_empty_positions([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']])
    (1, 1)
    >>> find_empty_positions([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']])
    (2, 0)
    """
    for i, g in enumerate(grid):
        for j, v in enumerate(g):
            if v == ".":
                return (i, j)
    return None


def find_possible_values(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.Set[str]:
    """Вернуть множество возможных значения для указанной позиции

    >>> grid = read_sudoku('puzzle1.txt')
    >>> values = find_possible_values(grid, (0,2))
    >>> values == {'1', '2', '4'}
    True
    >>> values = find_possible_values(grid, (4,7))
    >>> values == {'2', '5', '9'}
    True
    """
    values = {"1", "2", "3", "4", "5", "6", "7", "8", "9"}
    grid_values = set()  # type: tp.Set[str]
    grid_values.update(set(get_row(grid, pos)), set(get_col(grid, pos)), set(get_block(grid, pos)))
    return values.difference(grid_values)


def solve(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.List[tp.List[str]]]:
    """ Решение пазла, заданного в grid """
    """ Как решать Судоку?
        1. Найти свободную позицию
        2. Найти все возможные значения, которые могут находиться на этой позиции
        3. Для каждого возможного значения:
            3.1. Поместить это значение на эту позицию
            3.2. Продолжить решать оставшуюся часть пазла

    >>> grid = read_sudoku('puzzle1.txt')
    >>> solve(grid)
    [['5', '3', '4', '6', '7', '8', '9', '1', '2'], ['6', '7', '2', '1', '9', '5', '3', '4', '8'], ['1', '9', '8', '3', '4', '2', '5', '6', '7'], ['8', '5', '9', '7', '6', '1', '4', '2', '3'], ['4', '2', '6', '8', '5', '3', '7', '9', '1'], ['7', '1', '3', '9', '2', '4', '8', '5', '6'], ['9', '6', '1', '5', '3', '7', '2', '8', '4'], ['2', '8', '7', '4', '1', '9', '6', '3', '5'], ['3', '4', '5', '2', '8', '6', '1', '7', '9']]
    """

    while True:
        if not find_empty_positions(grid):
            return grid
        pos = find_empty_positions(grid)
        if pos is not None:
            possible = find_possible_values(grid, pos)
            if not possible:
                grid[pos[0]][pos[1]] = "."
                return False  # type: ignore
            for i in possible:
                grid[pos[0]][pos[1]] = i
                result = solve(grid)
                if result:
                    return result
            grid[pos[0]][pos[1]] = "."
            return False  # type: ignore


def check_solution(solution: tp.List[tp.List[str]]) -> bool:
    """ Если решение solution верно, то вернуть True, в противном случае False """
    # TODO: Add doctests with bad puzzles
    values = {"1", "2", "3", "4", "5", "6", "7", "8", "9"}
    for i, row in enumerate(solution):
        if values.difference(set(row)) != set():
            return False
        if values.difference(set(get_col(solution, (0, i)))) != set():
            return False
        if values.difference(set(get_block(solution, (i // 3 * 3, i // +3)))) != set():
            return False
        else:
            for v in row:
                if v == ".":
                    return False
    return True


def generate_sudoku(N: int) -> tp.List[tp.List[str]]:
    """Генерация судоку заполненного на N элементов

    >>> grid = generate_sudoku(40)
    >>> sum(1 for row in grid for e in row if e == '.')
    41
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(1000)
    >>> sum(1 for row in grid for e in row if e == '.')
    0
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(0)
    >>> sum(1 for row in grid for e in row if e == '.')
    81
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    """
    n = 3
    grid = [[str((i * n + i // n + j) % (n * n) + 1) for j in range(n * n)] for i in range(n * n)]

    def transposing(grid):
        """ Транспонирование таблицы """
        transposing_grid = list(map(list, zip(*grid)))
        return transposing_grid

    def swap_rows_small(grid, n):
        area = random.randrange(0, n)
        line1 = random.randrange(0, n)
        N1 = area * n + line1
        line2 = random.randrange(0, n)
        while line1 == line2:
            line2 = random.randrange(0, n)
        N2 = area * n + line2
        grid[N1], grid[N2] = grid[N2], grid[N1]
        return grid

    def swap_colums_small(grid):
        swap_grid = transposing(grid)
        swap_grid = swap_rows_small(swap_grid, n)
        swap_grid = transposing(swap_grid)
        return swap_grid

    def swap_rows_area(grid, n):
        area1 = random.randrange(0, n)
        area2 = random.randrange(0, n)
        while area1 == area2:
            area2 = random.randrange(0, n)
        for i in range(0, n):
            N1, N2 = area1 * n + i, area2 * n + i
            grid[N1], grid[N2] = grid[N2], grid[N1]
        return grid

    def swap_colums_area(grid):
        swap_grid = transposing(grid)
        swap_grid = swap_rows_area(swap_grid, n)
        swap_grid = transposing(swap_grid)
        return swap_grid

    def mix(grid):
        count = 15
        for i in range(1, count):
            id_func = random.randrange(0, 5)
            if id_func == 0:
                mixed_grid = transposing(grid)
            elif id_func == 1:
                mixed_grid = swap_rows_small(grid, n)
            elif id_func == 2:
                mixed_grid = swap_colums_small(grid)
            elif id_func == 3:
                mixed_grid = swap_rows_area(grid, n)
            elif id_func == 4:
                mixed_grid = swap_colums_area(grid)
        return mixed_grid

    generated_grid = mix(grid)
    flook = [[0 for j in range(n * n)] for i in range(n * n)]
    difficult = n ** 4 - N
    if difficult != 0:
        while difficult > 0:
            i, j = random.randrange(0, n * n), random.randrange(0, n * n)
            if flook[i][j] == 0:
                flook[i][j] = 1
                generated_grid[i][j] = "."
                difficult -= 1
        return generated_grid
    else:
        return [["'" for j in range(n * n)] for i in range(n * n)]


if __name__ == "__main__":
    for fname in ["puzzle1.txt", "puzzle2.txt", "puzzle3.txt"]:
        grid = read_sudoku(fname)
        display(grid)
        solution = solve(grid)
        if not solution:
            print(f"Puzzle {fname} can't be solved")
        else:
            display(solution)

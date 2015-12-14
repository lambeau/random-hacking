import random

count_columns = 7
count_rows = 4

matrix = [[random.randint(0, 1) for i in range(count_columns)] for j in range(count_rows)]


def print_matrix():
    for row in matrix:
        for value in row:
            print(value if value else ' ', end=' ')
        print()


def clear(r, c):
    if r < 0 or r >= count_rows or c < 0 or c >= count_columns or matrix[r][c] == 0:
        return
    matrix[r][c] = 0
    clear(r, c+1)
    clear(r, c-1)
    clear(r+1, c)
    clear(r-1, c)


def main():
    print_matrix()
    islands = 0

    for r, row in enumerate(matrix):
        for c, value in enumerate(row):
            if value == 1:
                islands += 1
                clear(r, c)

    print('islands: {}'.format(islands))


if __name__ == '__main__':
    main()

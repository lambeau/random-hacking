import random
import sys

sys.setrecursionlimit(15000)

count_columns = 50
count_rows = 40

matrix = [[random.randint(0, 1) for i in range(count_columns)] for j in range(count_rows)]
matrix = [[0] * count_columns for _ in range(count_rows)]
for _ in range(10):
    matrix[random.randint(0, count_rows - 1)][random.randint(0, count_columns - 1)] = 1
visited = [[False] * len(row) for row in matrix]

def print_matrix():
    for row in matrix:
        for value in row:
            print(value if value else ' ', end=' ')
        print()


# can use stack if recursion depth is too much - just push items on to be spread
# and iterate in a loop
def spread(r, c):
    if r < 0 or r >= count_rows or c < 0 or c >= count_columns:
        return

    if matrix[r][c] == 1 and not visited[r][c]:
        visited[r][c] = True
        spread(r, c+1)
        spread(r, c-1)
        spread(r+1, c)
        spread(r-1, c)
    else:
        matrix[r][c] = 1
    visited[r][c] = True



time = 0

while not all(all(row) for row in matrix):
    print_matrix()
    print()
    time += 1
    visited = [[False] * len(row) for row in matrix]
    for r, row in enumerate(matrix):
        for c, value in enumerate(row):
            if not visited[r][c] and value == 1:
                spread(r, c)
            visited[r][c] = True

print_matrix()
print(time)

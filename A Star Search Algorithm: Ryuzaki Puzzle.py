from sys import stdin, stdout
from heapq import heappush, heappop, heapify


def create_board(n, m):
    board = [[-1] * (m + 2) for i in range(n + 2)]
    board[0] = [None] * (m + 2)
    board[n + 1] = [None] * (m + 2)
    for i in range(1, n + 1):
        board[i][0] = None
        board[i][m + 1] = None
    return board


def add_tile(tiles, row):
    data = []
    for i in range(4):
        data.append((i, row[i]))
    data.sort(key=lambda a: a[1])
    tiles.append(data)


def a_star(m, n, tiles, min_weight):
    remaining_tiles = [*range(1, n * m)]

    heap = []
    heapify(heap)
    for row in range(1, n + 1):
        for column in range(1, m + 1):
            state = [[*item] for item in board]
            state[row][column] = 0
            heappush(heap, (0, len(remaining_tiles) * min_weight, state, remaining_tiles))

    ans = []
    possible_connection = {
        0: lambda i, j: [i - 1, j],
        1: lambda i, j: [i, j + 1],
        2: lambda i, j: [i + 1, j],
        3: lambda i, j: [i, j - 1],
    }
    while heap:
        g_distance, h_distance, state, remaining_tiles = heappop(heap)
        if h_distance == 0:
            ans.append(g_distance)
            continue
        h = h_distance - min_weight
        g = 10E10
        next_tiles_expanded = []
        for tile in remaining_tiles:
            for side_place, weight in tiles[tile]:
                could_connect_to_place_side = (side_place + 2) % 4
                for row in range(1, n + 1):
                    for column in range(1, m + 1):
                        if state[row][column] != -1 or g_distance + weight > g:
                            continue
                        new_row, new_column = possible_connection[side_place](row, column)
                        this_state = state[new_row][new_column]
                        if this_state != -1 and this_state is not None:
                            if list(filter(lambda x: x[0] == could_connect_to_place_side, tiles[this_state]))[0][1] == weight:
                                new_state = [[*item] for item in state]
                                new_state[row][column] = tile
                                new_g = g_distance + weight
                                if new_g <= g:
                                    g = new_g
                                    next_tiles_expanded.append((g, h, new_state, [node for node in remaining_tiles if node != tile]))

        for next_tile in next_tiles_expanded:
            heappush(heap, next_tile)

    return min(ans)


tiles_list = []
min_weight = 10E10

n, m = [int(i) for i in stdin.readline().split()]
board = create_board(n, m)

for i in range(n * m):
    row = [int(i) for i in input().split()]
    add_tile(tiles_list, row)
    min_weight = min(min_weight, *row)

print(a_star(m, n, tiles_list, min_weight))

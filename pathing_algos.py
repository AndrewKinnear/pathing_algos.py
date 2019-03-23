# 2018 - Pathing Algos, currently BFS, best first search, A* still to do dijkstra
# Also started this the 3rd day of learning python, probably going to look messy in a few months

from collections import deque
import time
import math


max_size = 20   


class GridElement:

    def __init__(self, x, y, prev_x, prev_y, known, can_trav, dist):
        self.x = x
        self.y = y
        self.prev_x = prev_x
        self.prev_y = prev_y
        self.known = known
        self.can_trav = can_trav
        self.dist = dist
        
def make_grid_elements(grid):
    grid_elements = [[GridElement] * max_size for _ in range(max_size)]
    for x in range(max_size):
        for y in range(max_size):
            if grid[x][y] == '*':
                grid_elements[x][y] = GridElement(x, y, None, None, None, None, 0)
            else:
                grid_elements[x][y] = GridElement(x, y, None, None, None, True, 0)
    return grid_elements

def make_grid():
    grid = [['-'] * max_size for _ in range(max_size)]
    for x in range(max_size):
        for y in range(max_size):
            grid[x][y] = '-'
    return grid





def build_walls(grid):
    for x in range(200):
        grid[x][15] = '*'
    for x in range(400):
        grid[202][x] = '*'

    print("test")



def pick_start_finish(grid):
    grid[599][599] = 's'
    grid[1][1] = 'f'


def print_grid(grid):
    for x in range(max_size):
        for y in range(max_size):
            print(grid[x][y], end=' ')
        print()
    print()


def find_start(grid):
    start_x = 0
    start_y = 0
    for x in range(max_size):
        for y in range(max_size):
            if grid[x][y] == 's':
                start_x = x
                start_y = y
                break
    return start_x, start_y


def find_end(grid):
    end_x = 0
    end_y = 0
    for x in range(max_size):
        for y in range(max_size):
            if grid[x][y] == 'f':
                end_x = x
                end_y = y
                break
    return end_x, end_y


def bfs(grid, grid_elements):
    my_que = deque()
    start_x, start_y = find_start(grid)
    end_x, end_y = find_end(grid)
    rx = [-1, 1, 0, 0, -1, -1, 1, 1]
    ry = [0, 0, 1, -1, -1, 1, -1, 1]
    # rx = [-1, 1, 0, 0]
    # ry = [0, 0, 1, -1]
    grid_elements[start_x][start_y].known = True
    my_que.append(grid_elements[start_x][start_y])
    counter = 0
    while len(my_que) > 0:
        counter += 1
        news = 0
        tmp_grid_ele = my_que.popleft()
        if tmp_grid_ele.x == end_x and tmp_grid_ele.y == end_y:
            print(f"Calls {counter}")
            return end_x, end_y
        while news < len(rx):
            xx = tmp_grid_ele.x + rx[news]
            
            yy = tmp_grid_ele.y + ry[news]
            if xx < 0 or yy < 0:
                news += 1
                continue
            if yy >= max_size or xx >= max_size:
                news += 1
                continue
            if grid_elements[xx][yy].known:
                news += 1
                continue
            # if xx == start_x and yy == start_y:
            #     news += 1
            #     continue
            if not grid_elements[xx][yy].can_trav:
                news += 1
                continue
            grid_elements[xx][yy].known = True
            grid[xx][yy] = 'O'
            # print_grid(grid)
            grid_elements[xx][yy].prev_x = tmp_grid_ele.x
            grid_elements[xx][yy].prev_y = tmp_grid_ele.y
            my_que.append(grid_elements[xx][yy])
            news += 1


def best_first_search(grid, grid_elements):
    my_que = deque()
    counter = 0
    start_x, start_y = find_start(grid)
    end_x, end_y = find_end(grid)
    # rx = [-1, 1, 0, 0, -1, -1, 1, 1]
    # ry = [0, 0, 1, -1, -1, 1, -1, 1]
    rx = [-1, 1, 0, 0]
    ry = [0, 0, 1, -1]
    grid_elements[start_x][start_y].known = True
    my_que.append(grid_elements[start_x][start_y])

    while len(my_que) > 0:
        news = 0
        counter += 1
        tmp_grid_ele = my_que.popleft()
        parent_dist = math.sqrt((tmp_grid_ele.x - end_x) ** 2 + (tmp_grid_ele.y - end_y) ** 2)
        if tmp_grid_ele.x == end_x and tmp_grid_ele.y == end_y:
            print(f"Calls {counter}")
            return end_x, end_y
        while news < len(rx):
            xx = tmp_grid_ele.x + rx[news]
            yy = tmp_grid_ele.y + ry[news]
            if xx < 0 or yy < 0:
                news += 1
                continue
            if yy >= max_size or xx >= max_size:
                news += 1
                continue
            if grid_elements[xx][yy].known:
                news += 1
                continue
            # if xx == start_x and yy == start_y:
            #     news += 1
            #     continue
            if not grid_elements[xx][yy].can_trav:
                news += 1
                continue
            child_dist = math.sqrt((xx - end_x) ** 2 + (yy - end_y) ** 2)
            grid_elements[xx][yy].known = True
            grid[xx][yy] = 'O'
            #print_grid(grid)
            grid_elements[xx][yy].prev_x = tmp_grid_ele.x
            grid_elements[xx][yy].prev_y = tmp_grid_ele.y
            if child_dist < parent_dist:
                my_que.appendleft(grid_elements[xx][yy])
            else:
                my_que.append(grid_elements[xx][yy])
            news += 1


def a_star(grid, grid_elements):
    my_que = deque()
    start_x, start_y = find_start(grid)
    end_x, end_y = find_end(grid)
    dist_counter = 0
    rx = [-1, 1, 0, 0, -1, -1, 1, 1]
    ry = [0, 0, 1, -1, -1, 1, -1, 1]
    counter = 0


    grid_elements[start_x][start_y].known = True
    my_que.append(grid_elements[start_x][start_y])

    while len(my_que) > 0:
        counter += 1
        news = 0
        tmp_grid_ele = my_que.popleft()
        parent_dist_to_end = math.sqrt((tmp_grid_ele.x - end_x) ** 2 + (tmp_grid_ele.y - end_y) ** 2)
        parent_dist_to_start = math.sqrt((tmp_grid_ele.x - start_x) ** 2 + (tmp_grid_ele.y - start_y) ** 2)
        if tmp_grid_ele.x == end_x and tmp_grid_ele.y == end_y:
            print(f"Calls {counter}")
            return end_x, end_y
        while news < len(rx):
            xx = tmp_grid_ele.x + rx[news]
            yy = tmp_grid_ele.y + ry[news]
            if xx < 0 or yy < 0:
                news += 1
                continue
            if yy >= max_size or xx >= max_size:
                news += 1
                continue
            if grid_elements[xx][yy].known:
                news += 1
                continue
            if not grid_elements[xx][yy].can_trav:
                news += 1
                continue
            child_dist_to_end = math.sqrt((xx - end_x) ** 2 + (yy - end_y) ** 2)
            child_dist_to_start = math.sqrt((xx - start_x) ** 2 + (yy - start_y) ** 2)
            grid_elements[xx][yy].known = True
            grid[xx][yy] = 'O'
            # print_grid(grid)
            grid_elements[xx][yy].dist = dist_counter
            grid_elements[xx][yy].prev_x = tmp_grid_ele.x
            grid_elements[xx][yy].prev_y = tmp_grid_ele.y
            if child_dist_to_end < parent_dist_to_end and child_dist_to_start < parent_dist_to_start: #if we add in an or, instead of and becomes a patrol
                my_que.appendleft(grid_elements[xx][yy])
            else:
                my_que.append(grid_elements[xx][yy])
            news += 1


def trace_back_to_start(grid, grid_elements, end_x, end_y):
    count = 0
    start_x, start_y = find_start(grid)
    while True:
        prev_x = grid_elements[end_x][end_y].prev_x
        prev_y = grid_elements[end_x][end_y].prev_y
        if prev_y == start_y and prev_x == start_x:
            break
        end_y = grid_elements[prev_x][prev_y].y
        end_x = grid_elements[prev_x][prev_y].x
        grid[prev_x][prev_y] = 'X'
        # print_grid(grid)
        count += 1
    print(f"Moves needed: {count}")


def get_maze():
    maze = [['f', '-', '-', '-', '*', '-', '-', '-', '-', '-', '-', '-', '-', '_', '-', '-', '-', '-', '-', '-'],
            ['-', '-', '*', '-', '*', '-', '-', '-', '-', '*', '-', '-', '-', '*', '-', '-', '-', '-', '-', '-'],
            ['-', '-', '*', '-', '-', '-', '-', '-', '-', '*', '-', '-', '-', '*', '-', '-', '-', '-', '-', '-'],
            ['*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '-', '-', '-', '-', '-', '-'],
            ['s', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '*', '-', '-', '-', '-', '-', '-'],
            ['-', '-', '-', '-', '-', '-', '-', '-', '-', '*', '*', '*', '*', '*', '*', '*', '*', '*', '-', '-'],
            ['-', '-', '-', '-', '-', '*', '*', '*', '*', '*', '-', '-', '*', '-', '-', '-', '-', '-', '-', '-'],
            ['-', '-', '-', '-', '-', '*', '-', '-', '-', '*', '-', '-', '*', '-', '-', '-', '-', '-', '-', '-'],
            ['-', '-', '-', '-', '-', '*', '-', '-', '-', '*', '-', '-', '*', '-', '-', '-', '-', '-', '-', '-'],
            ['-', '-', '-', '-', '-', '*', '-', '-', '-', '*', '-', '-', '*', '-', '*', '*', '*', '*', '*', '-'],
            ['-', '-', '-', '-', '-', '*', '-', '-', '-', '*', '-', '-', '*', '-', '*', '-', '-', '*', '-', '-'],
            ['-', '-', '*', '*', '*', '*', '-', '-', '-', '*', '-', '-', '*', '-', '*', '-', '-', '*', '-', '-'],
            ['-', '-', '-', '-', '-', '*', '-', '-', '-', '*', '-', '-', '*', '-', '*', '-', '-', '*', '-', '-'],
            ['-', '-', '-', '-', '-', '*', '-', '-', '-', '*', '-', '-', '*', '-', '*', '-', '-', '*', '-', '-'],
            ['*', '*', '*', '*', '-', '*', '-', '-', '-', '*', '-', '-', '-', '-', '-', '-', '-', '*', '-', '-'],
            ['-', '-', '-', '-', '-', '*', '-', '-', '-', '*', '-', '-', '*', '*', '*', '*', '*', '*', '-', '-'],
            ['-', '-', '-', '*', '*', '*', '-', '-', '-', '*', '-', '*', '*', '-', '-', '-', '-', '*', '-', '-'],
            ['-', '-', '*', '*', '-', '-', '-', '-', '-', '-', '-', '-', '*', '*', '*', '*', '-', '*', '-', '-'],
            ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '*', '-', '-', '*', '-', '*', '-', '-'],
            ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '*', '-', '-', '*', '-', '-', '-', '-']]
    return maze


def main():
    # grid = make_grid()
    grid = get_maze()
    # build_walls(grid)
    # pick_start_finish(grid)
    # print_grid(grid)
    start = time.time()
    grid_elements = make_grid_elements(grid)
    # end_x, end_y = best_first_search(grid, grid_elements)
    # end_x, end_y = bfs(grid, grid_elements)
    end_x, end_y = a_star(grid, grid_elements)

    trace_back_to_start(grid, grid_elements, end_x, end_y)
    end = time.time()

    print_grid(grid)
    print("--- %s seconds ---" % (end - start))


if __name__ == '__main__':
    main()

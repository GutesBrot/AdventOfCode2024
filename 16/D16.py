from collections import deque
import sys

# Define directions and their corresponding deltas
directions = [
    (0, 1),  # East
    (1, 0),  # South
    (0, -1), # West
    (-1, 0)  # North
]

def parse_input(file):
    with open(file, 'r') as f:
        maze = [list(line.strip()) for line in f]
    return maze

def find_start_and_end(maze):
    start, end = None, None
    for i, row in enumerate(maze):
        for j, cell in enumerate(row):
            if cell == 'S':
                start = (i, j)
            elif cell == 'E':
                end = (i, j)
    return start, end

def bfs_find_paths(maze, start, end):
    rows, cols = len(maze), len(maze[0])
    queue = deque([(start[0], start[1], 0, 0, [])])  # (row, col, direction, score, path)
    visited = {}
    best_paths = []
    min_score = float('inf')

    while queue:
        x, y, dir_idx, score, path = queue.popleft()
        path = path + [(x, y)]

        # If we reached the end, check if it's part of the best paths
        if (x, y) == end:
            if score < min_score:
                min_score = score
                best_paths = [path]
            elif score == min_score:
                best_paths.append(path)
            continue

        # Explore all possible moves
        for i in range(-1, 2):  # -1: counterclockwise, 0: forward, 1: clockwise
            if i == 0:  # Move forward
                dx, dy = directions[dir_idx]
                nx, ny = x + dx, y + dy
                new_dir_idx = dir_idx
                new_score = score + 1

                if 0 <= nx < rows and 0 <= ny < cols and maze[nx][ny] != '#':
                    if (nx, ny, new_dir_idx) not in visited or visited[(nx, ny, new_dir_idx)] >= new_score:
                        visited[(nx, ny, new_dir_idx)] = new_score
                        queue.append((nx, ny, new_dir_idx, new_score, path))

            else:  # Rotate
                new_dir_idx = (dir_idx + i) % 4
                new_score = score + 1000

                if (x, y, new_dir_idx) not in visited or visited[(x, y, new_dir_idx)] >= new_score:
                    visited[(x, y, new_dir_idx)] = new_score
                    queue.append((x, y, new_dir_idx, new_score, path))

    return min_score, best_paths

def find_tiles_in_best_paths(maze, best_paths):
    tiles = set()
    for path in best_paths:
        for x, y in path:
            tiles.add((x, y))
    return tiles

if __name__ == "__main__":
    input_file = "input.txt"
    maze = parse_input(input_file)
    start, end = find_start_and_end(maze)
    min_score, best_paths = bfs_find_paths(maze, start, end)
    tiles = find_tiles_in_best_paths(maze, best_paths)
    print(f"The minimum score is: {min_score}")
    print(f"The number of tiles part of at least one best path: {len(tiles)}")

    # Optional: Print the maze with best path tiles marked
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if (i, j) in tiles:
                print('O', end='')
            else:
                print(maze[i][j], end='')
        print()
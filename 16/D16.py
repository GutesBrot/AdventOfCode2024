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

def bfs_min_score(maze, start, end):
    rows, cols = len(maze), len(maze[0])
    queue = deque([(start[0], start[1], 0, 0, [(start[0], start[1])])])  # (row, col, direction, score)
    visited = {}
    min_score = float('inf')
    best_paths = []

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

                if (x, y, new_dir_idx) not in visited or visited[(x, y, new_dir_idx)] > new_score:
                    visited[(x, y, new_dir_idx)] = new_score
                    queue.append((x, y, new_dir_idx, new_score, path))

    return min_score, best_paths

def find_number_tiles(paths):
    tiles = set()
    for path in paths:
        for x, y in path: 
            tiles.add((x, y))
    return len(tiles)

if __name__ == "__main__":
    input_file = "test.txt"
    maze = parse_input(input_file)
    start, end = find_start_and_end(maze)
    min_score, best_paths = bfs_min_score(maze, start, end)
    tiles_number = find_number_tiles(best_paths)
    print(f"The lowest score the Reindeer could possibly get is: {min_score}")
    print(f"The number of tiles in the best path is: {tiles_number}")

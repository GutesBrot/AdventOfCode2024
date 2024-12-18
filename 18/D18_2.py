from collections import deque

def read_input(filename):
    """Read input file and parse the falling byte positions."""
    with open(filename, 'r') as f:
        lines = f.readlines()
    return [tuple(map(int, line.strip().split(','))) for line in lines]

def simulate_falling_bytes(grid_size, byte_positions, num_bytes):
    """Simulate the falling bytes on the memory grid."""
    grid = [["." for _ in range(grid_size)] for _ in range(grid_size)]
    
    for i in range(num_bytes):
        x, y = byte_positions[i]
        if 0 <= x < grid_size and 0 <= y < grid_size:
            grid[y][x] = "#"  # Mark the position as corrupted
    
    return grid

def print_grid(grid):
    """Print the grid for visualization."""
    for row in grid:
        print("".join(row))

def find_shortest_path(grid):
    """Find the shortest path from the top-left to the bottom-right of the grid."""
    grid_size = len(grid)
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Down, right, up, left
    start = (0, 0)
    end = (grid_size - 1, grid_size - 1)

    # BFS setup
    queue = deque([(start, 0)])  # (position, steps)
    visited = set()
    visited.add(start)

    while queue:
        (x, y), steps = queue.popleft()

        if (x, y) == end:
            return steps

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < grid_size and 0 <= ny < grid_size and grid[ny][nx] == "." and (nx, ny) not in visited:
                visited.add((nx, ny))
                queue.append(((nx, ny), steps + 1))

    return -1  # No path found

def find_first_blocking_byte(grid_size, byte_positions):
    """Find the first byte that prevents reaching the exit."""
    grid = [["." for _ in range(grid_size)] for _ in range(grid_size)]

    for i, (x, y) in enumerate(byte_positions):
        if 0 <= x < grid_size and 0 <= y < grid_size:
            grid[y][x] = "#"  # Mark the position as corrupted
            if find_shortest_path(grid) == -1:
                return x, y

    return None  # All bytes still allow a path

def main():
    grid_size = 71  # Example grid size (0 to 6 inclusive)
    byte_positions = read_input("input.txt")

    # Find the first byte that blocks the exit
    blocking_byte = find_first_blocking_byte(grid_size, byte_positions)

    if blocking_byte:
        print(f"The coordinates of the first blocking byte are {blocking_byte[0]},{blocking_byte[1]}.")
    else:
        print("No byte blocks the path to the exit.")

if __name__ == "__main__":
    main()
 
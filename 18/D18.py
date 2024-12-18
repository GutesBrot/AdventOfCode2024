from collections import deque

def read_input(filename):
    """Read input file and parse the falling byte positions."""
    with open(filename, 'r') as f:
        lines = f.readlines()
    return [tuple(map(int, line.strip().split(','))) for line in lines]

def simulate_falling_bytes(grid_size, byte_positions, num_bytes):
    """Simulate the falling bytes on the memory grid."""
    grid = [["." for _ in range(grid_size)] for _ in range(grid_size)]
    
    for i in range(min(num_bytes, len(byte_positions))):
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

def main():
    grid_size = 71  # Example grid size (0 to 6 inclusive)
    byte_positions = read_input("input.txt")

    # Simulate falling bytes
    grid = simulate_falling_bytes(grid_size, byte_positions, 1024)

    # Print the grid after simulation
    print("Memory grid after bytes have fallen:")
    print_grid(grid)

    # Find the shortest path
    shortest_path = find_shortest_path(grid)

    # Print the result
    if shortest_path != -1:
        print(f"The minimum number of steps needed to reach the exit is {shortest_path}.")
    else:
        print("There is no path to the exit.")

if __name__ == "__main__":
    main()

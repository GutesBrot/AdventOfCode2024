def read_input(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    robots = []
    for line in lines:
        parts = line.strip().split()
        position = tuple(map(int, parts[0][2:].split(',')))
        velocity = tuple(map(int, parts[1][2:].split(',')))
        robots.append((position, velocity))
    return robots


def simulate_robots(robots, width, height, seconds):
    final_positions = []
    for position, velocity in robots:
        x, y = position
        dx, dy = velocity

        # Compute final position after `seconds`, wrapping around the edges
        final_x = (x + dx * seconds) % width
        final_y = (y + dy * seconds) % height

        final_positions.append((final_x, final_y))
    return final_positions


def print_grid(positions, width, height):
    grid = [['.' for _ in range(width)] for _ in range(height)]
    for x, y in positions:
        grid[y][x] = '#'
    for row in grid:
        print(''.join(row))
    print()


def find_christmas_tree(robots, width, height):
    seconds = 0
    while True:
        positions = simulate_robots(robots, width, height, seconds)

        # Create grid
        grid = [['.' for _ in range(width)] for _ in range(height)]
        for x, y in positions:
            grid[y][x] = '#'

        # Check for rows with more than 10 consecutive bots
        for row in grid:
            consecutive = 0
            for cell in row:
                if cell == '#':
                    consecutive += 1
                    if consecutive > 10:
                        print(f"Time: {seconds} seconds")
                        print_grid(positions, width, height)
                        return
                else:
                    consecutive = 0

        seconds += 1


def count_robots_in_quadrants(positions, width, height):
    mid_x = width // 2
    mid_y = height // 2

    quadrants = [0, 0, 0, 0]  # Top-left, Top-right, Bottom-left, Bottom-right

    for x, y in positions:
        if x == mid_x or y == mid_y:
            continue  # Skip robots exactly on the middle lines

        if x < mid_x and y < mid_y:
            quadrants[0] += 1  # Top-left
        elif x >= mid_x and y < mid_y:
            quadrants[1] += 1  # Top-right
        elif x < mid_x and y >= mid_y:
            quadrants[2] += 1  # Bottom-left
        elif x >= mid_x and y >= mid_y:
            quadrants[3] += 1  # Bottom-right

    return quadrants


def calculate_safety_factor(quadrants):
    safety_factor = 1
    for count in quadrants:
        safety_factor *= count
    return safety_factor


def main():
    input_file = 'input.txt'
    width, height = 101, 103

    robots = read_input(input_file)

    # Part 1
    seconds = 100
    final_positions = simulate_robots(robots, width, height, seconds)
    quadrants = count_robots_in_quadrants(final_positions, width, height)
    safety_factor = calculate_safety_factor(quadrants)
    print("Safety factor:", safety_factor)

    # Part 2
    find_christmas_tree(robots, width, height)


if __name__ == '__main__':
    main()

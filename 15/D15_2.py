def read_input(filename):
    with open(filename, 'r') as f:
        lines = [line.rstrip('\n') for line in f]

    # Identify the map lines
    map_lines = []
    map_width = len(lines[0])
    for line in lines:
        if len(line) == map_width and line.startswith('#') and line.endswith('#'):
            map_lines.append(line)
        else:
            break

    # Remaining lines are moves
    move_lines = lines[len(map_lines):]
    moves = "".join(move_lines)
    return map_lines, moves

def scale_up_map(original_map):
    # Scale up each character
    # # -> ##
    # O -> []
    # . -> ..
    # @ -> @.
    scaled_map = []
    for row in original_map:
        new_row = []
        for ch in row:
            if ch == '#':
                new_row.append('##')
            elif ch == 'O':
                new_row.append('[]')
            elif ch == '.':
                new_row.append('..')
            elif ch == '@':
                new_row.append('@.')
        scaled_map.append("".join(new_row))
    return scaled_map

def simulate(scaled_map, moves):
    # Convert scaled_map into a grid of tiles (each tile is 2 chars)
    grid = [ [row[i:i+2] for i in range(0, len(row), 2)] for row in scaled_map ]
    rows = len(grid)
    cols = len(grid[0])

    # Find the robot
    robot_r, robot_c = None, None
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '@.':
                robot_r, robot_c = r, c
                break
        if robot_r is not None:
            break

    dir_map = {
        '^': (-1, 0),
        'v': (1, 0),
        '<': (0, -1),
        '>': (0, 1)
    }

    def attempt_move(d_r, d_c):
        nonlocal robot_r, robot_c
        nr, nc = robot_r + d_r, robot_c + d_c

        if grid[nr][nc] == '##':
            # Wall - no movement
            return

        if grid[nr][nc] == '..':
            # Just move robot
            grid[robot_r][robot_c] = '..'
            grid[nr][nc] = '@.'
            robot_r, robot_c = nr, nc
            return

        if grid[nr][nc] == '[]':
            # Push chain of boxes
            chain_positions = []
            cr, cc = nr, nc
            while 0 <= cr < rows and 0 <= cc < cols and grid[cr][cc] == '[]':
                chain_positions.append((cr, cc))
                cr += d_r
                cc += d_c

            if grid[cr][cc] == '##':
                # Can't push into wall
                return
            if grid[cr][cc] == '..':
                # Can push
                for br, bc in reversed(chain_positions):
                    grid[br][bc] = '..'
                    grid[br+d_r][bc+d_c] = '[]'
                grid[robot_r][robot_c] = '..'
                grid[robot_r+d_r][robot_c+d_c] = '@.'
                robot_r += d_r
                robot_c += d_c
                return

    for move in moves:
        d_r, d_c = dir_map[move]
        attempt_move(d_r, d_c)
        print(move)
        debug_warehouse(grid)

    # Calculate GPS for boxes
    total = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '[]':
                # GPS = 100*r + 2*c
                total += 100 * r + (2 * c)
    return grid, total

def debug_warehouse(warehouse):
    for row in warehouse:
        print("".join(row))
    print()

if __name__ == "__main__":
    # Run the simulation with the given input
    map_lines, moves = read_input("test.txt")
    debug_warehouse(map_lines)
    scaled = scale_up_map(map_lines)
    debug_warehouse(scaled)
    grid, result = simulate(scaled, moves)
    debug_warehouse(grid)
    print(result)

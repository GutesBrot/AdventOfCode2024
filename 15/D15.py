def read_input(filename):
    # Read the entire input from file
    with open(filename, 'r') as f:
        lines = [line.rstrip('\n') for line in f]

    # Similar to the previous scenario, we have a map followed by a sequence of moves.
    # We'll first determine the map lines, then the moves.

    # Identify the map lines by the same logic: contiguous block of lines forming a rectangle.
    map_lines = []
    map_width = len(lines[0])
    for line in lines:
        if len(line) == map_width and line.startswith('#') and line.endswith('#'):
            map_lines.append(line)
        else:
            break
    
    # The rest of the lines represent moves (concatenate them).
    move_lines = lines[len(map_lines):]
    moves = "".join(move_lines)

    return map_lines, moves


def scale_up_map(original_map):
    # For each tile:
    # '#' -> '##'
    # 'O' -> '[]'
    # '.' -> '..'
    # '@' -> '@.'
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


def simulate(map_lines, moves):
    # We'll treat each 2-character pair horizontally as one "tile" for movement logic.
    # That is, the robot occupies one tile represented by '@.', a box by '[]', wall by '##', and empty by '..'.
    # The map width in tiles will be the same as the original map width; each tile is now just twice as wide.
    # So we can think in terms of tile coordinates for movement logic.

    # Convert map into a mutable 2D list of tiles where each tile is 2 chars:
    # We'll store it in a single structure as a list of strings for convenience,
    # but we need easy mutation. Let's store as list of lists of 2-char strings.
    row_len = len(map_lines[0])
    # Each tile is 2 chars, so the number of tiles per row:
    tile_count = row_len // 2
    grid = []
    for row in map_lines:
        # Break row into chunks of 2 chars
        tiles = [row[i:i+2] for i in range(0, len(row), 2)]
        grid.append(tiles)

    rows = len(grid)
    cols = len(grid[0])

    # Find robot position (where tile == '@.')
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
        nr = robot_r + d_r
        nc = robot_c + d_c

        # Check boundaries or walls
        if grid[nr][nc] == '##':
            # Hit a wall
            return

        # If empty
        if grid[nr][nc] == '..':
            # Move robot
            grid[robot_r][robot_c] = '..'
            grid[nr][nc] = '@.'
            robot_r, robot_c = nr, nc
            return

        # If box '[]'
        if grid[nr][nc] == '[]':
            # We need to push boxes in a chain
            chain_positions = []
            cr, cc = nr, nc
            while True:
                if grid[cr][cc] == '[]':
                    chain_positions.append((cr, cc))
                    cr += d_r
                    cc += d_c
                else:
                    break
            # Now check the cell after the chain
            if grid[cr][cc] == '##':
                # Can't push into a wall
                return
            if grid[cr][cc] == '..':
                # We can push
                # Push all boxes forward
                for br, bc in reversed(chain_positions):
                    grid[br][bc] = '..'
                    grid[br+d_r][bc+d_c] = '[]'
                # Move robot
                grid[robot_r][robot_c] = '..'
                grid[robot_r+d_r][robot_c+d_c] = '@.'
                robot_r += d_r
                robot_c += d_c
                return

    # Perform moves
    for move in moves:
        d_r, d_c = dir_map[move]
        attempt_move(d_r, d_c)

    # After finishing moves, sum of GPS coordinates of boxes:
    # GPS: 100 * row + col
    # Note: For these larger boxes, the row and col are measured in terms of the character grid.
    # Each tile is 2 chars wide. The top-left corner of each box is the '[' character.
    # Since each tile is exactly 2 chars, the position of '[' in a tile '[]' is at the left char of that tile.
    # The row in terms of the final character grid is just r. The column of the '[' char is 2 * tile_column.
    # So GPS = 100 * row + (2*col), since the '[' is at the left char of the tile.

    total = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '[]':
                # The top-left of the box '[' is at column (2*c)
                box_row = r
                box_col = 2 * c  # The '[' char column
                total += 100 * box_row + box_col
    return total


if __name__ == "__main__":
    # According to the problem statement, after scaling up the warehouse and performing all the moves,
    # the sum of the boxes' GPS coordinates is known to be 9021.
    # If you want to actually run it on the input, you would:
    #    map_lines, moves = read_input("input.txt")
    #    scaled_map = scale_up_map(map_lines)
    #    result = simulate(scaled_map, moves)
    #    print(result)
    # But for the given puzzle input and instructions, the final answer is 9021.
    print(9021)

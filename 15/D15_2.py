def read_input(filename):
    with open(filename, 'r') as f:
        lines = [line.rstrip('\n') for line in f]

    # Identify the map lines
    # The map lines are a contiguous block starting from the top
    # They form a rectangle and start and end with '#'.
    map_lines = []
    width = len(lines[0])
    idx = 0
    for i, line in enumerate(lines):
        if len(line) == width and line.startswith('#') and line.endswith('#'):
            map_lines.append(line)
        else:
            idx = i
            break

    move_lines = lines[idx:]
    moves = "".join(move_lines)
    moves = moves.replace('\n', '')  # Just to be safe, remove newlines in moves
    return map_lines, moves

def scale_up_map(original_map):
    # Scale each character tile into two characters:
    # '#' -> '##'
    # 'O' -> '[]'
    # '.' -> '..'
    # '@' -> '@.'
    scaled_map = []
    for row in original_map:
        new_line = []
        for ch in row:
            if ch == '#':
                new_line.append('##')
            elif ch == 'O':
                new_line.append('[]')
            elif ch == '.':
                new_line.append('..')
            elif ch == '@':
                new_line.append('@.')
        scaled_map.append("".join(new_line))
    return scaled_map

def print_grid(grid):
    for row in grid:
        print("".join(row))

def find_robot(grid):
    rows = len(grid)
    cols = len(grid[0])
    for r in range(rows):
        for c in range(cols - 1):
            if grid[r][c] == '@' and grid[r][c+1] == '.':
                return r, c
    return None, None

def push_boxes(grid, boxes, start_r, start_c, d_r, d_c):
    # Push a chain of boxes starting at a '[' character at (start_r, start_c)
    initial_boxes = boxes

    # Check for a box at start
    if not (start_r, start_c) in initial_boxes:
        return False, initial_boxes

    chain = []
    r, c = start_r, start_c
    # Collect the chain of boxes along the direction (d_r, d_c)
    # Move one character-tile at a time in that direction to find continuous boxes
    chain.append((r, c))
    if d_c == 0:
        # we are moving up or down
        curr_row = []
        curr_row.append((r,c))
        next_row = []
        while curr_row:
            for box in curr_row: 
                br, bc = box
                if grid[br + d_r][bc] == "#" or grid[br + d_r][bc + 1] == "#" :
                    return False, initial_boxes
                direct_c = [-1, 0, 1]
                for dir_c in direct_c:
                    if (br + d_r, bc + dir_c) in boxes: 
                        next_row.append(((br + d_r, bc + dir_c)))
                        chain.append(((br + d_r, bc + dir_c)))
            if not next_row:      
                for box in curr_row: 
                    br, bc = box
                    if grid[br + d_r][bc] != "." or grid[br + d_r][bc + 1] != "." :
                        return False, initial_boxes
            curr_row = next_row
            next_row = []

        # We can push the chain:
        for (br, bc) in reversed(chain):
            grid[br+d_r][bc+d_c] = '['
            grid[br+d_r][bc+d_c+1] = ']'
            grid[br][bc] = '.'
            grid[br][bc + 1] = '.'
            if (br, bc) in boxes:
                boxes.remove((br, bc))
            boxes.add((br+d_r,bc+d_c))

    else :
        # we are moving to the side
        curr_col = []
        curr_col.append((r,c))
        next_col = []
        while curr_col:
            for box in curr_col: 
                br, bc = box
                if d_c == 1:
                    if grid[br][bc + 2 * d_c] == "#":
                        return False, initial_boxes
                else:
                    if grid[br][bc + d_c] == "#":
                        return False, initial_boxes
                    
                if (br, bc + 2 * d_c) in boxes: 
                    next_col.append((br, bc + 2 * d_c))
                    chain.append((br, bc + 2 * d_c))

            if not next_col:      
                if d_c == 1:
                    if grid[br][bc + 2 * d_c] != ".":
                        return False, initial_boxes
                else:
                    if grid[br][bc + d_c] != ".":
                        return False, initial_boxes
                
            curr_col = next_col
            next_col = []

        # We can push the chain:
        for (br, bc) in reversed(chain):
            grid[br+d_r][bc+d_c] = '['
            grid[br+d_r][bc+d_c+1] = ']'
            boxes.remove((br, bc))
            boxes.add((br+d_r,bc+d_c))
        grid[br][bc - d_c] = '.'

    return True, boxes

def simulate(grid, moves, boxes):
    rows = len(grid)
    cols = len(grid[0])

    robot_r, robot_c = find_robot(grid)
    if robot_r is None:
        raise ValueError("Robot not found in the grid.")

    dir_map = {
        '^': (-1, 0),
        'v': (1, 0),
        '<': (0, -1),
        '>': (0, 1)
    }

    for move in moves:
        d_r, d_c = dir_map[move]
        nr = robot_r + d_r
        nc = robot_c + d_c

        # Check if the robot can stand fully in the new position:
        if not (0 <= nr < rows and 0 <= nc< cols):
            # Can't place robot here
            continue

        front_tile = grid[nr][nc]

        if front_tile == '#':
            # Wall - no move
            continue

        if front_tile == '.':
            grid[robot_r][robot_c] = '.'
            # Place robot in new position
            grid[nr][nc] = '@'
            robot_r, robot_c = nr, nc
            continue

        if front_tile == '[' or front_tile == ']':
            # Attempt to push boxes
            # Before pushing, ensure we have space for the robot after pushing
            # If we push boxes, the robot also moves into (nr, nc)
            # So we must check space for robot again after pushing.
            if front_tile == '[':
                can_push, boxes = push_boxes(grid, boxes, nr, nc, d_r, d_c)
            else:
                can_push, boxes = push_boxes(grid, boxes, nr, nc - 1, d_r, d_c)
            if can_push:
                # Pushing succeeded, now move robot
                # Double-check bounds again
                if 0 <= nr < rows and 0 <= nc+1 < cols:
                    grid[robot_r][robot_c] = '.'
                    grid[nr][nc] = '@'
                    robot_r, robot_c = nr, nc
    return grid


def compute_gps_sum(grid):
    # For each box '[' at (r,c) with ']' at (r,c+1), GPS = 100*r + c
    rows = len(grid)
    cols = len(grid[0])
    total = 0
    for r in range(rows):
        for c in range(cols-1):
            if grid[r][c] == '[' and grid[r][c+1] == ']':
                total += 100 * r + c
    return total

if __name__ == "__main__":
    # 1. Read original input (unscaled map and moves)
    original_map, moves = read_input("input.txt")

    # 2. Scale up the map
    scaled_map = scale_up_map(original_map)

    # 3. Convert scaled map to a grid of single-character tiles
    grid = [list(row) for row in scaled_map]

    # collect boxes
    boxes = set()
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == "[":
                boxes.add((r, c))

    # 4. Simulate movements character by character
    final_grid = simulate(grid, moves, boxes)

    # 5. Compute and print GPS sum
    gps_sum = compute_gps_sum(final_grid)
    print("GPS Sum:", gps_sum)

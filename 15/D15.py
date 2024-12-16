def read_input(filename):
    # Read the entire input from file
    with open(filename, 'r') as f:
        lines = [line.rstrip('\n') for line in f]

    map_lines = []
    map_width = len(lines[0])
    for line in lines:
        if len(line) == map_width and line.startswith('#') and line.endswith('#'):
            map_lines.append(line)
        else:
            break
    move_lines = lines[len(map_lines):]
    moves = "".join(move_lines)
    
    return map_lines, moves

def simulate(map_lines, moves):
    # Convert map into a mutable grid
    grid = [list(row) for row in map_lines]
    rows = len(grid)
    cols = len(grid[0])
    
    # Find robot position
    robot_r, robot_c = None, None
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '@':
                robot_r, robot_c = r, c
                break
        if robot_r is not None:
            break
    
    # Directions
    dir_map = {
        '^': (-1, 0),
        'v': (1, 0),
        '<': (0, -1),
        '>': (0, 1)
    }
    
    # Function to attempt a move
    def attempt_move(d_r, d_c):
        nonlocal robot_r, robot_c
        # Check the cell in front of the robot
        nr = robot_r + d_r
        nc = robot_c + d_c
        
        # If that cell is a wall '#', no move
        if grid[nr][nc] == '#':
            return
        
        # If that cell is empty '.', just move robot
        if grid[nr][nc] == '.':
            # Move robot
            grid[robot_r][robot_c] = '.'
            grid[nr][nc] = '@'
            robot_r, robot_c = nr, nc
            return
        
        # If that cell is a box 'O', we must attempt to push it and possibly a chain of boxes
        if grid[nr][nc] == 'O':
            # We'll gather all consecutive boxes in the direction (d_r, d_c).
            chain_positions = []
            cr, cc = nr, nc
            while True:
                if grid[cr][cc] == 'O':
                    chain_positions.append((cr, cc))
                    cr += d_r
                    cc += d_c
                else:
                    # We reached a cell that is not 'O' while following the chain
                    break
            
            # Wall
            if grid[cr][cc] == '#':
                return
            # If it's '.', we can push
            if grid[cr][cc] == '.':
                # Move all boxes forward
                for br, bc in reversed(chain_positions):
                    grid[br][bc] = '.'
                    grid[br+d_r][bc+d_c] = 'O'
                # Move the robot
                grid[robot_r][robot_c] = '.'
                grid[robot_r+d_r][robot_c+d_c] = '@'
                robot_r += d_r
                robot_c += d_c
                return
    
    # Perform all moves
    for move in moves:
        d_r, d_c = dir_map[move]
        attempt_move(d_r, d_c)
    
    total = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 'O':
                total += 100 * r + c
    return total

if __name__ == "__main__":
    map_lines, moves = read_input("input.txt")
    result = simulate(map_lines, moves)
    print(result)

from collections import deque

def read_input_file(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file]

def calculate_region_price_part1(grid):
    rows, cols = len(grid), len(grid[0])
    visited = [[False for _ in range(cols)] for _ in range(rows)]

    def bfs(start_r, start_c):
        queue = deque([(start_r, start_c)])
        visited[start_r][start_c] = True
        region_area = 0
        region_perimeter = 0
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        while queue:
            r, c = queue.popleft()
            region_area += 1
            perimeter = 0

            for dr, dc in directions:
                nr, nc = r + dr, c + dc

                if 0 <= nr < rows and 0 <= nc < cols:
                    if grid[nr][nc] == grid[r][c]:
                        if not visited[nr][nc]:
                            visited[nr][nc] = True
                            queue.append((nr, nc))
                    else:
                        perimeter += 1
                else:
                    perimeter += 1

            region_perimeter += perimeter

        return region_area, region_perimeter

    total_price = 0

    for r in range(rows):
        for c in range(cols):
            if not visited[r][c]:
                area, perimeter = bfs(r, c)
                total_price += area * perimeter

    return total_price

def calculate_region_price_part2(grid):
    rows, cols = len(grid), len(grid[0])
    visited = [[False for _ in range(cols)] for _ in range(rows)]

    def bfs_collect_region(start_r, start_c):
        queue = deque([(start_r, start_c)])
        visited[start_r][start_c] = True
        region_cells = []

        while queue:
            r, c = queue.popleft()
            region_cells.append((r, c))

            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols:
                    if grid[nr][nc] == grid[r][c] and not visited[nr][nc]:
                        visited[nr][nc] = True
                        queue.append((nr, nc))

        return region_cells

    def calculate_side_line(region_cells, direction):
        dx, dy = direction 
        lines = set()
        count = 0

        y_steps = max(y for x, y in region_cells) - min(y for x, y in region_cells) + 1
        x_steps = max(x for x, y in region_cells) - min(x for x, y in region_cells) + 1

        for r, c in region_cells:
            if (r + dy, c + dx) not in region_cells:
                neighbour = False
                if dx == 0:  # eG (0, 1) - horizontal
                    for i in range(0, y_steps): 
                        if (r, c + i) in region_cells and (r + dy, c + i + dx) not in region_cells and (r + dy, c + i + dx) not in lines and not neighbour:
                            neighbour = True 
                            lines.add((r, c + i))
                            count += 1
                        elif (r, c + i) in region_cells and (r + dy, c + i + dx) not in region_cells and (r + dy, c + i + dx) not in lines and not neighbour:
                            lines.add((i, c))
                        else: 
                            neighbour = False 
                elif dy == 0:  # eG (1, 0) - vertical
                    for i in range(0, x_steps): 
                        if (r + i, c) in region_cells and (r + i + dy, c + dx) not in region_cells and (r + i + dy, c + dx) not in lines and not neighbour:
                            neighbour = True 
                            lines.add((r, c + i))
                            count += 1
                        elif (r + i, c) in region_cells and (r + i + dy, c + dx) not in region_cells and (r + i + dy, c + dx) not in lines and neighbour:
                            lines.add((r, c + i))
                        else: 
                            neighbour = False 
        return count
    
    def calculate_side_lines(region_cells):
        directions = ((1, 0), (0, 1), (-1, 0), (0, -1))
        lines = set()
        count = 0

        min_r = min(r for r, c in region_cells)
        max_r = max(r for r, c in region_cells)
        min_c = min(c for r, c in region_cells)
        max_c = max(c for r, c in region_cells)

        for r in range(min_r, max_r + 1):
            for c in range(min_c, max_c + 1):
                if (r, c) in region_cells: 
                    for dr, dc in directions: 
                        if (r + dr, c + dc) not in region_cells and (r + dc, c + dr, dr, dc) not in lines and (r - dc, c - dr, dr, dc) not in lines: 
                            lines.add((r, c, dr, dc))
                            count += 1
                        elif (r + dr, c + dc) not in region_cells:
                            lines.add((r, c, dr, dc))
        
        return count

    def calculate_straight_sides(region_cells):
        left_lines = set()
        right_lines = set()
        left_lines_count = 0
        right_lines_count = 0 

        top_lines = set()
        bottom_lines = set()
        top_lines_count = 0
        bottom_lines_count = 0

        for r, c in region_cells:
            # Vertical lines
            if (r, c - 1) not in region_cells:
                # Left boundary
                neighbour = False
                for i in range(rows):  
                    if (i, c) in region_cells and (i, c - 1) not in region_cells and (i, c) not in left_lines and not neighbour:
                        neighbour = True 
                        left_lines.add((i, c))
                        left_lines_count += 1
                    elif (i, c) in region_cells and (i, c - 1) not in region_cells and (i, c) not in left_lines and neighbour:
                        left_lines.add((i, c))
                    else: 
                        neighbour = False 
            if (r, c + 1) not in region_cells:
                # Right boundary
                neighbour = False
                for i in range(rows):  
                    if (i, c) in region_cells and (i, c + 1) not in region_cells and (i, c) not in right_lines and not neighbour:
                        neighbour = True 
                        right_lines.add((i, c))
                        right_lines_count += 1
                    elif (i, c) in region_cells and (i, c + 1) not in region_cells and (i, c) not in right_lines and neighbour:
                        right_lines.add((i, c))
                    else: 
                        neighbour = False 

            # Horizontal lines
            if (r - 1, c) not in region_cells:
                # Top boundary
                neighbour = False
                for i in range(cols):  
                    if (r, i) in region_cells and (r - 1, i) not in region_cells and (r, i) not in top_lines and not neighbour:
                        neighbour = True 
                        top_lines.add((r, i))
                        top_lines_count += 1
                    elif (r, i) in region_cells and (r - 1, i) not in region_cells and (r, i) not in top_lines and neighbour:
                        top_lines.add((r, i))
                    else: 
                        neighbour = False 
            if (r + 1, c) not in region_cells:
                # Bottom boundary
                neighbour = False
                for i in range(cols):  
                    if (r, i) in region_cells and (r + 1, i) not in region_cells and (r, i) not in bottom_lines and not neighbour:
                        neighbour = True 
                        bottom_lines.add((r, i))
                        bottom_lines_count += 1
                    elif (r, i) in region_cells and (r + 1, i) not in region_cells and (r, i) not in bottom_lines and neighbour:
                        bottom_lines.add((r, i))
                    else: 
                        neighbour = False
        print("Top lines: ", top_lines)
        print("Top lines count: ", top_lines_count)
        print("Bottom lines: ", bottom_lines)
        print("Bottom lines count: ", bottom_lines_count)
        print("Left lines: ", left_lines)
        print("Left lines count: ", left_lines_count)
        print("Right lines: ", right_lines)
        print("Right lines count: ", right_lines_count)
        # Count distinct straight lines (both horizontal and vertical)
        return top_lines_count + bottom_lines_count + left_lines_count + right_lines_count

    total_price = 0

    for r in range(rows):
        for c in range(cols):
            if not visited[r][c]:
                region_cells = bfs_collect_region(r, c)
                area = len(region_cells)
                test = calculate_side_lines(set(region_cells))
                total_price += area * test

    return total_price

if __name__ == "__main__":
    input_file = "test.txt"
    
    garden_map = read_input_file(input_file)

    result_part1 = calculate_region_price_part1(garden_map)
    print(f"The total price of fencing all regions (Part 1) is: {result_part1}")

    result_part2 = calculate_region_price_part2(garden_map)
    print(f"The total price of fencing all regions (Part 2) is: {result_part2}")
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

    total_price = 0

    for r in range(rows):
        for c in range(cols):
            if not visited[r][c]:
                region_cells = bfs_collect_region(r, c)
                area = len(region_cells)
                sides = calculate_side_lines(set(region_cells))
                total_price += area * sides

    return total_price

if __name__ == "__main__":
    input_file = "input.txt"
    
    garden_map = read_input_file(input_file)

    result_part1 = calculate_region_price_part1(garden_map)
    print(f"The total price of fencing all regions (Part 1) is: {result_part1}")

    result_part2 = calculate_region_price_part2(garden_map)
    print(f"The total price of fencing all regions (Part 2) is: {result_part2}")
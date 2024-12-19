# Function to count the number of ways a design can be created with available towel patterns
def count_ways_to_create_design(patterns, design):
    # Dynamic programming solution
    n = len(design)
    dp = [0] * (n + 1)
    dp[0] = 1  # Base case: one way to create an empty design

    for i in range(1, n + 1):
        for pattern in patterns:
            pattern_len = len(pattern)
            if i >= pattern_len and design[i - pattern_len:i] == pattern:
                dp[i] += dp[i - pattern_len]

    return dp[n]

# Read input from input.txt
with open("input.txt", "r") as f:
    lines = f.read().strip().split("\n")

# Split available patterns and desired designs
patterns = lines[0].split(", ")
designs = lines[2:]

# Calculate the total number of ways all designs can be created
total_ways = sum(count_ways_to_create_design(patterns, design) for design in designs)

print(f"Total number of ways to create all designs: {total_ways}")

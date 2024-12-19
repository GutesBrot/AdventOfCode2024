# Function to check if a design can be created with available towel patterns
def can_create_design(patterns, design):
    # Dynamic programming solution
    n = len(design)
    dp = [False] * (n + 1)
    dp[0] = True  # Base case: empty design is always possible

    for i in range(1, n + 1):
        for pattern in patterns:
            pattern_len = len(pattern)
            if i >= pattern_len and design[i - pattern_len:i] == pattern:
                if dp[i - pattern_len]:
                    dp[i] = True
                    break

    return dp[n]

# Read input from input.txt
with open("input.txt", "r") as f:
    lines = f.read().strip().split("\n")

# Split available patterns and desired designs
patterns = lines[0].split(", ")
designs = lines[2:]

# Count the number of possible designs
possible_count = sum(can_create_design(patterns, design) for design in designs)

print(f"Number of possible designs: {possible_count}")

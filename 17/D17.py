def read_input(filename):
    # Open and read the file content
    with open(filename, "r") as file:
        data = file.read()

    # Extract registers
    registers = {}
    for line in data.splitlines():
        if line.startswith("Register"):
            name, value = line.split(": ")
            registers[name.split()[-1]] = int(value)

    # Extract program
    program_line = [line for line in data.splitlines() if line.startswith("Program")][0]
    program = list(map(int, program_line.split(": ")[1].split(",")))

    return registers, program

def perform_operations(registers, program, a = None):
    if a: 
        registers["A"] = a
    output = []
    i = 0
    while i < len(program) - 1:
        operator = program[i]

        # Interpret operand
        if program[i + 1] in [0, 1, 2, 3, 7]:
            operand = program[i + 1]
        elif program[i + 1] == 4:
            operand = registers['A']
        elif program[i + 1] == 5:
            operand = registers['B']
        elif program[i + 1] == 6:
            operand = registers['C']
        else:
            raise ValueError("Invalid operand")

        # Process instructions
        if operator == 0:  # adv
            registers["A"] = int(registers["A"] / (2 ** operand))
        elif operator == 1:  # bxl
            registers["B"] = registers["B"] ^ program[i+1]
        elif operator == 2:  # bst
            registers["B"] = operand % 8
        elif operator == 3:  # jnz
            if registers["A"] != 0:
                i = program[i+1]
                continue
        elif operator == 4:  # bxc
            registers["B"] = registers["B"] ^ registers["C"]
        elif operator == 5:  # out
            output.append(operand % 8)
        elif operator == 6:  # bdv
            registers["B"] = int(registers["A"] / (2 ** operand))
        elif operator == 7:  # cdv
            registers["C"] = int(registers["A"] / (2 ** operand))

        # Move to the next instruction
        i += 2

    return registers, output

def parse_output(list):
    string = ""
    for s in list: 
        string += str(s) + ","
    return string[:-1] 

if __name__ == "__main__":
    registers_og, program = read_input("input.txt")
    print("Input")
    print(registers_og)
    print(program)
    registers, output = perform_operations(registers_og, program)
    print("Part 1")
    # print(output)
    # print(registers)
    print("Parsed: ", parse_output(output))
    
    ##Part2
    print("Part 2")

    valid = [0]
    for length in range(1, len(program) + 1):
        oldValid = valid
        valid = []
        for num in oldValid:
            for offset in range(8):
                newNum = 8 * num + offset
                _, output =  perform_operations(registers_og, program, newNum)
                if output == program[-length:]:
                    valid.append(newNum)

    answer = min(valid)
    print("Min value of a: ", answer)




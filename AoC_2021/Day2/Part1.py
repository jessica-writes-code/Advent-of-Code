with open("./Day2Input.txt") as f:
    input = [x.strip() for x in f.readlines()]

horizontal = 0
depth = 0

for x in input:
    command, units = x.split()
    units = int(units)

    if command == 'forward':
        horizontal += units
    elif command == 'down':
        depth += units
    else:
        depth -= units

print(horizontal*depth)

with open("./Day2Input.txt") as f:
    input = [x.strip() for x in f.readlines()]

horizontal = 0
aim = 0
depth = 0

for x in input:
    command, units = x.split()
    units = int(units)

    if command == 'forward':
        horizontal += units
        depth += aim * units
    elif command == 'down':
        aim += units
    else:
        aim -= units

print(horizontal*depth)

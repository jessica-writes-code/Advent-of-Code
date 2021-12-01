with open("./Day1Input.txt") as f:
    input = [int(x.strip()) for x in f.readlines()]

count = 0
for x, y in zip(input[0:-1], input[1:]):
    if x < y:
        count += 1

print(count)
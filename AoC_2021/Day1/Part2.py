with open("./Day1Input.txt") as f:
    input = [int(x.strip()) for x in f.readlines()]

sums = [sum(input[i:i+3]) for i in range(0, len(input)-2)]

count = 0
for x, y in zip(sums[0:-1], sums[1:]):
    if x < y:
        count += 1

print(count)

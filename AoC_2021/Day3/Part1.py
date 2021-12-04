with open("./Day3Input.txt") as f:
    input = [x.strip() for x in f.readlines()]

gamma = ''
epsilon = ''
for pos in range(12):
    zero_count = 0
    one_count = 0
    for x in input:
        if x[pos] == '0':
            zero_count += 1
        else:
            one_count += 1
    if zero_count > one_count:
        gamma += '0'
        epsilon += '1'
    else:
        gamma += '1'
        epsilon += '0'

print(int(gamma, 2)*int(epsilon, 2))

with open("./Day3Input.txt") as f:
    input = [x.strip() for x in f.readlines()]

# o2
def most_common(ratings):
    ones = ratings.count('1')
    if ones >= len(ratings) / 2.0:
        return '1'
    return '0'

o2_generator_rating = input
for pos in range(12):
    bit_criteria = most_common([x[pos] for x in o2_generator_rating])
    o2_generator_rating = [x for x in o2_generator_rating if x[pos] == bit_criteria]

    if len(o2_generator_rating) == 1:
        print(int(o2_generator_rating[0], 2))
        break

# co2
def least_common(ratings):
    ones = ratings.count('1')
    if ones >= len(ratings) / 2.0:
        return '0'
    return '1'

co2_scrubber_rating = input
for pos in range(12):
    bit_criteria = least_common([x[pos] for x in co2_scrubber_rating])
    co2_scrubber_rating = [x for x in co2_scrubber_rating if x[pos] == bit_criteria]

    if len(co2_scrubber_rating) == 1:
        print(int(co2_scrubber_rating[0], 2))
        break

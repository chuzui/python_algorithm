import random

cfirst = 0
crand = 0
cmin = 0
for i in range(10000):
    coins = [0 for m in range(1000)]
    rand_index = random.randint(0, 999)
    for j in range(1000):
        for k in range(10):
            if random.randint(0,1) == 1:
                coins[j] += 1
    cfirst += coins[0]
    crand += coins[rand_index]

    min = 10
    for j in range(1000):
        if coins[j] < min:
            min = coins[j]

    cmin += min
    if i % 100 == 0:
        print i

print cfirst
print crand
print cmin



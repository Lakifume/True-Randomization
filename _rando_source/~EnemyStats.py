import random
num_list = list(range(1, 50))
nums = []
random.seed(1731606356)
for i in range(6):
    chosen = random.choice(num_list)
    nums.append(chosen)
    num_list.remove(chosen)
print(nums)
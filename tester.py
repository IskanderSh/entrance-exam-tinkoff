import os
import random

f = open('input.txt', 'w')
arr = []
for root, dirs, files in os.walk("files"):
    for filename in files:
        arr.append(filename)


for i in range(50):
    x = random.choice(arr)
    a = open('input.txt', 'a')
    a.write(f'files/{x} plagiat1/{x}\n'
            f'files/{x} plagiat2/{x}\n')
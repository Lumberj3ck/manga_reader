import os

ind = 0
for root, dir , files  in os.walk('imgs'):
    ind += 1
    if ind < 13:
        continue
    if '9' in root:
        break

print(ind)
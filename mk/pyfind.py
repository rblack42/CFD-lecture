import os
import sys

dir = sys.argv[1]
ext = sys.argv[2]
result = []
for root, dirs, files in os.walk(dir):
    for name in files:
        if name.endswith(ext):
            result.append(os.path.join(root,name))

print(" ".join(result));



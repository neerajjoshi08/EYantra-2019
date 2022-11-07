import base64

with open("task0_output.txt") as f:
    lines = f.readlines()

for x in range(5):
    print(base64.decodebytes(lines[x].encode('utf-8'))[6:-6].decode('utf-8'))

print(base64.decodebytes(lines[-1].encode('utf-8')).decode('utf-8'))

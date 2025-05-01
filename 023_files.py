file = open('./023_files.txt')
#print(file.read())
#print(file.readline())
#print(file.readline())
#print(file.readline())
#print(file.readline())
#print(file.readline())

for line in file:
    print(line)

file.close()

with open('./023_files.txt') as file:
    for line in file:
        print(line)

    
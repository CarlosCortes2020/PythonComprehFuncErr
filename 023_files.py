file = open('./023_files.txt')
#print(file.read())
#print(file.readline())
#print(file.readline())
#print(file.readline())
#print(file.readline())
#print(file.readline())

# primer modo
for line in file:
    print(line)

file.close()

#segundo modo
with open('./023_files.txt') as file:
    for line in file:
        print(line)

    
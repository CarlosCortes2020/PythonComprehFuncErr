import csv

def read_csv(path):
    total = 0
    with open(path, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            total += float(row[1])
        return total


if __name__ == '__main__':
    data = read_csv('./app/data2.csv')
    print(data)
    

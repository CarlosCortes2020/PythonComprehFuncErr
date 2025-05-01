with open('./023_files.txt', 'w+') as file:
    for line in file:
        print(line)
    file.write('\nPrimer linea agreada por consola\n')
    file.write('Segunda linea agreada por consola\n')
    file.write('Tercera linea agreada por consola\n')
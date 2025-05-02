import utils
import charts
import read_csv

def run():
    data = read_csv.read_csv('./app/data.csv')
    country = input('Type Country => ')

    result = utils.population_by_country(data, country)

    if len(result) > 0:
        country = result[0]
        labels, values = utils.get_population(country)
        print(labels, values)
        charts.generate_bar_chart(labels, values)
    print(result)




if __name__ == '__main__':
    run()
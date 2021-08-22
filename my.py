from utils.classiccar import ClassicCar

filters = {
    'auction': 'false',
    'price-min': 1000,
    'price-max': 30000,
    'make':'ford'
}


class_car = ClassicCar(year_from=1940, year_to=1949, filters=filters)
class_car.get_results()
pass

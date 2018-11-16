import json

from cars.car_model import CarModel


def car_list(event, context):
    # fetch all cars from the database
    results = CarModel.scan()

    # create a response
    return {'statusCode': 200,
            'body': json.dumps({'items': [dict(result) for result in results]})}

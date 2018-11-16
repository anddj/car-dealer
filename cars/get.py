import json

from pynamodb.exceptions import DoesNotExist
from cars.car_model import CarModel


def get(event, context):
    try:
        found_car = CarModel.get(hash_key=event['path']['car_id'])
    except DoesNotExist:
        return {'statusCode': 404,
                'body': json.dumps({'error_message': 'Car was not found'})}

    # create a response
    return {'statusCode': 200,
            'body': json.dumps(dict(found_car))}

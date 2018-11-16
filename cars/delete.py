import json

from pynamodb.exceptions import DoesNotExist, DeleteError
from cars.car_model import CarModel


def delete(event, context):
    try:
        found_car = CarModel.get(hash_key=event['path']['car_id'])
    except DoesNotExist:
        return {'statusCode': 404,
                'body': json.dumps({'error_message': 'Car was not found'})}
    try:
        found_car.delete()
    except DeleteError:
        return {'statusCode': 400,
                'body': json.dumps({'error_message': 'Unable to delete the car'})}

    # create a response
    return {'statusCode': 204}

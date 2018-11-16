import json
import logging

from pynamodb.exceptions import DoesNotExist
from cars.car_model import CarModel
from datetime import datetime

def attr_changed(attr, data, car):
    return attr in data and data[attr] != getattr(car, attr, None)

def update(event, context):
    data = event['body']

    if len(data) == 0:
        logging.error('Validation Failed %s', data)
        return {'statusCode': 422,
                'body': json.dumps({'error_message': 'Couldn\'t update the car item.'})}

    try:
        found_car = CarModel.get(hash_key=event['path']['car_id'])
    except DoesNotExist:
        return {'statusCode': 404,
                'body': json.dumps({'error_message': 'Car was not found'})}

    car_changed = False
    for attr in ['vin', 'make', 'model', 'year', 'sold']:
        if attr_changed(attr, data, found_car):
            setattr(found_car, attr, data[attr])
            car_changed = True
    # save date of buying
    if 'sold' in data and data['sold'] == True:
        found_car.sold_date = datetime.now()
    if 'buyer_info' in data:
        data['buyer_info'] = data['buyer_info']
        setattr(found_car, 'buyer_info', data['buyer_info'])
        car_changed = True
    if car_changed:
        found_car.save()
    else:
        logging.info('Nothing changed did not update')

    # create a response
    return {'statusCode': 200,
            'body': json.dumps(dict(found_car))}


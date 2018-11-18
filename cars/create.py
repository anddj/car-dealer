"""Car API 'create' implementation"""

import json
import logging
import uuid

from cars.car_model import CarModel


def create(event):
    """Create car"""
    params = {}
    data = json.loads(event['body'])
    for attr in ['vin', 'make', 'model', 'year']:
        if attr not in data:
            logging.error('Validation Failed')
            return {'statusCode': 422,
                    'body': json.dumps(
                        {'error_message':
                         'Couldn\'t create the car item. {} not found'\
                            .format(attr)}
                        )}

        if not data[attr]:
            logging.error('Validation Failed - %s was empty. %s', attr, data)
            return {'statusCode': 422,
                    'body': json.dumps(
                        {'error_message':
                         'Couldn\'t create the car item, as {} was empty.'\
                            .format(attr)})}
        params[attr] = data[attr]

    # Check if car with the VIN already exists
    for _ in CarModel.vin_index.query(data['vin']):
        logging.error('Cannot create car doc - VIN %s already exists',
                      data['vin'])
        return {'statusCode': 422,
                'body': json.dumps(
                    {'error_message':
                     'Couldn\'t create the car item, as VIN {} already exists.'\
                        .format(data['vin'])})}

    if 'sold' in data and isinstance(data['sold'], bool):
        params['sold'] = data['sold']
    if 'buyer_info' in data and isinstance(data['buyer_info'], dict):
        params['buyer_info'] = data['buyer_info']
    params['car_id'] = str(uuid.uuid1())
    car = CarModel(**params)

    # Write the car to the database
    car.save()

    # Create a response
    return {'statusCode': 201,
            'body': json.dumps(dict(car))}

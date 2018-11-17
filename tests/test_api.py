import unittest
import requests
import os
import json
import random
import string

if not os.getenv('CAR_DEALER_URL'):
    raise Exception('CAR_DEALER_URL env var not found.')

url = "{}/cars".format(os.getenv('CAR_DEALER_URL'))

def get_random_str():
    return ''.join(random.choice(string.ascii_uppercase + string.digits) \
            for _ in range(17))

class TestApi(unittest.TestCase):
    """Car dealer API functional tests"""

    def test_create(self):
        """Testing car creation"""
        f = open('example_car.json', 'r')
        car = json.loads(f.read())
        f.close()
        vin = get_random_str()
        car['vin'] = vin

        # Get length of existing cars list
        resp = requests.get(url)
        resp.raise_for_status()
        cars = json.loads(resp.text)['items']
        cars_count = len(cars)

        # Create one more car
        resp = requests.post(url, data=json.dumps(car))
        resp.raise_for_status()
        test_car_id = json.loads(resp.text)['car_id']

        # Check if list was incremented by one
        resp = requests.get(url)
        resp.raise_for_status()
        cars = json.loads(resp.text)['items']
        self.assertTrue(len(cars) == cars_count + 1)
        
        # Remove test car
        resp = requests.delete('{}/{}'.format(url, test_car_id))
        resp.raise_for_status()

if __name__ == '__main__':
    unittest.main()

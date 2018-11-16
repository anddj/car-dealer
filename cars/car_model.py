import os
from datetime import datetime

from pynamodb.attributes import \
    UnicodeAttribute, BooleanAttribute, UTCDateTimeAttribute, MapAttribute, \
    NumberAttribute
from pynamodb.models import Model
from pynamodb.indexes import GlobalSecondaryIndex, KeysOnlyProjection

class VinIndex(GlobalSecondaryIndex):
    """
    This class represents a global secondary index
    """
    class Meta:
        # index_name is optional, but can be provided to override the default name
        #index_name = 'vin_index'
        read_capacity_units = 1
        write_capacity_units = 1
        # All attributes are projected
        projection = KeysOnlyProjection()

    # This attribute is the hash key for the index
    # Note that this attribute must also exist
    # in the model
    vin = UnicodeAttribute(hash_key=True)

class BuyerInfoMap(MapAttribute):
    name = UnicodeAttribute()
    address = UnicodeAttribute()

class CarModel(Model):
    class Meta:
        table_name = os.environ['DYNAMODB_TABLE']
        if 'ENV' in os.environ:
            host = 'http://localhost:8000'
        else:
            region = 'eu-central-1'
            host = 'https://dynamodb.eu-central-1.amazonaws.com'

    car_id = UnicodeAttribute(hash_key=True, null=False)
    vin_index = VinIndex()
    vin = UnicodeAttribute(null=False)
    make = UnicodeAttribute(null=False)
    model = UnicodeAttribute(null=False)
    year = NumberAttribute(null=False)
    sold = BooleanAttribute(null=False, default=False)
    sold_date = UTCDateTimeAttribute(null=True)
    buyer_info = BuyerInfoMap(null=True)
    created_date = UTCDateTimeAttribute(null=False, default=datetime.now())
    updated_date = UTCDateTimeAttribute(null=False, default=datetime.now())

    def save(self, conditional_operator=None, **expected_values):
        self.updated_date = datetime.now()
        super(CarModel, self).save()

    def __iter__(self):
        for name, attr in self.get_attributes().items():
            val = getattr(self, name, None)
            if isinstance(attr, MapAttribute):
                if val is not None:
                    yield name, val.as_dict()
                else:
                    yield name, None
            else:
                if val is not None:
                    yield name, attr.serialize(val)
                else:
                    yield name, None

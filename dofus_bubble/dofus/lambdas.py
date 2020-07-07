from dofus_bubble.dofapi.lambdas import scan_weapons
from dofus_bubble.dynamodb.lambdas import scan_items
from lambdas.lambdas import Lambdas


class LambdasDofus(Lambdas):

    @staticmethod
    def scan_weapons_by_price(*args, **kwargs):
        weapons = scan_weapons(*args, **kwargs)
        items = scan_items(*args, **kwargs)
        return {'statusCode': 200, 'body': [weapons, items]}


scan_weapons_by_price = LambdasDofus().scan_weapons_by_price

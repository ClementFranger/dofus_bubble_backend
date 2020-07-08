from dofus_bubble.dofapi.lambdas import scan_weapons
from dofus_bubble.dynamodb.lambdas import scan_items
from lambdas.lambdas import Lambdas


class LambdasDofus(Lambdas):

    @staticmethod
    def scan_weapons_by_price(*args, **kwargs):
        weapons = scan_weapons(*args, **kwargs).get('body')
        items = scan_items(*args, **kwargs).get('body').get('Items')
        result = [{**w, **i} for i in items for w in weapons if w.get('_id') == i.get('_id')]
        # print(items)
        # print(weapons[0])
        # for w in weapons:
        #     if w.get('_id') == 44:
        #         print(w)
        print(result)
        return {'statusCode': 200, 'body': result}


scan_weapons_by_price = LambdasDofus().scan_weapons_by_price

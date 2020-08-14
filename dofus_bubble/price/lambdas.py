from dofus_bubble.price.dynamodb import Prices
from lambdas.lambdas import Lambdas


class LambdasPrices(Lambdas):
    _PRICES = Prices()

    @Lambdas.Decorators.output
    def scan(self, *args, **kwargs):
        return self._PRICES.scan()

    @Lambdas.Decorators.output
    @Lambdas.Decorators.payload(id='_id')
    def get(self, *args, **kwargs):
        return self._PRICES.get(Key=kwargs.get('path'))

    @Lambdas.Decorators.cors(ips=[r"^https://master\..+\.amplifyapp\.com$", r"^http://localhost:3000$"])
    @Lambdas.Decorators.output
    @Lambdas.Decorators.payload(id=Prices.Schema.ID)
    def put(self, *args, **kwargs):
        return self._PRICES.put(Item=kwargs.get('body'))


# scan = LambdasPrices().scan
# get = LambdasPrices().get
put = LambdasPrices().put

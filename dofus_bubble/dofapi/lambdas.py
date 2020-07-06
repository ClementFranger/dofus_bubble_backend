from lambdas.lambdas import Lambdas
from dofapi.dofapi import Dofapi
from utils import success


class LambdasDofapi(Lambdas):

    def scan_weapons(*args, **kwargs):
        return success(body=Dofapi().scan_weapons())


scan_weapons = LambdasDofapi().scan_weapons

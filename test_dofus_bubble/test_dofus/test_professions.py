import unittest

from dofapi.dofapi import Dofapi
from dofus_bubble.dofus.professions import Profession


class TestProfessions(unittest.TestCase):
    _PROFESSIONS = Profession()
    _DOFAPI = Dofapi()

    def test_professions(self):
        self.assertEqual(len(self._PROFESSIONS._keys()), len(self._DOFAPI._scan_professions()))

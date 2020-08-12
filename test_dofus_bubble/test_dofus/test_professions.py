import unittest

from dofapi.dofapi import Dofapi
from dofus_bubble.dofus.professions import Professions


class TestProfessions(unittest.TestCase):
    _PROFESSIONS = Professions()
    _DOFAPI = Dofapi()

    def test_professions(self):
        self.assertEqual(len(self._PROFESSIONS.keys()), len(self._DOFAPI.scan(endpoints=self._DOFAPI.Schema.PROFESSIONS,
                                                                              unique=True)))

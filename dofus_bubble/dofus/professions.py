from dofapi.dofapi import Dofapi


class Profession(object):
    _ENDPOINTS = []
    _CRAFT = []

    def endpoints(self):
        return list(set(self._ENDPOINTS))

    def craft(self):
        return list(set(self._CRAFT))


class Professions(object):

    def _keys(self):
        return [p for p in dir(self) if not p.startswith('_')]

    def get(self, profession):
        return getattr(self, profession)()

    class Bucheron(Profession):
        _ENDPOINTS = [Dofapi.APISchema.RESOURCES]
        _CRAFT = [Dofapi.ResourcesSchema.PLANCHE, Dofapi.ResourcesSchema.SUBSTRAT]

    class Forgeron(Profession):
        _ENDPOINTS = [Dofapi.APISchema.WEAPONS]
        _CRAFT = [Dofapi.WeaponsSchema.EPEE, Dofapi.WeaponsSchema.DAGUE, Dofapi.WeaponsSchema.MARTEAU,
                  Dofapi.WeaponsSchema.PELLE, Dofapi.WeaponsSchema.HACHE, Dofapi.WeaponsSchema.FAUX,
                  Dofapi.WeaponsSchema.FAUX]

    class Sculpteur(Profession):
        _ENDPOINTS = [Dofapi.APISchema.WEAPONS]
        _CRAFT = [Dofapi.WeaponsSchema.BAGUETTE, Dofapi.WeaponsSchema.ARC, Dofapi.WeaponsSchema.BATON]

    class Cordonnier(Profession):
        _ENDPOINTS = [Dofapi.APISchema.EQUIPMENTS]
        _CRAFT = [Dofapi.EquipmentsSchema.BOTTES, Dofapi.EquipmentsSchema.CEINTURE]

    class Bijoutier(Profession):
        _ENDPOINTS = [Dofapi.APISchema.EQUIPMENTS]
        _CRAFT = [Dofapi.EquipmentsSchema.ANNEAU, Dofapi.EquipmentsSchema.AMULETTE]

    class Mineur(Profession):
        _ENDPOINTS = [Dofapi.APISchema.RESOURCES]
        _CRAFT = [Dofapi.ResourcesSchema.ALLIAGE, Dofapi.ResourcesSchema.PIERRE_PRECIEUSE]

    class Alchimiste(Profession):
        _ENDPOINTS = [Dofapi.APISchema.RESOURCES, Dofapi.APISchema.CONSUMABLES]
        _CRAFT = [Dofapi.ResourcesSchema.ESSENCE, Dofapi.ResourcesSchema.TEINTURE, Dofapi.ConsumablesSchema.POTION,
                  Dofapi.ConsumablesSchema.POTION_CONQUETE, Dofapi.ConsumablesSchema.POTION_OUBLI_PERCEPTEUR,
                  Dofapi.ConsumablesSchema.POTION_TELEPORTATION]

    class Tailleur(Profession):
        _ENDPOINTS = [Dofapi.APISchema.EQUIPMENTS]
        _CRAFT = [Dofapi.EquipmentsSchema.CAPE, Dofapi.EquipmentsSchema.CHAPEAU, Dofapi.EquipmentsSchema.SAC_DOS]

    class Paysan(Profession):
        _ENDPOINTS = []
        _CRAFT = []

    class Pecheur(Profession):
        _ENDPOINTS = []
        _CRAFT = []

    class Chasseur(Profession):
        _ENDPOINTS = []
        _CRAFT = []

    class Forgemage(Profession):
        pass

    class Sculptemage(Profession):
        pass

    class Faconneur(Profession):
        _ENDPOINTS = [Dofapi.APISchema.RESOURCES, Dofapi.APISchema.EQUIPMENTS]
        _CRAFT = [Dofapi.ResourcesSchema.IDOLE, Dofapi.EquipmentsSchema.TROPHEE, Dofapi.EquipmentsSchema.BOUCLIER]

    class Cordomage(Profession):
        pass

    class Joaillomage(Profession):
        pass

    class Costumage(Profession):
        pass

    class Bricoleur(Profession):
        _ENDPOINTS = [Dofapi.APISchema.RESOURCES, Dofapi.APISchema.CONSUMABLES]
        _CRAFT = [Dofapi.ResourcesSchema.CLEF, Dofapi.ConsumablesSchema.OBJET_ELEVAGE]

    class Facomage(Profession):
        pass

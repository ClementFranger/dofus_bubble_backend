from dofapi.dofapi import Dofapi
from utils import Schema


class Profession(object):
    ENDPOINTS = []
    CRAFT = []

    def endpoints(self):
        return list(set(self.ENDPOINTS))

    def craft(self):
        return list(set(self.CRAFT))


class Professions(Schema):

    def get(self, profession):
        return getattr(self, profession)()

    class Bucheron(Profession):
        ENDPOINTS = [Dofapi.APISchema.RESOURCES]
        CRAFT = [Dofapi.ResourcesSchema.PLANCHE, Dofapi.ResourcesSchema.SUBSTRAT]

    class Forgeron(Profession):
        ENDPOINTS = [Dofapi.APISchema.WEAPONS]
        CRAFT = [Dofapi.WeaponsSchema.EPEE, Dofapi.WeaponsSchema.DAGUE, Dofapi.WeaponsSchema.MARTEAU,
                 Dofapi.WeaponsSchema.PELLE, Dofapi.WeaponsSchema.HACHE, Dofapi.WeaponsSchema.FAUX,
                 Dofapi.WeaponsSchema.FAUX]

    class Sculpteur(Profession):
        ENDPOINTS = [Dofapi.APISchema.WEAPONS]
        CRAFT = [Dofapi.WeaponsSchema.BAGUETTE, Dofapi.WeaponsSchema.ARC, Dofapi.WeaponsSchema.BATON]

    class Cordonnier(Profession):
        ENDPOINTS = [Dofapi.APISchema.EQUIPMENTS]
        CRAFT = [Dofapi.EquipmentsSchema.BOTTES, Dofapi.EquipmentsSchema.CEINTURE]

    class Bijoutier(Profession):
        ENDPOINTS = [Dofapi.APISchema.EQUIPMENTS]
        CRAFT = [Dofapi.EquipmentsSchema.ANNEAU, Dofapi.EquipmentsSchema.AMULETTE]

    class Mineur(Profession):
        ENDPOINTS = [Dofapi.APISchema.RESOURCES, Dofapi.APISchema.WEAPONS]
        CRAFT = [Dofapi.ResourcesSchema.ALLIAGE, Dofapi.ResourcesSchema.PIERRE_PRECIEUSE,
                 Dofapi.ResourcesSchema.ORBRE_FORGEMAGIE, Dofapi.WeaponsSchema.PIERRE_AME]

    class Alchimiste(Profession):
        ENDPOINTS = [Dofapi.APISchema.RESOURCES, Dofapi.APISchema.CONSUMABLES]
        CRAFT = [Dofapi.ResourcesSchema.ESSENCE, Dofapi.ResourcesSchema.TEINTURE, Dofapi.ConsumablesSchema.POTION,
                 Dofapi.ConsumablesSchema.POTION_CONQUETE, Dofapi.ConsumablesSchema.POTION_OUBLI_PERCEPTEUR,
                 Dofapi.ConsumablesSchema.POTION_TELEPORTATION]

    class Tailleur(Profession):
        ENDPOINTS = [Dofapi.APISchema.EQUIPMENTS]
        CRAFT = [Dofapi.EquipmentsSchema.CAPE, Dofapi.EquipmentsSchema.CHAPEAU, Dofapi.EquipmentsSchema.SAC_DOS]

    class Paysan(Profession):
        ENDPOINTS = []
        CRAFT = []

    class Pecheur(Profession):
        ENDPOINTS = []
        CRAFT = []

    class Chasseur(Profession):
        ENDPOINTS = []
        CRAFT = []

    class Forgemage(Profession):
        pass

    class Sculptemage(Profession):
        pass

    class Faconneur(Profession):
        ENDPOINTS = [Dofapi.APISchema.RESOURCES, Dofapi.APISchema.EQUIPMENTS]
        CRAFT = [Dofapi.ResourcesSchema.IDOLE, Dofapi.EquipmentsSchema.TROPHEE, Dofapi.EquipmentsSchema.BOUCLIER]

    class Cordomage(Profession):
        pass

    class Joaillomage(Profession):
        pass

    class Costumage(Profession):
        pass

    class Bricoleur(Profession):
        ENDPOINTS = [Dofapi.APISchema.RESOURCES, Dofapi.APISchema.CONSUMABLES]
        CRAFT = [Dofapi.ResourcesSchema.CLEF, Dofapi.ConsumablesSchema.OBJET_ELEVAGE]

    class Facomage(Profession):
        pass

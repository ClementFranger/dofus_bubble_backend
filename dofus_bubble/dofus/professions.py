from dofapi.dofapi import Dofapi


class Profession(object):

    @staticmethod
    def _keys():
        return [p for p in dir(Profession) if not p.startswith('_')]

    class Bucheron(object):
        _CRAFT = [Dofapi.ResourcesSchema.PLANCHE, Dofapi.ResourcesSchema.SUBSTRAT]

    class Forgeron(object):
        _CRAFT = [Dofapi.WeaponsSchema.EPEE, Dofapi.WeaponsSchema.DAGUE, Dofapi.WeaponsSchema.MARTEAU,
                  Dofapi.WeaponsSchema.PELLE, Dofapi.WeaponsSchema.HACHE, Dofapi.WeaponsSchema.FAUX,
                  Dofapi.WeaponsSchema.FAUX]

    class Sculpteur(object):
        _CRAFT = [Dofapi.WeaponsSchema.BAGUETTE, Dofapi.WeaponsSchema.ARC, Dofapi.WeaponsSchema.BATON]

    class Cordonnier(object):
        _CRAFT = [Dofapi.EquipmentsSchema.BOTTES, Dofapi.EquipmentsSchema.CEINTURE]

    class Bijoutier(object):
        _CRAFT = [Dofapi.EquipmentsSchema.ANNEAU, Dofapi.EquipmentsSchema.AMULETTE]

    class Mineur(object):
        _CRAFT = [Dofapi.ResourcesSchema.ALLIAGE, Dofapi.ResourcesSchema.PIERRE_PRECIEUSE]

    class Alchimiste(object):
        _CRAFT = [Dofapi.ResourcesSchema.ESSENCE, Dofapi.ResourcesSchema.TEINTURE, Dofapi.ConsumablesSchema.POTION,
                  Dofapi.ConsumablesSchema.POTION_CONQUETE, Dofapi.ConsumablesSchema.POTION_OUBLI_PERCEPTEUR,
                  Dofapi.ConsumablesSchema.POTION_TELEPORTATION]

    class Tailleur(object):
        _CRAFT = [Dofapi.EquipmentsSchema.CAPE, Dofapi.EquipmentsSchema.CHAPEAU, Dofapi.EquipmentsSchema.SAC_DOS]

    class Paysan(object):
        _CRAFT = []

    class Pecheur(object):
        _CRAFT = []

    class Chasseur(object):
        _CRAFT = []

    class Forgemage(object):
        pass

    class Sculptemage(object):
        pass

    class Faconneur(object):
        _CRAFT = [Dofapi.ResourcesSchema.IDOLE, Dofapi.EquipmentsSchema.TROPHEE, Dofapi.EquipmentsSchema.BOUCLIER]

    class Cordomage(object):
        pass

    class Joaillomage(object):
        pass

    class Costumage(object):
        pass

    class Bricoleur(object):
        _CRAFT = [Dofapi.ResourcesSchema.CLEF, Dofapi.ConsumablesSchema.OBJET_ELEVAGE]

    class Facomage(object):
        pass

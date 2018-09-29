from basic_functions import BasicFunctions
from items import Weapon, Armor

d = BasicFunctions.d


class Constants:

    class AttackType:

        def __init__(self, **kwargs):
            for arg, value in kwargs.items():
                setattr(self, arg, value)

    class ClassPropertyGetter:

        def __init__(self, fget):
            self.fget = fget

        def __get__(self, obj, type_=None):
            if type_ is None:
                type_ = type(obj)
            return self.fget.__get__(obj, type_)()

    @classmethod
    def classproperty(cls, func):
        if not isinstance(func, (classmethod, staticmethod)):
            func = classmethod(func)
        return cls.ClassPropertyGetter(func)

    ER_UNNOMINATOR = 2
    STR_UNNOMINATOR = 4
    EVASION_THRESHOLD = 4

    ATTACK_HIT = AttackType(name='hit',
                            attack_flavours=('fp', 'hp', 'bp'),
                            offense_power=
        lambda person: (person.full_str + person.full_dex//2) // 2,
                            defense_power=
        lambda person: person.ac,
                            accuracy_power=
        lambda person, distance: person.int//2 + person.dex + person.str//2,
                            dodge_power=
        lambda person: d(person.int+person.dex-person.encumbrance),
                            block_power=
        lambda person, damage:  (max(0, person.str + min(0, damage)), 'fp'),
                            graze_power=
        lambda person, damage: (damage, 'hp'),
                            hit_power=
        lambda person, damage: (person.int + person.dex//2 + damage, 'bp')
                            )

    ATTACK_POKE = AttackType(name='poke',
                            offense_power=
        lambda person: (person.full_str//2 + person.full_dex*2) // 3,
                            defense_power=
        lambda person: person.ac//2,
                            accuracy_power=
        lambda person, distance: person.int//2 + person.dex*2,
                            dodge_power=
        lambda person: d(person.int + d(person.dex - person.encumbrance)),
                            block_power=
        lambda person, damage: (max(0, person.str//3 + min(0, damage)), 'fp'),
                            graze_power=
        lambda person, damage: (damage, 'hp'),
                            hit_power=
        lambda person, damage: (person.dex*2 + damage, 'bp')
                            )

    ATTACK_CRUSH = AttackType(name='crush',
                            offense_power=
        lambda person: person.full_str,
                            defense_power=
        lambda person: 0,
                            accuracy_power=
        lambda person, distance: person.int//4 + person.dex//2 + person.str,
                            dodge_power=
        lambda person: d(person.int + person.dex - d(person.encumbrance)),
                            block_power=
        lambda person, damage: (person.str, 'fp'),
                            graze_power=
        lambda person, damage: (damage, 'hp'),
                            hit_power=
        lambda person, damage: (1, 'stun')
                            )

    ATTACK_HEX = AttackType(name='hex',
                            offense_power=
        lambda person: person.full_int,
                            defense_power=
        lambda person: person.ac//3 + person.mr*person.int,
                            accuracy_power=
        lambda person, distance: max(person.int, person.full_int//distance),
                            dodge_power=
        lambda person: d(person.full_int) + person.mr,
                            block_power=
        lambda person, damage: (max(0, person.int + damage), 'mp'),
                            graze_power=
        lambda person, damage: (damage, 'mp'),
                            hit_power=
        lambda person, damage: (damage*3, 'fp')
                            )

    CONTROLS = {'move_up'         : b't',
                'move_up_right'   : b'y',
                'move_right'      : b'h',
                'move_down_right' : b'n',
                'move_down'       : b'b',
                'move_down_left'  : b'v',
                'move_left'       : b'f',
                'move_up_left'    : b'r',
                'get_item'        : b'g',
                'drop_item'       : b'd',
                'use_item'        : b'i',
                'shout'           : b'u',
                'inspect_tile'    : b'm',
                'dual_wield'      : b' '}

    ICONS = {'weapon'    : '!',
             'potion'    : '?',
             'food'      : '%',
             'armor'     : '[',
             'shield'    : ']',
             'accessory' : '"',
             'wall'      : '#',
             'door'      : '+',
             'unknown'   : ',',
             'nothing'   : '.'}

    STATUS_TEMPLATE = {'poison': 0, 'energy': 0, 'regeneration': 0,
                       'viper': 0, 'madness': 0, 'brilliance': 0}

    # Those three return new instance of a class by template.
    @classproperty
    def NULL_WEAPON(cls):
        return Weapon('''Something''')

    @classproperty
    def NULL_ARMOR(cls):
        return Armor('''Something''')

    @classproperty
    def NULL_SHIELD(cls):
        return Weapon('''Something''')

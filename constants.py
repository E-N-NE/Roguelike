from basic_functions import BasicFunctions

d = BasicFunctions.d

class Constants:

    def __init__(self):
        pass

    ER_UNNOMINATOR = 2
    STR_UNNOMINATOR = 4
    EVASION_THRESHOLD = 4


    class AttackType:

        def __init__(self, **kwargs):
            for arg, value in kwargs.items():
                setattr(self, arg, value)


    ATTACK_HIT = AttackType(name='hit',
                            attack_flavour1='fp',
                            attack_flavour2='hp',
                            attack_flavour3='bp',
                            offense_power=
       lambda person           : (person.full_str + person.full_dex//2) // 2,
                            defense_power=
       lambda person           : person.ac,
                            accuracy_power=
       lambda person, distance : person.int//2 + person.dex + person.str//2,
                            dodge_power=
       lambda person           : d(person.int+person.dex-person.encumbrance),
                            block_power=
       lambda person, damage   :  max(0, person.str + min(0, damage)),
                            graze_power=
       lambda person, damage   : damage,
                            hit_power=
       lambda person, damage   : person.int + person.dex//2 + damage
                            )

    controls = {'move_up'         : b't',
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

    icons = {'weapon'    : '!',
             'potion'    : '?',
             'food'      : '%',
             'armor'     : '[',
             'shield'    : ']',
             'accessory' : '"',
             'wall'      : '#',
             'door'      : '+',
             'unknown'   : ',',
             'nothing'   : '.'}

    # Those three return new instance of a class by template.
    @staticmethod
    def NULL_WEAPON():
        return Weapon('''Something''')

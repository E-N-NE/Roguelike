from basic_functions import BasicFunctions

d = BasicFunctions.d


class PersonInteractions:

    def __init__(self, messenger, *constants):
        self.messenger = messenger
        self.EVASION_THRESHOLD = constants
        self.ATTACK_FLAVOURS = {'hit': ['']}

    @staticmethod
    def evasion_damage(en_a, en_d, attack_type):
        evasion = en_d.dodge_power(attack_type) * (not en_d.status['stun']) \
                  - en_a.accuracy_power(attack_type)
        damage = (
            en_a.offense_power(attack_type)
            + en_d.offense_power(attack_type) * ('illusion' in en_a.doping)
            - en_d.defense_power(attack_type)
                 ) \
            // max(1, evasion)
        return evasion, damage

    # What happens when en_a attacks en_d.
    def attack(self, en_a, en_d, attack_type):
        evasion, damage = self.evasion_damage(en_a, en_d, attack_type)
        if evasion >= self.EVASION_THRESHOLD:
            self.dodge_confirms(en_a, en_d, damage, attack_type)
        elif damage <= 0:
            self.block_confirms(en_a, en_d, damage, attack_type)
        elif evasion > 1:
            self.graze_confirms(en_a, en_d, damage, attack_type)
        else:
            self.hit_confirms(en_a, en_d, damage, attack_type)

    @staticmethod
    def plural(word):
        if word[-1] == 's' or word[-1] == 'x' or\
          (word[-2] == 's' or word[-2] == 'c') and word[-1] == 'h':
            return word+'es'
        else:
            return word+'s'

    @staticmethod
    # Decreases a specific value of en_d.
    def reduce(en_d, amount, flavour):
        if flavour == 'hp':
            en_d.hp -= amount
        elif flavour == 'fp':
            en_d.fp += amount
        elif flavour == 'bp':
            en_d.bp += amount
        elif flavour == 'sp':
            en_d.sp -= amount
        elif flavour == 'stun':
            en_d.status['stun'] += 1
        elif flavour == 'mp':
            en_d.mp -= amount

    # Feed the message into a list of a Messenger class.
    def add_feed(self, string):
        self.messenger.feed += [string]

    #
    def special_effects(self, en_a, en_d, damage, attack_type):
        if 'vampirism' in en_a.doping:
            en_a.heal(damage)
            self.add_feed("{} drains {}.".format(en_a.name,
                                                              en_d.name))
            if attack_type == 'bite' and 'kai' not in en_d.doping:
                en_d.base_doping += ['kai', 'vampirism']
        if en_a.status['viper']:
            en_d.status['poison'] += d(en_a.status['viper']+en_a.dex-en_d.dex)
            self.add_feed("{} poisons {}.".format(en_a.name, en_d.name))
        if 'kai' in en_d.doping and 'purify' in en_a.doping:
            en_d.hp = -45
            self.add_feed("{} purifies {}.".format(en_a.name, en_d.name))
        if 'death' in en_a.doping:
            en_d.hp = -45
            self.add_feed("{} executes {}.".format(en_a.name, en_d.name))

    # Messages and calculations in the case en_d dodges.
    def dodge_confirms(self, en_a, en_d, damage, attack_type):
        self.add_feed("{} dodges {}'s {}.".format(en_d.name,
                                                  en_a.name,
                                                  attack_type))
        if 'pride' in en_a.doping:
            en_a.hp -= 111  # Maybe change?
            self.add_feed += ["{}'s pride hurts!".format(en_a.name)]

    # Messages and calculations in the case en_d dodges.
    def block_confirms(self, en_a, en_d, damage, attack_type):
        self.reduce(en_d,
                    en_a.block_power(attack_type, damage),
                    self.ATTACK_FLAVOURS[attack_type][2])
        self.add_feed("{} blocks {}'s {}.".format(en_d.name,
                                                  en_a.name,
                                                  attack_type))
        if 'pride' in en_a.doping:
            en_a.hp -= 111  # Maybe change?
            self.add_feed("{}'s pride hurts!".format(en_a.name))

    # Messages and calculations in the case en_a grazes.
    def graze_confirms(self, en_a, en_d, damage, attack_type):
        self.reduce(en_d,
                    damage,
                    self.ATTACK_FLAVOURS[attack_type][0])
        self.reduce(en_d,
                    en_a.bonus_power(attack_type, damage),
                    self.ATTACK_FLAVOURS[attack_type][1])
        self.add_feed("{}'s {} grazes {}.".format(en_a.name,
                                                  attack_type,
                                                  en_d.name))
        self.special_effects(en_a, en_d, damage, attack_type)

    # Messages and calculations in the case en_a hits.
    def hit_confirms(self, en_a, en_d, damage, attack_type):
        self.reduce(en_d,
                    damage,
                    self.ATTACK_FLAVOURS[attack_type][0])
        self.reduce(en_d,
                    en_a.bonus_power(attack_type, damage),
                    self.ATTACK_FLAVOURS[attack_type][1])
        self.add_feed("{} {} {}.".format(en_a.name,
                                         self.plural(attack_type),
                                         en_d.name))
        self.special_effects(en_a, en_d, damage, attack_type)

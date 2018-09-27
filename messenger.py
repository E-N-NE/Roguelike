from constants import Constants

class Messenger:

    def __init__(self, player, mapper):
        self.player = player
        self.mapper = mapper
        self.feed = []

    @classmethod
    # Makes a line from a 'number' of lines.
    def split_pane(cls, number, length, *lists):
        out = []
        for j in range(number):
            lists[j] = cls.fill_list(length, lists[j])
        for i in range(length):
            line = ''
            for j in range(number):
                line += lists[j][i]+' '
            out += [line]
        return out

    @staticmethod
    # Fills list with empty lines.
    def fill_list(length, list_):
        for i in range(max(length-len(list_), 0)):
            list_ += ['']
        return list_

    @classmethod
    def stats(cls, person):
        return [
                '{}'.format(cls.rank(person)),
                'HP:{:<7}MP:{:<7}FP:{}'.format(person.hp,
                                               person.mp,
                                               person.fp),
                'BP:{:<7}SP:{:<7}XP:{}'.format(person.bp,
                                               person.sp,
                                               person.xp),
                'AC:{:<7}ER:{:<7}MR:{}'.format(person.ac,
                                               person.er,
                                               person.mr),
                'STR:{:<6}DEX:{:<6}INT:{}'.format(person.str,
                                                  person.dex,
                                                  person.int),
                'Wear:{}'.format(person.wear.name),
                'AC:{:<7}ER:{:<7}MR:{}'.format(person.wear.ac,
                                               person.wear.er,
                                               person.wear.mr),
                'Wield:{}'.format(person.wield.name),
                'AC:{:<7}ER:{:<7}MR:{}'.format(person.wield.ac,
                                               person.wield.er,
                                               person.wield.mr),
                'STR:{:<6}DEX:{:<6}INT:{}'.format(person.wield.strm,
                                                  person.wield.dexm,
                                                  person.wield.intm)
               ]\
            + ([
               'Shield:{}'.format(person.shield.name),
               'AC:{:<7}ER:{:<7}MR:{}'.format(person.shield.ac,
                                              person.shield.er,
                                              person.shield.mr)
               ]
               if person.dual_wield == 0 else
               [
               'Shield:-'
               ]
               )


    def print_everything(self):
        print_stats = self.stats(self.player)
        printer = self.split_pane(2,self.player.ROS*2+1,
                                  [self.mapper.map(self.player.ROS),
                                   print_stats])

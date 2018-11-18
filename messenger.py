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

        for i in range(number):
            for j in range(length - len(lists[i])):
                lists[i].append('')

        for i in range(length):
            line = ''
            for j in range(number):
                line += lists[j][i]+' '
            line += '\n'
            out.append(line)
        return out

    @staticmethod
    # Fills list with empty lines.
    def fill_list(length, list_):
        for i in range(length-len(list_)):
            list_.append('')
        return list_

    def print_everything(self):
        print_stats = self.player.human_readable_stats.split('\n')
        printer = self.split_pane(2, self.player.ros*2+1,
                                  [self.mapper.map(self.player.ros),
                                   print_stats])
        self.messenger_output(printer)

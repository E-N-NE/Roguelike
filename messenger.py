class Messenger:

    def __init__(self):
        pass

    @classmethod
    # Makes a line from a 'number' of lines.
    def split_pane(cls, number, length, *lists):
        out = []
        for j in range(number):

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


    def print_everything(self):
        printer = self.split_pane(2,SoMeLeNgTh*2+1,self.mapper.map(SoMeLeNgTh) +

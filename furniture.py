from constants import Constants


class Furniture:

    def __init__(self, icon, name, x, y):
        self.icon = icon
        self.name = name
        self.x = x
        self.y = y


class Wall(Furniture):

    def __init__(self, name, x, y):
        super().__init__(Constants.ICONS['wall'],
                         name, x, y)


class Stairs(Furniture):

    def __init__(self, name, connection, direction, x, y):
        self.connection = connection
        super().__init__(Constants.ICONS['stairs {}'.format(direction)],
                         name, x, y)


class Door(Furniture):

    def __init__(self, name, x, y):
        self.open = 0
        super().__init__(Constants.ICONS['door{}'.format(' open'*self.open)],
                         name, x, y)


class Void(Furniture):

    def __init__(self, name, x, y):
        super().__init__(Constants.ICONS['void'],
                         name, x, y)

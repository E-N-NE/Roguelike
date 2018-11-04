from constants import Constants


class Furniture:

    def __init__(self, walkable, icon, name, x, y):
        self.icon = icon
        self.walkable = walkable
        self.name = name
        self.x = x
        self.y = y


class Wall(Furniture):

    def __init__(self, name, x, y):
        super().__init__(Constants.ICONS['wall'], False,
                         name, x, y)


class Stairs(Furniture):

    def __init__(self, name, connection, direction, x, y):
        self.connection = connection
        super().__init__(Constants.ICONS['stairs {}'.format(direction)], True,
                         name, x, y)


class Door(Furniture):

    def __init__(self, name, x, y):
        super().__init__('', False,
                         name, x, y)

    @property
    def icon(self):
        return Constants.ICONS['door{}'.format(' open' * self.walkable)]


class Water(Furniture):

    def __init__(self, name, x, y):
        super().__init__(Constants.ICONS['void'], False,
                         name, x, y)

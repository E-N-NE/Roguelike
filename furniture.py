from constants import Icons


class Furniture:

    def __init__(self, walkable, icon, name, x, y):
        self._icon = icon
        self.walkable = walkable
        self.name = name
        self.x = x
        self.y = y

    @property
    def transparency(self):
        return self.walkable

    @property
    def icon(self):
        return self._icon


class Wall(Furniture):

    def __init__(self, name, x, y):
        super().__init__(Icons.WALL, False,
                         name, x, y)


class Stairs(Furniture):

    def __init__(self, name, connection, direction, x, y):
        self.connection = connection
        super().__init__(Icons.STAIRS_DOWN if direction == '>'
                         else Icons.STAIRS_UP, True,
                         name, x, y)


class Door(Furniture):

    def __init__(self, name, x, y):
        super().__init__('', False,
                         name, x, y)

    @property
    def icon(self):
        return Icons.DOOR_OPEN if self.walkable else Icons.DOOR_CLOSED


class Water(Furniture):

    def __init__(self, name, x, y):
        super().__init__(Icons.WATER, False,
                         name, x, y)

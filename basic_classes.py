class Coordinates:

    def __init__(self, x, y):
        assert (x.__class__ is int) and (y.__class__ is int),\
            "Trying to put gibberish in coordinates.\n"\
            "Gibberish is {} and {}.".format(x.__class__.__name__,
                                             y.__class__.__name__)
        self.x = x
        self.y = y

    def __add__(self, increment):
        assert increment.__class__ is Coordinates, \
            "Trying to add gibberish to coordinates.\n"\
            "Gibberish is {}.".format(increment.__class__.__name__)
        return Coordinates(self.x + increment.x, self.y + increment.y)

    def __sub__(self, increment):
        assert increment.__class__ is Coordinates,\
            "Trying to subtract gibberish from coordinates.\n"\
            "Gibberish is {}.".format(increment.__class__.__name__)
        return Coordinates(self.x - increment.x, self.y - increment.y)

    def __eq__(self, other):
        assert other.__class__ is Coordinates, \
            "Trying to compare gibberish with coordinates.\n" \
            "Gibberish is {}.".format(other.__class__.__name__)
        return self.x == other.x and self.y == other.y

    def copy(self):
        return Coordinates(self.x, self.y)

    # Can turn only coordinates exactly one tile far from zero.
    def turn_clw(self):
        assert 0 < self.x**2 + self.y**2 < 3,\
            "Trying to turn unacceptable coordinates.\n"\
            "({}, {})".format(self.x, self.y)
        mid = self.x
        self.x += self.y * (self.x != self.y)
        self.y += -mid * (-mid != self.y)

    def next_clw(self):
        assert 0 < self.x ** 2 + self.y ** 2 < 3, \
            "Trying to turn unacceptable coordinates.\n" \
            "({}, {})".format(self.x, self.y)
        return Coordinates(
            self.x + self.y * (self.x != self.y),
            self.y - self.x * (-self.x != self.y)
        )


class Size:

    def __init__(self, width, height):
        self.width = width
        self.height = height


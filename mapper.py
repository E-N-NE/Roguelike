from constants import Icons
from basic_classes import Coordinates, Size

class Mapper:

    def __init__(self, world):
        self.world = world

    class PathWalker:

        def __init__(self, increment, distance):
            self.increment_1 = increment.copy()
            self.increment_2 = increment.next_clw()
            self.case_multiply_x = self.increment_1.y + self.increment_2.y
            self.case_multiply_y = self.increment_1.x + self.increment_2.x
            self.targets =

        # We choose direction closest to the line from current to target.
        def cased_increment(self, current, target):
            delta = target - current
            if delta.x*self.case_multiply_x > delta.y*self.case_multiply_y:
                return self.increment_1,
            elif delta.x*self.case_multiply_x < delta.y*self.case_multiply_y:
                return self.increment_2,
            else:
                return self.increment_1, self.increment_2

        def turn_clw(self):
            self.increment_1.turn_clw()
            self.increment_2.turn_clw()
            self.case_multiply_x = self.increment_1.y + self.increment_2.y
            self.case_multiply_y = self.increment_1.x + self.increment_2.x

    class MapImage:

        def __init__(self, ros, real_position, stage):
            self.size = Size(ros*2 + 1, ros*2 + 1)
            self.image = self.empty_image
            self.real_position = real_position
            self.stage = stage

        @property
        def empty_image(self):
            return [[Icons.UNKNOWN]*self.size.width
                    for i in range(self.size.height)]

        def advance(self, current, target, walker):
            response = self.visual_response(current.x, current.y)
            self.image[current.x][current.y] = response.icon
            if not response.tranparency:
                return

            if current != target:
                for increment in walker.cased_increment(current, target):
                    self.advance(current + increment, target, walker)

        def visual_response(self, x, y):
            if self.stage.mob_is_at(x, y):
                return self.stage.visual_response_of_mob_at(x, y)
            elif self.stage.furniture_is_at(x, y):
                return self.stage.visual_response_of_furniture_at(x, y)
            elif self.stage.item_is_at(x, y):
                return self.stage.visual_response_of_item_at(x, y)
            else:
                return Icons.NOTHING

    def draw_map(self, ros, x, y):

        walker = self.PathWalker(Coordinates(0, 1), ros)

        for i in range(8):



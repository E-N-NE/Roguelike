# from basic_functions import d, r
from constants import Icons
from furniture import Wall, Stairs, Door, Water

from subprocess import Popen, PIPE, STDOUT


class World:

    @classmethod
    def create_new_stage(cls, connections, stage_info, generator):
        return cls.Stage(connections, stage_info, generator)

    # class Pattern:
    #
    #     def __init__(self, contents=(('.',),), width=1, height=1):
    #         self.contents = contents
    #         self.width = width
    #         self.height = height
    #         assert height == len(contents),\
    #             "Pattern creation failed, size_y mismatch."
    #         assert width == len(contents[0]),\
    #             "Pattern creation failed, size_x mismatch."
    #         if __debug__:
    #             for i in range(len(contents) - 1):
    #                 assert len(contents[i]) == len(contents[i+1]),\
    #                     "Pattern creation failed, lengths mismatch."
    #
    #     def intake(self, start_x, start_y, pattern):
    #         for i in range(pattern.size_x):
    #             for j in range(pattern.size_y):
    #                 if '?' not in pattern[i][j]:
    #                     self.contents[start_x+i][start_y+j] = pattern[i][j]
    #
    # class Divergence:
    #
    #     def __init__(self, randomizer, probability):
    #         self.randomizer = randomizer
    #         self.probability = probability
    #         assert 0.0 <= probability <= 1.0,\
    #             "Incorrect probability, {}.".format(probability)
    #
    # class Movement:
    #
    #     def __init__(self, count, direction, divergence):
    #         self.count = count
    #         self.direction = direction
    #         self.divergence = divergence
    #         assert len(direction) == 2,\
    #             "Incorrect direction, {}.".format(direction)
    #
    # class Generator:
    #
    #     def __init__(self, count, pattern, movement):
    #         self.count = count
    #         self.pattern = pattern
    #         self.movement = movement
    #
    #     def modify(self, stage):
    #         rightmost = stage.width - self.pattern.width
    #         downmost = stage.height - self.pattern.height
    #         for i in range(self.count):
    #             pos_x = d(rightmost + 1) - 1
    #             pos_y = d(downmost + 1) - 1
    #             for j in range(self.movement.count):
    #                 if rightmost >= pos_x >= 0 and rightmost >= pos_y >= 0:
    #                     stage.contents.intake(pos_x, pos_y, self.pattern)
    #                 else:
    #                     break
    #                 if r(self.movement.divergence.probability):
    #                     move = self.movement.divergence.randomizer()
    #                 else:
    #                     move = self.movement.direction
    #                 pos_x += move[0]
    #                 pos_y += move[1]

    class StageInfo:

        def __init__(self, width, height, mob_info,
                     width_partition=8, height_partition=8, type='s'):
            self.width = width
            self.height = height
            self.width_partition = width_partition
            self.height_partition = height_partition
            self.mob_info = mob_info
            self.type = type

    class Stage:

        def __init__(self, connections, stage_info):
            self.mob_list = []
            self.item_list = []
            self.furniture_list = []
            self.width = stage_info.width
            self.height = stage_info.height
            self.width_partition = stage_info.width_partition
            self.height_partition = stage_info.height_partition
            map = Popen(['map_generator.exe',
                         self.width, self.height, stage_info.type],
                        stdout=PIPE, stderr=STDOUT, shell=True)
            for y in range(self.height):
                line = map.stdout.readline()
                for x in range(self.width):
                    if line[x] == Icons.NOTHING:
                        pass
                    elif line[x] == Icons.WALL:
                        self.furniture_list.append(Wall('Wall', x, y))
                    elif line[x] == Icons.DOOR_CLOSED:
                        self.furniture_list.append(Door('Door', x, y))
                    elif line[x] == Icons.WATER:
                        self.furniture_list.append(Water('Water', x, y))

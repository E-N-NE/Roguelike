class World:

    @classmethod
    def create_new_stage(cls, connections, stage_info):
        return cls.Stage(connections, stage_info)


    class Stage:

        def __init__(self):
            pass
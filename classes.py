class Particle:

    def __init__(self):
        self.location
        self.direction

    def particle_collision(self):
        pass

    def move(self):
        pass


class Entity:

    def __init__(self):
        self.health
        self.energy
        self.location
        self.direction

    def move(self):
        pass

    def terrain_collision(self):
        pass


class Terrain:

    def __init__(self):
        self.location
        self.dimensions


class SubTerrain(Terrain):

    def __init__(self):
        Terrain.__init__(self)
        self.health


class Skill:

    def __init__(self):
        self.skill_id
        self.damage
        self.energy_cost
        self.cooldown

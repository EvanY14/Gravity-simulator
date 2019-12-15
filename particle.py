import math


class Particle:
    radius = 0
    position = [0, 0, 0]
    mass = 0
    gravitational_constant = 6.67408 * pow(10.0, -0.5)
    velocity = [0, 0, 0]
    acceleration = [0, 0, 0]
    density = 70
    color = [0, 0, 0]
    is_black_hole = False
    trail = []
    movable = True

    def __init__(self, radius, position, velocity, color, is_black_hole, trail):
        self.radius = radius
        self.position = position
        self.velocity = velocity
        self.mass = math.pi * pow(radius, 2) * self.density
        self.color = color
        self.is_black_hole = is_black_hole
        self.trail = trail

    def get_trail(self):
        return self.trail

    def get_density(self):
        return self.density

    def get_radius(self):
        return self.radius

    def get_x(self):
        return int(self.position[0])

    def get_y(self):
        return int(self.position[1])

    def get_color(self):
        return self.color

    def set_black_hole(self, is_black_hole):
        self.is_black_hole = is_black_hole
        self.density = 10000
        self.mass = self.radius * pow(math.pi, 2) * self.density
        self.radius = self.get_radius() / 10
        self.color = [0, 0, 0]

    def get_is_black_hole(self):
        return self.is_black_hole

    def get_acceleration(self, p):
        sum_x = 0
        sum_y = 0
        x_sign = 1
        y_sign = 1
        for i in p:
            if not i == self:
                if self.get_distance_to_particle(i) <= self.get_radius() + i.get_radius():
                    return i
                else:
                    if i.get_x() - self.get_x() < 0:
                        x_sign = -1
                    if i.get_y() - self.get_y() < 0:
                        y_sign = -1

                    # if not (i.get_x() is self.get_x() and i.get_y() is self.get_y()):
                    sum_x += (self.gravitational_constant * i.get_mass() * self.get_mass() / pow(
                        self.get_distance_to_particle(i), 3)) * (i.get_x() - self.get_x())

                    sum_y += (self.gravitational_constant * i.get_mass() * self.get_mass() / pow(
                        self.get_distance_to_particle(i), 3)) * (i.get_y() - self.get_y())

        self.acceleration[0] = (sum_x / pow(self.get_mass(), 1)) / 5
        self.acceleration[1] = (sum_y / pow(self.get_mass(), 1)) / 5
        return None

    def get_acceleration_2(self, particles):
        sum_x = 0
        sum_y = 0
        sign_change_x = 1
        sign_change_y = 1
        for p in particles:
            if not p == self:
                if self.get_distance_to_particle(p) <= self.get_radius() + p.get_radius():
                    return p
                else:
                    # Correct for squaring the distance
                    '''
                    if self.get_x() - p.get_x() > 0:
                        sign_change_x = 1
                    if self.get_y() - p.get_y() > 0:
                        sign_change_y = 1
                    '''
                    if not (self.get_x() == p.get_x() and self.get_y() == p.get_y()):
                        sum_x += ((self.gravitational_constant * (p.get_mass() / self.get_mass())) / pow(
                            pow(self.get_x() - p.get_x(), 2) + pow(self.get_y() - p.get_y(), 2), 1.5)) / (
                                         p.get_x() - self.get_x())

                        # if not self.get_y() == p.get_y():
                        # sum_y += -1 * sign_change_y * (self.gravitational_constant * (
                        #       (self.get_mass() * p.get_mass()) / pow(self.get_y() - p.get_y(), 1)))
                        sum_y += ((self.gravitational_constant * (p.get_mass() / self.get_mass())) / pow(
                            pow(self.get_x() - p.get_x(), 2) +
                            pow(self.get_y() - p.get_y(), 2),
                            1.5)) / (p.get_y() - self.get_y())

                    sign_change_x = 1
                    sign_change_y = 1

        self.acceleration[0] = sum_x
        self.acceleration[1] = sum_y

        return None

    def get_acceleration_3(self, p):
        sum_x = 0
        sum_y = 0
        for i in p:
            if not i == self:
                if self.get_distance_to_particle(i) == 0:
                    return i
                else:
                    # if not (i.get_x() is self.get_x() and i.get_y() is self.get_y()):
                    sum_x += (self.gravitational_constant * i.get_mass() * self.get_mass()) \
                             / pow(self.get_distance_to_particle(i), 3)

                    sum_y += (self.gravitational_constant * i.get_mass() * (
                        self.get_mass())) / pow(self.get_distance_to_particle(i), 3)
        self.acceleration[0] = sum_x / self.get_mass()
        self.acceleration[1] = sum_y / self.get_mass()
        return None

    def get_acceleration_x(self):
        return self.acceleration[0]

    def get_acceleration_y(self):
        return self.acceleration[1]

    def calc_velocity_x(self, time):
        self.velocity[0] += self.get_acceleration_x() * time
        return self.velocity[0]

    def calc_velocity_y(self, time):
        self.velocity[1] += self.get_acceleration_y() * time
        return self.velocity[1]

    def get_velocity_x(self):
        x = self.velocity[0]
        return x

    def get_velocity_y(self):
        y = self.velocity[1]
        return y

    def get_mass(self):
        return self.mass

    def is_movable(self):
        return self.movable

    def set_x(self, x):
        self.position[0] = x

    def set_y(self, y):
        self.position[1] = y

    def set_density(self, density):
        self.density = density
        self.mass = math.pi * pow(self.radius, 2) * self.density

    def set_movable(self, movable):
        self.movable = movable

    def add_to_trail(self, pos):
        if (len(self.trail) > 20 and abs(pos[0] - self.trail[0][0]) < 20) or len(self.trail) > 1000:
            # if math.hypot(self.trail[0][0] - pos[0], self.trail[0][1] - pos[1]) > 100 + self.radius:
            self.trail.remove(self.trail[0])
        self.trail.append(pos)

    def get_distance_to_particle(self, p):
        distance = math.sqrt(pow(self.get_x() - p.get_x(), 2) + pow(self.get_y() - p.get_y(), 2))
        return abs(distance)

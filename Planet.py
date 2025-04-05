import math

class Planet:
    AU_TO_KM = 149597870.7  # 1 AU in km

    def __init__(self):
        self.name = None
        self.diameter = 0#km
        self.mass = 0#kg
        self.orbital_radius = None#AU
        self.period = 0#Days
        self.current_angular_position = 0#in degrees
        self.orbiting_speed = 0#in km/s

    def calculate_angular_position(self, time_in_days: float):#in degrees
        return round(360 / self.period * (time_in_days % self.period),2)

    def calculate_orbiting_speed(self):#in km/s
        self.orbiting_speed = 2 * math.pi * self.orbital_radius * self.AU_TO_KM / self.period / 24 / 3600

    def __str__(self):
        return f'{self.name}: Radius: {self.diameter}km Mass: {self.mass}kg'
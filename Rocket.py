import math

from Planet import Planet

GRAVITATIONAL_CONSTANT = 6.67 * pow(10,-11)
EARTH_MASS = 6 * pow(10,24)
AU_TO_KM = 149597870.7  # 1 AU in km

class Rocket:
    def __init__(self, rocket_filepath: str):
        self.engine_acceleration = None
        self.engine_number = None
        self.rocket_filepath = rocket_filepath
        self.read_rocket_data()

    def read_rocket_data(self):
        try:
            file = open(self.rocket_filepath, 'r')
        except:
            raise FileNotFoundError

        line = file.readline().strip()
        self.engine_number = int("".join(c for c in line if c.isnumeric() or c == '.'))
        line = file.readline().strip()
        self.engine_acceleration = float("".join(c for c in line[:len(line) -  1] if c.isnumeric() or c == '.'))


    def calculate_escape_velocity(self, planet: Planet):
        return int(math.sqrt(2 * GRAVITATIONAL_CONSTANT * planet.mass / (planet.diameter / 2) * 1000)/1000) #in m/s

    def calculate_time_to_escape_velocity(self, planet: Planet)->int:
            return int(int(self.calculate_escape_velocity(planet) / (self.engine_number * self.engine_acceleration)))# in s

    def calculate_distance_to_escape_velocity(self, planet: Planet, starting_velocity: float):#in m
        return int(starting_velocity * self.calculate_time_to_escape_velocity(planet) +
                self.engine_number * self.engine_acceleration * pow(self.calculate_time_to_escape_velocity(planet),2)
                / 2)

    def travel(self, start_planet: Planet, dest_planet: Planet):

        if self.calculate_escape_velocity(start_planet) > self.calculate_escape_velocity(dest_planet):
            bigger_velocity_planet = start_planet
        else:
            bigger_velocity_planet = dest_planet

        time_to_escape_velocity = self.calculate_time_to_escape_velocity(bigger_velocity_planet)
        distance_until_nominal_velocity =   math.ceil(self.calculate_distance_to_escape_velocity(bigger_velocity_planet, 0) / 10000) * 10 # in km

        #TYPO IN THE EXAMPLE: 77790892.76 - 6400 - 2900 - 1560 - 1560 = 77778482.76 (its 77778472.76)
        distance_between_planets_surfaces = abs(start_planet.orbital_radius - dest_planet.orbital_radius) * AU_TO_KM - start_planet.diameter / 2 - dest_planet.diameter / 2 #in km
        distance_between_burns = distance_between_planets_surfaces - distance_until_nominal_velocity * 2 #in km
        time_of_nominal_velocity = int(distance_between_burns * 1000 / self.calculate_escape_velocity(bigger_velocity_planet))

        decel_time = int(self.calculate_escape_velocity(bigger_velocity_planet) / (self.engine_number * self.engine_acceleration))

        total_travel_time = time_to_escape_velocity + decel_time + time_of_nominal_velocity #in seconds

        return (time_to_escape_velocity, distance_until_nominal_velocity, time_of_nominal_velocity,
                distance_until_nominal_velocity, decel_time, total_travel_time)

    def print_rocket_travel_data(self, start_planet: Planet, dest_planet: Planet):

        rocket_travel_data = self.travel(start_planet,dest_planet)

        print(f'Time to cruising velocity from {start_planet.name}: {rocket_travel_data[0]} seconds')
        print(f'Distance to cruising velocity from {start_planet.name}: {rocket_travel_data[1]} km')
        print(f'Time of nominal velocity: {rocket_travel_data[2]} seconds')
        print(f'Distance from {dest_planet.name} surface to begin deceleration burn : {rocket_travel_data[3]} km')
        print(f'Deceleration time when reaching {dest_planet.name}: {rocket_travel_data[4]} seconds')

        aux = rocket_travel_data[5]

        total_travel_time_days_hours_sec = '' + f'{int(aux / 86400)} days '  # in days
        aux = aux % 86400

        total_travel_time_days_hours_sec = total_travel_time_days_hours_sec + f'{int(aux / 3600)} hours '# in hours
        aux = aux % 3600

        total_travel_time_days_hours_sec = total_travel_time_days_hours_sec + f'{int(aux)} seconds ' #in seconds

        print(f'Total travel time aproximation: {total_travel_time_days_hours_sec}\n')

    def __str__(self):
        return f'Engine number: {self.engine_number} \nEngine acceleration: {self.engine_acceleration} m/s^2'
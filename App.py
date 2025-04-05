import math
from Planet import Planet
from Rocket import Rocket

GRAVITATIONAL_CONSTANT = 6.67 * pow(10,-11)
EARTH_MASS = 6 * pow(10,24)
AU_TO_KM = 149597870.7  # 1 AU in km

class Space_App:
    def __init__(self, planet_filepath:str, rocket_filepath: str, system_filepath: str):
        self.planet_filepath = planet_filepath
        self.rocket_filepath = rocket_filepath
        self.system_filepath = system_filepath

        self.planets = []
        self.read_planetary_data()#read and create planet with name, diameter and mass
        self.read_system_data()#read and initialize planet period and orbital radius

        self.rocket = Rocket(rocket_filepath)

        self.planet_escape_data = {}
        for planet in self.planets:
            self.planet_escape_data[planet.name] = (self.rocket.calculate_escape_velocity(planet)
                                                    , self.rocket.calculate_distance_to_escape_velocity(planet,0)
                                                    ,self.rocket.calculate_time_to_escape_velocity(planet))

    def simulate_solar_system(self, time_in_years: int, time_in_days: int):
        planetary_angular_position = []
        for planet in self.planets:
            angular_position = planet.calculate_angular_position(time_in_years * 365 + time_in_days)
            planetary_angular_position.append(angular_position)
            planet.current_angular_position = angular_position
            print(f'{planet.name} angular position: {planet.current_angular_position}')

        return planetary_angular_position


    def calculate_intermediary_planets(self, start_planet:Planet, dest_Planet:Planet):
        intermediary_planets = []

        step = 1
        if self.planets.index(start_planet) > self.planets.index(dest_Planet): step = -1

        for index in range(self.planets.index(start_planet), self.planets.index(dest_Planet),step):
            if index != self.planets.index(start_planet):
                intermediary_planets.append(self.planets[index])
        return intermediary_planets

    def calculate_possible_collision(self, start_planet: Planet, dest_planet: Planet, start_time: float) -> bool:
            intermediary_planets = self.calculate_intermediary_planets(start_planet, dest_planet)

            if len(intermediary_planets) == 0:
                return False

            rocket_travel_data = self.rocket.travel(start_planet, dest_planet)

            start_angular_position = start_planet.current_angular_position

            for planet in intermediary_planets:

                distance_to_planet = abs(start_planet.orbital_radius - planet.orbital_radius) * AU_TO_KM - start_planet.diameter #in front of its core in km

                # time to escape velocity + (distance(start_planet_surface,current_planet_core) - distance_until_nominal_velocity) / nominal velocity
                time_to_reach_planet = (rocket_travel_data[0] + (distance_to_planet - rocket_travel_data[1]) /
                                        max(self.rocket.calculate_escape_velocity(start_planet),
                                            self.rocket.calculate_escape_velocity(dest_planet)))
                time_to_reach_planet_days = time_to_reach_planet / (24 * 3600)


                planet_position_at_crossing = planet.calculate_angular_position(start_time + time_to_reach_planet_days)


                time_to_travel_radius = (planet.diameter / 2) / planet.orbiting_speed  # in seconds
                time_to_travel_radius_days = time_to_travel_radius / (24 * 3600)

                angular_displacement = (360 / planet.period) * time_to_travel_radius_days

                planet_first_touch = planet_position_at_crossing - angular_displacement
                planet_last_touch = planet_position_at_crossing + angular_displacement

                if (planet_first_touch <= start_angular_position <= planet_last_touch) or \
                        (planet_last_touch < planet_first_touch and (
                                start_angular_position >= planet_first_touch or start_angular_position <= planet_last_touch)):
                    return True

            return False

    def find_optimal_transfer_window(self, start_planet: Planet, dest_planet: Planet, start_time_years: int , start_time_days:int):

        start_orbiting_speed = 360 / start_planet.period#degrees per day
        dest_orbiting_speed = 360 / dest_planet.period#degrees per day
        self.simulate_solar_system(start_time_years, start_time_days)

        start_angular_pos = start_planet.current_angular_position
        dest_angular_pos = dest_planet.current_angular_position

        rocket_travel_data = self.rocket.travel(start_planet, dest_planet)
        rocket_travel_time_days = rocket_travel_data[5] / (24 * 3600)

        # We're solving for t such that:
        # start_angular_pos + start_orbiting_speed * t ≡ dest_angular_pos + dest_orbiting_speed * (t + travel_time) (mod 360)

        # Rearranged:
        # (start_orbiting_speed - dest_orbiting_speed) * t ≡ (dest_angular_pos + dest_orbiting_speed * travel_time - start_angular_pos) % 360

        relative_velocity = start_orbiting_speed - dest_orbiting_speed
        angle_offset = (dest_angular_pos + dest_orbiting_speed * rocket_travel_time_days - start_angular_pos) % 360

        # We solve for the smallest t such that the above holds true within 10 years
        max_days = 365 * 10
        t = 0
        found = False
        while t <= max_days:
            if abs((relative_velocity * t) % 360 - angle_offset) < 0.1:
                found = True
                break
            t += 1  # increment by 1 day

        if found:
            print(f'Optimal transfer window found: Launch on day {t}')
            return t
        else:
            print('No optimal transfer window found in the next 10 years.')
            return None

    def read_system_data(self):
        try:
            file = open(self.system_filepath, 'r')
        except:
            raise Exception

        for line in file.readlines():

            line = line.strip().split(':')

            line[1] = line[1].split(',')
            line[1][0] = float("".join(c for c in line[1][0] if c.isnumeric() or c == '.'))
            line[1][1] = float("".join(c for c in line[1][1] if c.isnumeric() or c == '.'))

            for planet in self.planets:
                if planet.name == line[0]:
                    planet.period = line[1][0]
                    planet.orbital_radius = line[1][1]

    def read_planetary_data(self):
        try:
            file = open(self.planet_filepath, 'r')
        except:
            raise Exception

        for line in file.readlines():

            line = line.strip().split(':')
            line[1] = line[1].split(',')
            line[1][0] = float("".join(c for c in line[1][0] if c.isnumeric() or c == '.'))

            planet = Planet()
            planet.name = line[0]
            planet.diameter = float(line[1][0])
            if 'Earths' in line[1][1]:
                line[1][1] = float("".join(c for c in line[1][1] if c.isnumeric() or c == '.'))
                planet.mass = float(line[1][1] * EARTH_MASS)

            else:
                planet.mass = EARTH_MASS

            self.planets.append(planet)

    def write_planetary_escape_data(self):
        try:
            file = open("Planetary_Escape_Data.txt", 'w')

            for planet_name in self.planet_escape_data.keys():
                file.write(f'{planet_name}: Velocity: {self.planet_escape_data[planet_name][0]} m/s \n'
                           f'Distance: {self.planet_escape_data[planet_name][1]} m\n'
                           f'Time: {self.planet_escape_data[planet_name][2]} s\n\n')
        except:
            raise Exception



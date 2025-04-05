import sys

from PyQt5.QtWidgets import QApplication
from App_GUI import SpaceAppGUI


def main():

    app = QApplication(sys.argv)
    window = SpaceAppGUI()
    window.show()
    sys.exit(app.exec_())


    # app = Space_App("Planetary_Data.txt", "Rocket_Data.txt", "Solar_System_Data.txt")
    # print(calculate_escape_velocity(12800 / 2 * pow(10,3), 6 * pow(10,24)))
    # app.rocket.travel(app.planets[2], app.planets[3]) #Earth, Mars
    # app.rocket.travel(app.planets[3], app.planets[2]) #Mars, Earth
    # app.write_planetary_escape_data()
    # app.planetary_angular_position = app.simulate_solar_system(100,0)
    #
    # app.planets[3].calculate_orbiting_speed()
    # print(app.planets[3].orbiting_speed)
    # print(app.find_optimal_transfer_window(app.planets[3], app.planets[2],100,0))#Mars, Earth
    # app.simulate_solar_system(100,708)
    # print(app.calculate_intermediary_planets(app.planets[5], app.planets[1]))
    # print(app.calculate_distance_to_escape_velocity("Earth", 0))

main()
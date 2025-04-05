from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog,
    QComboBox, QSpinBox, QTextEdit, QHBoxLayout
)

from App import Space_App
import sys

class SpaceAppGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Space App")
        self.setGeometry(100, 100, 800, 600)

        self.app = Space_App("Planetary_Data.txt", "Rocket_Data.txt", "Solar_System_Data.txt")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.start_combo = QComboBox()
        self.dest_combo = QComboBox()

        self.update_planet_dropdown()

        planet_layout = QHBoxLayout()
        planet_layout.addWidget(QLabel("Start Planet:"))
        planet_layout.addWidget(self.start_combo)
        planet_layout.addWidget(QLabel("Destination Planet:"))
        planet_layout.addWidget(self.dest_combo)
        layout.addLayout(planet_layout)

        self.years_spin = QSpinBox()
        self.years_spin.setRange(0, 10000)
        self.years_spin.setPrefix("Years: ")

        self.days_spin = QSpinBox()
        self.days_spin.setRange(0, 365)
        self.days_spin.setPrefix("Days: ")

        date_layout = QHBoxLayout()
        date_layout.addWidget(self.years_spin)
        date_layout.addWidget(self.days_spin)
        layout.addLayout(date_layout)

        escape_btn = QPushButton("Stage 1: Show Escape Velocities")
        escape_btn.clicked.connect(self.show_escape_velocities)

        reach_btn = QPushButton("Stage 2: Reach Escape Velocity")
        reach_btn.clicked.connect(self.show_escape_stats)

        journey_btn = QPushButton("Stage 3–4: Simulate Travel")
        journey_btn.clicked.connect(self.simulate_journey)

        angular_btn = QPushButton("Stage 4: Show Angular Positions")
        angular_btn.clicked.connect(self.show_angular_positions)

        transfer_btn = QPushButton("Stage 5–6: Optimal Transfer Window")
        transfer_btn.clicked.connect(self.find_transfer_window)

        layout.addWidget(escape_btn)
        layout.addWidget(reach_btn)
        layout.addWidget(journey_btn)
        layout.addWidget(angular_btn)
        layout.addWidget(transfer_btn)

        self.output = QTextEdit()
        self.output.setReadOnly(True)
        layout.addWidget(self.output)

        self.setLayout(layout)

    def update_planet_dropdown(self):
        self.start_combo.clear()
        self.dest_combo.clear()
        for planet in self.app.planets:
            self.start_combo.addItem(planet.name)
            self.dest_combo.addItem(planet.name)

    def get_planet_by_name(self, name):
        for planet in self.app.planets:
            if planet.name == name:
                return planet
        return None

    def show_escape_velocities(self):
        self.output.append("Escape Velocities:")
        for planet in self.app.planets:
            v = self.app.rocket.calculate_escape_velocity(planet)
            self.output.append(f"{planet.name}: {v:.2f} m/s")
        self.output.append("")

    def show_escape_stats(self):
        self.output.append("Rocket Launch Stats (Stage 2):")
        for planet in self.app.planets:
            t = self.app.rocket.calculate_time_to_escape_velocity(planet)
            d = self.app.rocket.calculate_distance_to_escape_velocity(planet, 0)
            self.output.append(f"{planet.name}: Time = {t} s, Distance = {d/1000:.2f} km")
        self.output.append("")

    def simulate_journey(self):
        start_name = self.start_combo.currentText()
        dest_name = self.dest_combo.currentText()

        start = self.get_planet_by_name(start_name)
        dest = self.get_planet_by_name(dest_name)

        self.output.append(f"Simulating travel from {start_name} to {dest_name}:")
        rocket_travel_data = self.app.rocket.travel(start, dest)
        self.output.append(f'Time to cruising velocity from {start.name}: {rocket_travel_data[0]} seconds')
        self.output.append(f'Distance to cruising velocity from {start.name}: {rocket_travel_data[1]} km')
        self.output.append(f'Time of nominal velocity: {rocket_travel_data[2]} seconds')
        self.output.append(f'Distance from {dest.name} surface to begin deceleration burn : {rocket_travel_data[3]} km')
        self.output.append(f'Deceleration time when reaching {dest.name}: {rocket_travel_data[4]} seconds')

        total_travel_time = rocket_travel_data[0] + rocket_travel_data[4] + rocket_travel_data[2] #in seconds
        aux = total_travel_time

        total_travel_time_days_hours_sec = '' + f'{int(aux / 86400)} days '  # in days
        aux = aux % 86400

        total_travel_time_days_hours_sec = total_travel_time_days_hours_sec + f'{int(aux / 3600)} hours '# in hours
        aux = aux % 3600

        total_travel_time_days_hours_sec = total_travel_time_days_hours_sec + f'{int(aux)} seconds ' #in seconds
        self.output.append(f'Total travel time aproximation: {total_travel_time_days_hours_sec}\n')


    def show_angular_positions(self):
        years = self.years_spin.value()
        days = self.days_spin.value()
        self.output.append(f"Angular Positions after {years} years and {days} days:")
        self.app.simulate_solar_system(years, days)
        for planet in self.app.planets:
            self.output.append(f"{planet.name}: {planet.current_angular_position:.2f}°")
        self.output.append("")

    def find_transfer_window(self):
        start_name = self.start_combo.currentText()
        dest_name = self.dest_combo.currentText()

        start = self.get_planet_by_name(start_name)
        dest = self.get_planet_by_name(dest_name)

        years = self.years_spin.value()
        days = self.days_spin.value()

        result = self.app.find_optimal_transfer_window(start, dest, years, days)
        if result is not None:
            self.output.append(f"Optimal transfer window: Launch in {result} days")
        else:
            self.output.append("No optimal transfer window found in the next 10 years.")
        self.output.append("")

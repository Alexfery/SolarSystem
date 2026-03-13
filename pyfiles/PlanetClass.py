import re
import numpy as np

class Planet:

    def __init__(self, name, diameter, mass):
        self.name = name
        self.diameter = diameter * 1000
        self.mass = mass

    def __str__(self):
        return f"{self.name} {self.diameter/1000}km {self.mass} kg \n -------------------------------------------------"

    G = 6.67 * np.power(10.0, -11.0)
    @classmethod
    def time_distance(planet, total_thrust):
        v = planet.showEscPlanetsVelocity(planet)
        g = planet.surface_gravity(planet)
        a = total_thrust - g
        if a <= 0:
            return None, None
        t = v / a
        d = (v ** 2) / (2 * a)
        return t, d

    @classmethod
    def surface_gravity(planet):
        r = planet.diameter / 2
        return planet.G * planet.mass / (r ** 2)

    @classmethod
    def showEscPlanetsVelocity(cls, planets):

        for planet in planets:
            v = np.sqrt(2*planet.G*planet.mass/planet.diameter*2)
            print(f"{planet.name:<10}  v = {v:.2e} m/s")
            return v


    @classmethod
    def display_planets(cls, planets):
        print("\n--- Planet List ---")
        for planet in planets:
            print(planet)

    @classmethod
    def parse_planets(cls, filename: str) -> list:
        EARTH_DIAMETER_KM = None
        EARTH_MASS_KG = None
        raw_lines = []

        # 1: read file & extract Earth's values
        with open(filename, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                raw_lines.append(line)

                if line.lower().startswith("earth:"):
                    diam_match = re.search(r"diameter\s*=\s*([\d.]+)\s*km", line)
                    if diam_match:
                        EARTH_DIAMETER_KM = float(diam_match.group(1))

                    mass_match = re.search(r"mass\s*=\s*([\d.]+)\s*\*\s*10\^([\d]+)\s*kg", line)
                    if mass_match:
                        EARTH_MASS_KG = float(mass_match.group(1)) * (10 ** int(mass_match.group(2)))

        if EARTH_DIAMETER_KM is None or EARTH_MASS_KG is None:
            raise ValueError("Could not extract Earth's reference values.")
        # 2: pars every line and create Planet
        planets = []

        for line in raw_lines:
            name_match = re.match(r"^(\w+):\s*(.+)$", line)
            if not name_match:
                continue
            name = name_match.group(1)
            data = name_match.group(2)

            # Diameter (km)
            diam_match = re.search(r"diameter\s*=\s*([\d.]+)\s*km", data)
            diameter_km = float(diam_match.group(1)) if diam_match else 0.0

            # Masă — fie absolută (X * 10^Y kg), fie relativă (X Earths)
            mass_abs = re.search(r"mass\s*=\s*([\d.]+)\s*\*\s*10\^([\d]+)\s*kg", data)
            mass_rel = re.search(r"mass\s*=\s*([\d.]+)\s*Earths", data)

            if mass_abs:
                mass_kg = float(mass_abs.group(1)) * (10 ** int(mass_abs.group(2)))
            elif mass_rel:
                mass_kg = float(mass_rel.group(1)) * EARTH_MASS_KG
            else:
                mass_kg = 0.0

            # diameter_km e pasat direct — constructorul face *1000 intern
            planets.append(Planet(name, diameter_km, mass_kg))

        return planets
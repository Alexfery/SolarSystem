from pyfiles import PlanetClass
from pyfiles import PlanetClass
import re

class Rocket:

    @classmethod
    def parse_rocket(cls, filename: str) -> dict:
        rocket = {}
        with open(filename, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                # extrage primul număr din linie
                numbers = re.findall(r"[\d.]+", line)
                if "engine" in line.lower() and "number" in line.lower():
                    rocket["engines"] = float(numbers[0])
                elif "acceleration" in line.lower():
                    rocket["engine_thrust"] = float(numbers[0])
        return rocket

    @classmethod
    def calc_surface_gravity(cls, planet):
        r = planet.diameter / 2
        g = PlanetClass.G * planet.mass / (r ** 2)
        return g



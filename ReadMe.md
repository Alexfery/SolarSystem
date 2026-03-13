# 🚀 Rocket Project — Solar System Explorer

A Python application that simulates rocket escape velocity calculations for planets in our Solar System, with an interactive Tkinter UI.

---

## 📁 Project Structure

```
Rocket_Project/
├── pyfiles/
│   ├── PlanetClass.py       # Planet class with parsing and physics methods
│   ├── Rocket.py            # Rocket class with physics calculations
│   ├── UI.py                # Tkinter Solar System UI
│   └── Main.py              # Console menu entry point
├── res/
│   ├── Planetary_Data.txt   # Planet data input file
│   └── Rocket_Data.txt      # Rocket engine configuration
└── README.md
```

---

## 📄 Input Files

### `Planetary_Data.txt`
Contains planet data in the following format:
```
Mercury: diameter = 4900 km, mass = 0.06 Earths
Venus: diameter = 12100 km, mass = 0.82 Earths
Earth: diameter = 12800 km, mass = 6 * 10^24 kg
Mars: diameter = 5800 km, mass = 0.11 Earths
...
```
- Masses are expressed either in **absolute** form (`X * 10^Y kg`) or **relative** to Earth (`X Earths`)
- Earth's values are used as the reference for all relative mass calculations

### `Rocket_Data.txt`
Contains rocket engine configuration:
```
engines = 4
engine_thrust = 10
```
- `engines` — number of rocket engines
- `engine_thrust` — acceleration per engine in m/s²
- Total thrust = `engines × engine_thrust` (e.g. 4 × 10 = **40 m/s²**)

---

## 🐍 Classes

### `Planet` (`PlanetClass.py`)

| Method | Type | Description |
|--------|------|-------------|
| `__init__(name, diameter, mass)` | instance | Creates a planet; diameter stored in **meters** (km × 1000) |
| `__str__()` | instance | Returns formatted string with name, diameter, mass |
| `parse_planets(filename)` | `@classmethod` | Reads `Planetary_Data.txt` and returns a list of `Planet` objects |
| `showPlanetsVelocity(planets)` | `@classmethod` | Prints escape velocity for each planet |

### `Rocket` (`Rocket.py`)

| Method | Type | Description |
|--------|------|-------------|
| `parse_rocket(filename)` | `@classmethod` | Reads `Rocket_Data.txt` and returns a dict with engine config |
| `calc_surface_gravity(planet)` | `@classmethod` | Calculates surface gravity: `g = GM/r²` |

---

## ⚙️ Physics

### Constants
```python
G = 6.67 × 10⁻¹¹  # Gravitational constant (m³/kg/s²)
```

### Formulas

| Formula | Description |
|---------|-------------|
| `v = √(2GM/r)` | Escape velocity from planet surface |
| `g = GM/r²` | Surface gravitational acceleration |
| `a = thrust - g` | Net rocket acceleration |
| `t = v / a` | Time to reach escape velocity |
| `d = v² / 2a` | Distance travelled to reach escape velocity |

> ⚠️ Assumptions: constant gravitational pull regardless of altitude, no air resistance, infinite fuel with no mass, linear gravity model.

---

## 🖥️ Running the Application

### Console Menu (`Main.py`)
```bash
python pyfiles/Main.py
```
Options:
1. List planets
2. List planets with escape velocity
3. Time & distance to reach escape velocity
0. Exit

### Solar System UI (`UI.py`)
```bash
python pyfiles/UI.py
```
Requires `tkinter`:
```bash
# Linux
sudo apt-get install python3-tk

# macOS
brew install python-tk
```

---

## 📦 Dependencies

```bash
pip install numpy
```

| Package | Usage |
|---------|-------|
| `numpy` | Mathematical calculations (`np.sqrt`, `np.power`) |
| `tkinter` | Graphical UI (built into Python on Windows/macOS) |
| `re` | Regex parsing of input files |

---

## 🪐 UI Features

- Animated Solar System with planets orbiting the Sun
- Click any planet to view its stats in the detail panel
- **PLANETS tab** — diameter, mass, escape velocity
- **ROCKET tab** — surface gravity, net acceleration, time and distance to escape
- Pause / Play animation toggle
- Saturn ring rendering
- Starfield background

---

## 📐 Example Output

```
===== MENU =====
1. List planets
2. List planets with escape velocity
3. Time & distance to reach escape velocity
0. Exit

--- Planets with Escape Velocity ---
Mercury     v = 4.18e+03 m/s
Venus       v = 1.04e+04 m/s
Earth       v = 1.12e+04 m/s
Mars        v = 5.03e+03 m/s
Jupiter     v = 6.03e+04 m/s
```
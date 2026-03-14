import tkinter as tk
import math
from pyfiles.PlanetClass import Planet as pc
from pyfiles.Rocket import Rocket
# ── constants ────────────────────────────────────────────────────────────────
G = 6.67e-11

PLANET_COLORS = {
    "Mercury": "#b5b5b5",
    "Venus":   "#e8cda0",
    "Earth":   "#4fa3e0",
    "Mars":    "#c1440e",
    "Jupiter": "#c88b3a",
    "Saturn":  "#e4d191",
    "Uranus":  "#7de8e8",
    "Neptune": "#4b70dd",
    "Pluto":   "#a89f94",
}

PLANET_SIZES = {
    "Mercury": 4,
    "Venus":   9,
    "Earth":   10,
    "Mars":    6,
    "Jupiter": 22,
    "Saturn":  18,
    "Uranus":  13,
    "Neptune": 12,
    "Pluto":   3,
}

ORBIT_RADII = {
    "Mercury": 70,
    "Venus":   105,
    "Earth":   145,
    "Mars":    185,
    "Jupiter": 250,
    "Saturn":  310,
    "Uranus":  360,
    "Neptune": 405,
    "Pluto":   440,
}

ORBIT_SPEEDS = {
    "Mercury": 4.0,
    "Venus":   2.8,
    "Earth":   2.2,
    "Mars":    1.7,
    "Jupiter": 1.1,
    "Saturn":  0.8,
    "Uranus":  0.6,
    "Neptune": 0.45,
    "Pluto":   0.35,
}

# ── main app ─────────────────────────────────────────────────────────────────

class SolarApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Solar System Explorer")
        self.configure(bg="#050a18")
        self.geometry("1200x700")
        self.resizable(True, True)

        # load data
        try:
            self.planets = pc.parse_planets("res/Planetary_Data.txt")
        except FileNotFoundError:
            self.planets = self._demo_planets()

        try:
            self.rocket = Rocket.parse_rocket("res/Rocket_Data.txt")
        except FileNotFoundError:
            self.rocket = {"engines": 4, "engine_thrust": 10}

        self.total_thrust = self.rocket["engines"] * self.rocket["engine_thrust"]
        self.angles = {p.name: i * (360 / len(self.planets))
                       for i, p in enumerate(self.planets)}
        self.selected = None
        self.animating = True

        self._build_ui()
        self._animate()

    # ── demo planets if file missing ─────────────────────────────────────────
    def _demo_planets(self):
        data = [
            ("Mercury", 4900,   3.30e23),
            ("Venus",   12100,  4.87e24),
            ("Earth",   12800,  5.97e24),
            ("Mars",    6780,   6.39e23),
            ("Jupiter", 142800, 1.90e27),
            ("Saturn",  120000, 5.68e26),
            ("Uranus",  51118,  8.68e25),
            ("Neptune", 49528,  1.02e26),
            ("Pluto",   2376,   1.30e22),
        ]
        return [pc.Planet(n, d, m) for n, d, m in data]

    # ── UI layout ─────────────────────────────────────────────────────────────
    def _build_ui(self):
        # left panel — solar system canvas
        self.canvas = tk.Canvas(self, bg="#050a18", highlightthickness=0, width=700)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # right panel
        right = tk.Frame(self, bg="#090f24", width=420)
        right.pack(side=tk.RIGHT, fill=tk.BOTH)
        right.pack_propagate(False)

        # title
        tk.Label(right, text="SOLAR SYSTEM", bg="#090f24", fg="#e8c96e",
                 font=("Courier", 18, "bold")).pack(pady=(20, 2))
        tk.Label(right, text="E X P L O R E R", bg="#090f24", fg="#4a7ab5",
                 font=("Courier", 10, "bold")).pack(pady=(0, 15))

        # tab bar
        tab_frame = tk.Frame(right, bg="#090f24")
        tab_frame.pack(fill=tk.X, padx=10)

        self.tab_var = tk.StringVar(value="planets")
        for label, val in [("PLANETS", "planets"), ("ROCKET", "rocket")]:
            tk.Radiobutton(tab_frame, text=label, variable=self.tab_var, value=val,
                           command=self._switch_tab,
                           bg="#090f24", fg="#7a9fd4", selectcolor="#0d1a3a",
                           activebackground="#090f24", activeforeground="#e8c96e",
                           font=("Courier", 9, "bold"), indicatoron=False,
                           relief=tk.FLAT, padx=16, pady=6,
                           borderwidth=0).pack(side=tk.LEFT)

        sep = tk.Frame(right, bg="#1a2a4a", height=1)
        sep.pack(fill=tk.X, padx=10, pady=4)

        # scrollable table area
        self.table_frame = tk.Frame(right, bg="#090f24")
        self.table_frame.pack(fill=tk.BOTH, expand=True, padx=10)

        # detail panel at bottom
        self.detail_frame = tk.Frame(right, bg="#0d1a3a", height=160)
        self.detail_frame.pack(fill=tk.X, padx=10, pady=10)
        self.detail_frame.pack_propagate(False)

        self.detail_label = tk.Label(self.detail_frame,
                                     text="Click a planet to see details",
                                     bg="#0d1a3a", fg="#4a7ab5",
                                     font=("Courier", 9), justify=tk.LEFT,
                                     wraplength=380)
        self.detail_label.pack(padx=12, pady=12, anchor=tk.W)

        # toggle animation button
        btn_frame = tk.Frame(right, bg="#090f24")
        btn_frame.pack(fill=tk.X, padx=10, pady=(0, 12))
        tk.Button(btn_frame, text="⏸  PAUSE / PLAY",
                  command=self._toggle_anim,
                  bg="#1a2a4a", fg="#e8c96e",
                  font=("Courier", 9, "bold"),
                  relief=tk.FLAT, padx=10, pady=6,
                  activebackground="#2a3a6a",
                  activeforeground="#ffffff",
                  cursor="hand2").pack(fill=tk.X)

        self._build_table()

    # ── table ─────────────────────────────────────────────────────────────────
    def _build_table(self):
        for w in self.table_frame.winfo_children():
            w.destroy()

        mode = self.tab_var.get()

        if mode == "planets":
            headers = ["Planet", "Diameter (km)", "Mass (kg)", "Esc. Vel (m/s)"]
        else:
            headers = ["Planet", "Surface g", "Net a (m/s²)", "Time (s)", "Dist (km)"]

        # header row
        hf = tk.Frame(self.table_frame, bg="#0d1a3a")
        hf.pack(fill=tk.X, pady=(4, 2))
        for i, h in enumerate(headers):
            tk.Label(hf, text=h, bg="#0d1a3a", fg="#e8c96e",
                     font=("Courier", 8, "bold"),
                     width=max(10, len(h)+2), anchor=tk.W).grid(row=0, column=i, padx=4)

        # planet rows
        for p in self.planets:
            color = PLANET_COLORS.get(p.name, "#ffffff")
            rf = tk.Frame(self.table_frame, bg="#090f24", cursor="hand2")
            rf.pack(fill=tk.X, pady=1)
            rf.bind("<Enter>",  lambda e, f=rf: f.configure(bg="#0d1a3a"))
            rf.bind("<Leave>",  lambda e, f=rf: f.configure(bg="#090f24"))
            rf.bind("<Button-1>", lambda e, pl=p: self._select_planet(pl))

            v = p.showEscPlanetsVelocity();
            g = p.surface_gravity()
            thrust = self.total_thrust
            a_net = thrust - g
            t, d = p.time_distance(self.total_thrust)

            if mode == "planets":
                vals = [p.name,
                        f"{p.diameter/1000:,.0f}",
                        f"{p.mass:.3e}",
                        f"{v:.2e}"]
            else:
                vals = [p.name,
                        f"{g:.2f}",
                        f"{a_net:.2f}" if a_net > 0 else "N/A",
                        f"{t:.1f}" if t else "∞",
                        f"{d/1000:.1f}" if d else "∞"]

            for i, val in enumerate(vals):
                lbl = tk.Label(rf, text=val, bg="#090f24", fg=color if i == 0 else "#c8d8f0",
                               font=("Courier", 8),
                               width=max(10, len(headers[i])+2), anchor=tk.W)
                lbl.grid(row=0, column=i, padx=4, pady=3)
                lbl.bind("<Button-1>", lambda e, pl=p: self._select_planet(pl))
                lbl.bind("<Enter>",  lambda e, f=rf: f.configure(bg="#0d1a3a"))
                lbl.bind("<Leave>",  lambda e, f=rf: f.configure(bg="#090f24"))

    # ── detail panel ─────────────────────────────────────────────────────────
    def _select_planet(self, planet):
        self.selected = planet.name
        v = planet.escape_velocity()
        g = planet.surface_gravity()
        t, d = planet.time_distance(self.total_thrust)
        a_net = self.total_thrust - g

        t_str = f"{t:.2f} s"   if t else "Cannot escape!"
        d_str = f"{d/1000:.2f} km" if d else "N/A"

        text = (
            f"  ● {planet.name.upper()}\n\n"
            f"  Diameter      : {planet.diameter/1000:,.0f} km\n"
            f"  Mass          : {planet.mass:.3e} kg\n"
            f"  Surface g     : {g:.2f} m/s²\n"
            f"  Escape vel.   : {v:.2e} m/s\n"
            f"  Net accel.    : {a_net:.2f} m/s²\n"
            f"  Time to escape: {t_str}\n"
            f"  Distance      : {d_str}"
        )
        color = PLANET_COLORS.get(planet.name, "#ffffff")
        self.detail_label.configure(text=text, fg=color)

    def _switch_tab(self):
        self._build_table()

    def _toggle_anim(self):
        self.animating = not self.animating
        if self.animating:
            self._animate()

    # ── animation ────────────────────────────────────────────────────────────
    def _animate(self):
        self.canvas.delete("all")
        w = self.canvas.winfo_width()  or 700
        h = self.canvas.winfo_height() or 700
        cx, cy = w // 2, h // 2

        # starfield (static seed)
        for i in range(120):
            sx = (i * 97 + 13) % w
            sy = (i * 53 + 7)  % h
            r  = 1 if i % 3 else 2
            br = ["#ffffff", "#aaccff", "#ffeecc"][i % 3]
            self.canvas.create_oval(sx-r, sy-r, sx+r, sy+r, fill=br, outline="")

        # sun glow
        for gr, ga in [(40, "#1a0a00"), (28, "#2a1000"), (18, "#ff6600"), (10, "#ffaa00"), (6, "#ffdd44")]:
            self.canvas.create_oval(cx-gr, cy-gr, cx+gr, cy+gr, fill=ga, outline="")

        # orbits + planets
        for planet in self.planets:
            orb_r = ORBIT_RADII.get(planet.name, 200)
            spd   = ORBIT_SPEEDS.get(planet.name, 1.0)
            color = PLANET_COLORS.get(planet.name, "#ffffff")
            size  = PLANET_SIZES.get(planet.name, 8)

            # orbit ring
            self.canvas.create_oval(cx - orb_r, cy - orb_r,
                                     cx + orb_r, cy + orb_r,
                                     outline="#1a2a4a", width=1)

            # planet position
            angle_deg = self.angles.get(planet.name, 0)
            angle_rad = math.radians(angle_deg)
            px = cx + orb_r * math.cos(angle_rad)
            py = cy + orb_r * math.sin(angle_rad)

            # highlight selected
            if self.selected == planet.name:
                self.canvas.create_oval(px - size - 4, py - size - 4,
                                         px + size + 4, py + size + 4,
                                         outline="#e8c96e", width=2)

            # planet circle
            self.canvas.create_oval(px - size, py - size,
                                     px + size, py + size,
                                     fill=color, outline="")

            # Saturn rings
            if planet.name == "Saturn":
                self.canvas.create_oval(px - size*2, py - size*0.5,
                                         px + size*2, py + size*0.5,
                                         outline="#c8b060", width=2)

            # label
            self.canvas.create_text(px, py - size - 8,
                                     text=planet.name,
                                     fill="#7a9fd4",
                                     font=("Courier", 7))

            # bind click
            tag = f"planet_{planet.name}"
            self.canvas.create_oval(px - size - 6, py - size - 6,
                                     px + size + 6, py + size + 6,
                                     fill="", outline="", tags=tag)
            self.canvas.tag_bind(tag, "<Button-1>",
                                  lambda e, pl=planet: self._select_planet(pl))

            # advance angle
            if self.animating:
                self.angles[planet.name] = (angle_deg + spd * 0.5) % 360

        if self.animating:
            self.after(30, self._animate)


# ── entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = SolarApp()
    app.mainloop()
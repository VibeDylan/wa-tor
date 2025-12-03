import tkinter as tk

class PlanetUI:
    def __init__(self, planet, cell_size=25):
        self.planet = planet
        self.cell_size = cell_size
        
        self.chronon = 0;
        self.running = False

        self.root = tk.Tk()
        self.root.title("Wa-Tor Simulation")

        self.canvas = tk.Canvas(
            self.root,
            width=self.planet.width * cell_size,
            height=self.planet.height * cell_size,
            bg="white"
        )
        self.canvas.grid(row=0, column=0, padx=10, pady=10)

        self.sidebar = tk.Frame(self.root)
        self.sidebar.grid(row=0, column=1, padx=10, pady=10, sticky="n")

        self.label_chronon = tk.Label(self.sidebar, text="Chronon : 0", font=("Arial", 14))
        self.label_chronon.pack(anchor="w", pady=5)

        self.label_fish = tk.Label(self.sidebar, text="Fish alive : 0", font=("Arial", 14))
        self.label_fish.pack(anchor="w", pady=5)

        self.label_shark = tk.Label(self.sidebar, text="Shark alive : 0", font=("Arial", 14))
        self.label_shark.pack(anchor="w", pady=5)
        
        self.button_start = tk.Button(self.sidebar, text="Start", command=self.start)
        self.button_start.pack(fill="x", pady=5)

        self.button_pause = tk.Button(self.sidebar, text="Pause", command=self.pause)
        self.button_pause.pack(fill="x", pady=5)

        self.button_reset = tk.Button(self.sidebar, text="Reset", command=self.reset)
        self.button_reset.pack(fill="x", pady=5)

    def draw_grid(self):
        self.canvas.delete("all")

        for y in range(self.planet.height):
            for x in range(self.planet.width):
                cell = self.planet.get(x, y)

                # TEMPORAIRE : on affiche juste un carré vide le temps que fish et shark n'existe pas 
                color = "white" if cell is None else "gray"

                self.canvas.create_rectangle(
                    x * self.cell_size,
                    y * self.cell_size,
                    (x + 1) * self.cell_size,
                    (y + 1) * self.cell_size,
                    fill=color,
                    outline="black"
                )

    def update_counters(self, chronon, fish_count, shark_count):
        self.label_chronon.config(text=f"Chronon : {chronon}")
        self.label_fish.config(text=f"Fish alive : {fish_count}")
        self.label_shark.config(text=f"Shark alive : {shark_count}")

    def refresh(self):
        self.draw_grid()
        self.root.update()
        
    def start(self):
        """Lance la simulation (si pas déjà en cours)."""
        if not self.running:
            self.running = True
            self._run_loop()

    def pause(self):
        """Met la simulation en pause."""
        self.running = False

    def reset(self):
        """Réinitialise la simulation."""
        # Arrêter si ça tourne
        self.running = False

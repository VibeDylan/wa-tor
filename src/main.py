import time

from wator.planet import Planet
from wator.ui import PlanetUI

planet = Planet(20, 20)
ui = PlanetUI(planet)

chronon = 0

while True:
    chronon += 1

    # Faux nombres en attendant Fish / Shark
    fish_alive = 10
    shark_alive = 3

    ui.update_counters(chronon, fish_alive, shark_alive)
    ui.refresh()

    time.sleep(0.3)

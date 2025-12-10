from __future__ import annotations

import tkinter as tk
from .simulation import initiate_grid

root = tk.Tk(baseName="Wa-Tor", className="Tk")
root.title("Wa-Tor")
root.geometry("800x600")

count_frame = tk.Frame(root)

chronon_count = tk.Label(count_frame, text="Chronon n° ")
fish_count = tk.Label(count_frame, text="Fishes : ")
shark_count = tk.Label(count_frame, text="Sharks : ")

chronon_count.grid(row=0, column=0)
fish_count.grid(row=0, column=1)
shark_count.grid(row=0, column=2)


canvas = tk.Canvas(root, height=500)

planet = initiate_grid()

for column in range(planet.width):
    for row in range(planet.height):
        cell = planet.get(column, row)
        if cell is None:
            canvas.create_rectangle(row*15, column*15, (row*15)+15, (column*15)+15, fill="skyblue", outline="")
        elif cell.name == "shark":
            canvas.create_text((row*15)+15, (column*15)+15, text="\U0001F988")
        else:
            canvas.create_text((row*15)+15, (column*15)+15, text="\U0001F420")



buttons_frame = tk.Frame(root)

button_start = tk.Button(buttons_frame, text="Start")
button_pause = tk.Button(buttons_frame, text="Pause")
button_history = tk.Button(buttons_frame, text="Historique")

button_start.grid(row=0, column=0)
button_pause.grid(row=0, column=1)
button_history.grid(row=0, column=2)


count_frame.pack()
canvas.pack()
buttons_frame.pack()




root.mainloop()
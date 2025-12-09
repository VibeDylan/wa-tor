grid_width = 200
grid_height = 100
number_fishes = 60
number_sharks = 30
fish_reproduction = 2
shark_reproduction = 15
shark_energy = 10
shark_energy_gain = 3


# Ratio : Fish = Shark * 2

# 30x20 -> pas assez d'espace, résultats trop aléatoires

# 50x50 - 5 Shark - 10 Fish
# -> 15467 (not finished)
# -> 6063 (not finished)

# 80x50 - 10 Shark - 20 Fish
# -> 3101 (not finished)
# -> 3009 (not finished)
# -> failed

# 80x50 - 15 Shark - 30 Fish
# -> no early failure

# 100x50 - 15 Shark - 30 Fish
# -> no early failure

# 200x100 - 15 Shark - 30 Fish
# -> early failure --> more population

# 200x100 - 30 Shark - 60 Fish
# -> no early failure
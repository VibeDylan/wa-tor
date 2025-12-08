grid_width = 80
grid_height = 50
number_fishes = 30
number_sharks = 15
fish_reproduction = 2
shark_reproduction = 15
shark_energy = 10
shark_energy_gain = 3


# Ratio : Fish = Shark * 2

# 30x20 -> pas assez d'espace, résultats trop aléatoires

# 50x50 - 7 Fish (rep 2) - 3 Shark (rep 15, energy 10, eat +3)
# -> 5924 chronons (not finished)
# -> 5116 chronons (not finished)

# 50x50 - 10 Fish - 5 Shark
# -> 15467 (not finished)
# -> 6063 (not finished)

# 100x50 - 14 Fish - 7 Shark
# -> crash
# -> 3746 (not finished)
# -> failed twice (sharks couldn't eat) --> more population ?
# -> 5059 (not finished)

# 100x50 - 20 Fish - 10 Shark
# -> 4535 (not finished)

# 80x50 - 8 Shark - 16 Fish
# -> 4943 (not finished)
# -> 3496 (not finished)
# -> failed twice (sharks couldn't eat) --> more population ?
# -> 3356 (not finished)

# 80x50 - 10 Shark - 20 Fish
# -> 3101 (not finished)
# -> 3009 (not finished)
# -> failed

# 80x50 - 15 Shark - 30 Fish
# -> no early failure
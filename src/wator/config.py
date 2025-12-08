grid_width = 100
grid_height = 50
number_fishes = 20
number_sharks = 10
fish_reproduction = 2
shark_reproduction = 15
shark_energy = 10
shark_energy_gain = 3


# 30x20 -> pas assez d'espace, résultats trop aléatoires

# 50x50 - 7 Fish (rep 2) - 3 Shark (rep 15, energy 10, eat +3)
# -> 5924 chronons (not finished)
# -> 5116 chronons (not finished)

# 100x50 - 14 Fish (rep 2) - 7 Shark (rep 15, energy 10, eat +3)
# -> crash
# -> 3746 (not finished)
# 2 failed tries (sharks failed to eat fish before dying)
# -> 5059 (not finished)

# 100x50 - Same with 20 Fish - 10 Shark
# -> 4535 (not finished)
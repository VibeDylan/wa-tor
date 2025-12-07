from __future__ import annotations
import random

from typing import Union
from .planet import Planet
from .fish import Fish
from .shark import Shark


def display_grid(planet: 'Planet') -> None:
	print((planet.width*4+4)*"-")
	print(f"  ", end='')
	for j in range(planet.width):
		print(f"| {j} ", end='')
	print("| ")
	print((planet.width*4+4)*"-")

	for row in range(planet.height):
		print(f"{row} ", end='')
		for column in range(planet.width):
			if type(planet.get(column, row)) == Fish:
				print(f"|\U0001F420 ", end='')
			elif type(planet.get(column, row)) == Shark:
				print(f"|\U0001F988 ", end='')
			else:
				print(f"| _ ", end='')
		print("|")
		print((planet.width*4+4)*"-")


def get_free_positions(planet: 'Planet') -> list[tuple[int, int]]:
	free_positions = []
	for row in range(planet.height):
		for column in range(planet.width):
			if planet.get(column, row) is None:
				free_positions.append((column, row))
	return free_positions


def create_fishes(planet: 'Planet', free_positions: list[tuple[int, int]]) -> None:
	x, y = free_positions.pop()
	new_fish = Fish(x = x, y = y)
	planet.add(new_fish, new_fish.x, new_fish.y)


def create_sharks(planet: 'Planet', free_positions: list[tuple[int, int]]) -> None:
	x, y = free_positions.pop()
	new_shark = Shark(x = x, y = y)
	planet.add(new_shark, new_shark.x, new_shark.y)


def create_entities(planet: 'Planet', number_fishes: int, number_sharks: int) -> None:
	free_positions = get_free_positions(planet)
	random.shuffle(free_positions)

	for fish in range(number_fishes):
		create_fishes(planet, free_positions)

	for shark in range(number_sharks):
		create_sharks(planet, free_positions)


def get_entities(planet: 'Planet') -> list[Union[Fish, Shark]]:
	entities = []
	for row in range(planet.height):
		for column in range(planet.width):
			entity = planet.get(column, row)
			if entity is not None:
				entities.append(entity)
	return entities


def move_entities(planet: 'Planet') -> None:
	entities = get_entities(planet)
	i = 0
	for entity in entities:
		print(i, " ", entity)
		if type(entity) == Fish:
			entity.search_free(planet)
		else:
			entity.search_fish(planet)
			# enlever Fish mangé de entities
		print(i, " ", entity)
		i += 1


def main():
	wator = Planet(5, 3)

	create_entities(wator, 1, 1)

	print((wator.width*4+4)*"-")
	print("Chronon 0 :")
	display_grid(wator)

	move_entities(wator)

	print((wator.width*4+4)*"-")
	print("Chronon 1 :")
	display_grid(wator)

	move_entities(wator)

	print((wator.width*4+4)*"-")
	print("Chronon 2 :")
	display_grid(wator)

	move_entities(wator)

	print((wator.width*4+4)*"-")
	print("Chronon 3 :")
	display_grid(wator)

main()

# Quand Shark mange un Fish, se déplace de 2 cases ???
# Empiètement fish_reprod / eat
# Pb de reproduction : un Fish ne devrait pas pouvoir se reproduire s'il est mangé
# Séparer Fish/Shark dans move_entities : déplacer d'abord tous les Sharks puis récupérer les Fish restants ? ou inversement ?
# Ou ajouter condition : si une entité disparaît, l'enlever de la liste entities ?
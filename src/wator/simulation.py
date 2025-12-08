from __future__ import annotations
import random
import time

from typing import Union
from .planet import Planet
from .fish import Fish
from .shark import Shark
from .config import grid_width, grid_height, number_fishes, number_sharks


def display_grid(planet: 'Planet', chronon: int) -> None:
	print((planet.width*4+4)*"-")
	print(f"Chronon {chronon} :")
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


def count_entities(entities: list[Union[Fish, Shark]]) -> tuple[int, int]:
	sharks = sum(1 for entity in entities if type(entity) == Shark)
	fishes = sum(1 for entity in entities if type(entity) == Fish)
	print(f"Shark : {sharks}, Fish : {fishes}")
	return sharks, fishes


def move_entities(planet: 'Planet', entities: list[Union[Fish, Shark]]) -> None:
	i = 0
	for entity in entities:
		if type(entity) == Fish:
			if not entity.alive:
				continue
			entity.search_free(planet)
		else:
			entity.search_fish(planet)
	entities = get_entities(planet)
	return entities


def start_simulation(planet: 'Planet', chronon: int, entities: list[Union[Fish, Shark]]) -> None:
	sharks, fishes = count_entities(entities)
	while sharks > 0 and fishes > 0:
		chronon += 1
		entities = move_entities(planet, entities)
		display_grid(planet, chronon)
		sharks, fishes = count_entities(entities)
		# time.sleep(3)
	print("Number of chronons : ", chronon)
		


def simulation():
	wator = Planet(grid_width, grid_height)
	chronon = 0

	create_entities(wator, number_fishes, number_sharks)
	display_grid(wator, chronon)

	entities = get_entities(wator)
	start_simulation(wator, chronon, entities)



simulation()


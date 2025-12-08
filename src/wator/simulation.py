from __future__ import annotations
import random

from typing import Union
from .planet import Planet
from .fish import Fish
from .shark import Shark


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
		print(i, " ", entity)
		if type(entity) == Fish:
			if not entity.alive:
				continue
			entity.search_free(planet)
		else:
			entity.search_fish(planet)
		print(i, " ", entity)
		i += 1
	entities = get_entities(planet)
	return entities


def run_simulation(planet: 'Planet', chronon: int, duration: int, entities: list[Union[Fish, Shark]]) -> None:
	sharks, fishes = count_entities(entities)
	while sharks > 0 and fishes > 0 and chronon < duration:
		chronon += 1
		entities = move_entities(planet, entities)
		display_grid(planet, chronon)
		sharks, fishes = count_entities(entities)

		


def simulation():
	wator = Planet(5, 3)
	chronon = 0

	create_entities(wator, 1, 1)
	display_grid(wator, chronon)

	entities = get_entities(wator)
	run_simulation(wator, chronon, 11, entities)



simulation()


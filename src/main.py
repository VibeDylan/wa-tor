import random
from wator.planet import Planet
from wator.fish import Fish
from wator.shark import Shark


def display_grid(planet: 'Planet') -> None:
	for row in range(planet.height):
		for column in range(planet.width):
			if planet.get(column, row) is Fish:
				print(f"| F ", end='')
			elif planet.get(column, row) is Shark:
				print(f"| S ", end='')
			else:
				print(f"| _ ", end='')
		print("|")


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
	planet.add(Fish, new_fish.x, new_fish.y)


def create_sharks(planet: 'Planet', free_positions: list[tuple[int, int]]) -> None:
	x, y = free_positions.pop()
	new_shark = Shark(x = x, y = y)
	planet.add(Shark, new_shark.x, new_shark.y)


def create_entities(planet: 'Planet', number_fishes: int, number_sharks: int) -> None:
	free_positions = get_free_positions(planet)
	random.shuffle(free_positions)

	for fish in range(number_fishes):
		create_fishes(planet, free_positions)

	for shark in range(number_sharks):
		create_sharks(planet, free_positions)


def main():
	wator = Planet(5, 5)

	create_entities(wator, 6, 4)

	display_grid(wator)

# Next: start a chronon with fishes and sharks moves

main()
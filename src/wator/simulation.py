from __future__ import annotations
import random

from typing import Union
from .planet import Planet
from .fish import Fish
from .shark import Shark
from .config import grid_width, grid_height, number_fishes, number_sharks
from .database import create_database, archive_simulation



def display_grid(planet: 'Planet', chronon: int) -> None:
    """
        Display the grid in the console, with Fish and Sharks.

        Args:
            planet (Planet): the planet
            chronon (int): the chronon
    """
    print((planet.width*4+4)*"-")
    print(f"Chronon {chronon} :")
    print((planet.width*4+4)*"-")
    print(f"  ", end="")
    for j in range(planet.width):
        print(f"| {j} ", end="")
    print("| ")
    print((planet.width*4+4)*"-")

    for row in range(planet.height):
        print(f"{row} ", end="")
        for column in range(planet.width):
            cell = planet.get(column, row)
            if isinstance(cell, Shark):
                print(f"|\U0001F988 ", end="")
            elif isinstance(cell, Fish):
                print(f"|\U0001F420 ", end="")
            else:
                print(f"| _ ", end="")
        print("|")
        print((planet.width*4+4)*"-")


def get_free_positions(planet: 'Planet') -> list[tuple[int, int]]:
    """
        Get the positions who contain no sharks or fish.

        Args:
            planet (Planet): the planet

        Returns: list of tuple[int, int]: the positions who contain no sharks or fish
    """
    free_positions = []
    for row in range(planet.height):
        for column in range(planet.width):
            if planet.get(column, row) is None:
                free_positions.append((column, row))
    return free_positions


def create_entity(planet: 'Planet', instance: Union[Fish, Shark], free_positions: list[tuple[int, int]]):
    """
        Add a new entity to the planet at the last available position.

        Args:
            planet (Planet): the planet
            instance (Union[Fish, Shark]): the fish or shark
            free_positions (list[tuple[int, int]]): the positions who contain no sharks or fish
    """
    x, y = free_positions.pop()
    new_entity = instance(x = x, y = y)
    planet.add(new_entity, new_entity.x, new_entity.y)


def place_entities(planet: 'Planet', number_fishes: int, number_sharks: int) -> None:
    """
        Place randomly entities in the planet at the free positions.

        Args:
            planet (Planet): the planet
            number_fishes (int): the number of fish to add
            number_sharks (int): the number of sharks to add
    """
    free_positions = get_free_positions(planet)
    random.shuffle(free_positions)

    for fish in range(number_fishes):
        create_entity(planet, Fish, free_positions)

    for shark in range(number_sharks):
        create_entity(planet, Shark, free_positions)


def get_entities(planet: 'Planet') -> list[Union[Fish, Shark]]:
    """
        Get all the fish and shark in the planet.

        Args:
            planet (Planet): the planet

        Returns: list[Union[Fish, Shark]]: the fish or sharks found in the planet
    """
    entities = []
    for row in range(planet.height):
        for column in range(planet.width):
            entity = planet.get(column, row)
            if entity is not None:
                entities.append(entity)
    return entities


def count_entities(entities: list[Union[Fish, Shark]]) -> tuple[int, int]:
    """
        Get the number of fish and sharks in the planet.

        Args:
            entities (list[Union[Fish, Shark]]): the fish or sharks in the planet

        Returns: tuple[int, int]: the number of fish and sharks in the planet
    """
    sharks = sum(1 for entity in entities if type(entity) is Shark)
    fishes = sum(1 for entity in entities if type(entity) is Fish)
    print(f"Shark : {sharks}, Fish : {fishes}")
    return sharks, fishes


def move_entities(planet: 'Planet', entities: list[Union[Fish, Shark]]) -> None:
    """
        Move alive fish and sharks to the closest position in the planet.

        Args:
            planet (Planet): the planet
            entities (list[Union[Fish, Shark]]): the fish or sharks in the planet to move
    """
    i = 0
    for entity in entities:
        if type(entity) is Fish:
            if not entity.alive:
                continue
            entity.search_free(planet)
        else:
            entity.search_fish(planet)
    entities = get_entities(planet)
    return entities


def start_simulation(planet: 'Planet', chronon: int, entities: list[Union[Fish, Shark]]) -> None:
    """
        Create the main event (chrono) loop.
        Archive the simulation when ended.
    """
    sharks, fishes = count_entities(entities)
    while sharks > 0 and fishes > 0:
        chronon += 1
        entities = move_entities(planet, entities)
        display_grid(planet, chronon)
        sharks, fishes = count_entities(entities)
    print("Number of chronons : ", chronon)
    archive_simulation(chronon, fishes, sharks)



def simulation():
    """
        Create Planet, Shark, and Fish entities.
        Display grid.
        Start simulation.
    """
    create_database()
    wator = Planet(grid_width, grid_height)
    chronon = 0

    place_entities(wator, number_fishes, number_sharks)
    display_grid(wator, chronon)

    entities = get_entities(wator)
    start_simulation(wator, chronon, entities)


from src.wator.planet import Planet
from src.wator.fish import Fish
from src.wator.shark import Shark
import random


class TestSharkEat:
    def test_shark_eats_fish_and_gains_energy(self):
        """
        Vérifie que :
        - le requin peut se déplacer sur un poisson
        - le poisson est supprimé
        - le requin se retrouve à la nouvelle position
        - l'énergie du requin augmente correctement
        """

        planet = Planet(5,5)
        shark = Shark(2,2, energy=3)
        fish = Fish(2,3)

        planet.set(2,2, shark)
        planet.set(2,3, fish)

        shark.eat(planet, (2,3))

        assert shark.energy == 6
        assert shark.x == 2
        assert shark.y == 3
        assert planet.get(2,3) is shark
        assert planet.get(2,2) is None


    def test_shark_eat_caps_energy_at_max(self):
        """
        Vérifie que :
        - si le requin mange alors qu'il est presque à énergie max,
        - son énergie est plafonnée au maximum (10 dans ton modèle)
        """

        planet = Planet(5,5)
        shark = Shark(2,2, energy=8)
        fish = Fish(2,3)

        planet.set(2,2, shark)
        planet.set(2,3, fish)

        shark.eat(planet, (2,3))

        assert shark.energy == 10
        assert shark.x == 2
        assert shark.y == 3
        assert planet.get(2,3) is shark
        assert planet.get(2,2) is None



class TestSharkDeath:
    def test_shark_dies_when_energy_reaches_zero(self):
        """
        Vérifie que :
        - si l'énergie du requin tombe à 0 ou moins
        - la case contenant le requin est vidée (remove)
        """

        shark = Shark(2,2,energy=1)
        planet = Planet(5,5)

        planet.set(2,2,shark)
        shark.energy -= 1
        shark.check_if_dead(planet)

        assert shark.energy == 0
        assert planet.get(2,2) is None


    def test_shark_doesnt_die_with_positive_energy(self):
        """
        Vérifie que :
        - si l'énergie est > 0
        - le requin reste sur la grille après check_if_dead()
        """

        shark = Shark(2,2,energy=1)
        planet = Planet(5,5)

        planet.set(2,2,shark)
        shark.check_if_dead(planet)

        assert shark.energy == 1
        assert planet.get(2,2) is shark


class TestSharkSearchFish:
    def test_shark_moves_to_adjacent_fish(self):
        """
        Vérifie que :
        - search_fish() détecte un poisson adjacent
        - le requin se déplace vers lui
        - l'énergie se met à jour comme prévu
        """

        planet = Planet(5,5)
        shark = Shark(2,2, energy=8)
        fish = Fish(2,3)

        planet.set(2,2, shark)
        planet.set(2,3, fish)

        shark.search_fish(planet)

        assert planet.get(2,2) is None
        assert planet.get(2,3) is shark
        assert shark.energy == 10


    def test_shark_loses_energy_when_no_fish(self, monkeypatch):
        """
        Vérifie que :
        - s'il n’y a AUCUN poisson adjacent
        - le requin se déplace aléatoirement via ask_direction()
        - il perd 1 point d’énergie
        - il meurt si son énergie atteint 0
        """

        planet = Planet(5,5)
        shark = Shark(2,2, energy=1)

        planet.set(2,2, shark)

        def fake_choise(seq):
            return (2,3)
        
        monkeypatch.setattr(random, "choice", fake_choise)

        shark.search_fish(planet)

        assert shark.energy == 0
        assert planet.get(2,3) is None



class TestSharkReproduction:
    def test_shark_reproduce_at_reproduction_time(self, monkeypatch):
        """
        Vérifie que :
        - quand l'âge atteint un multiple du reproduction_time du requin
        - un bébé requin apparaît à l’ancienne position
        - le parent est bien à la nouvelle position
        """
        planet = Planet(5,5)
        shark = Shark(2,2)
        shark.age = 4

        planet.set(2,2, shark)

        def fake_choise(seq):
            return (2,3)
        
        monkeypatch.setattr(random, "choice", fake_choise)

        shark.search_fish(planet)

        assert shark.age == 5
        assert planet.get(2,3) is shark
        assert planet.get(2,2) is Shark


    def test_shark_no_reproduce_before_time(self):
        """
        Vérifie que :
        - avant le moment de reproduction,
        - aucun bébé requin n’apparaît
        """

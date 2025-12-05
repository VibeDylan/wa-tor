from src.wator.planet import Planet
from src.wator.fish import Fish
from src.wator.shark import Shark


class TestSharkEat:
    def test_shark_eats_fish_and_gains_energy(self):
        """
        Vérifie que :
        - le requin peut se déplacer sur un poisson
        - le poisson est supprimé
        - le requin se retrouve à la nouvelle position
        - l'énergie du requin augmente correctement
        """


    def test_shark_eat_caps_energy_at_max(self):
        """
        Vérifie que :
        - si le requin mange alors qu'il est presque à énergie max,
        - son énergie est plafonnée au maximum (10 dans ton modèle)
        """



class TestSharkDeath:
    def test_shark_dies_when_energy_reaches_zero(self):
        """
        Vérifie que :
        - si l'énergie du requin tombe à 0 ou moins
        - la case contenant le requin est vidée (remove)
        """


    def test_shark_doesnt_die_with_positive_energy(self):
        """
        Vérifie que :
        - si l'énergie est > 0
        - le requin reste sur la grille après check_if_dead()
        """



class TestSharkSearchFish:
    def test_shark_moves_to_adjacent_fish(self):
        """
        Vérifie que :
        - search_fish() détecte un poisson adjacent
        - le requin se déplace vers lui
        - l'énergie se met à jour comme prévu
        """


    def test_shark_loses_energy_when_no_fish(self):
        """
        Vérifie que :
        - s'il n’y a AUCUN poisson adjacent
        - le requin se déplace aléatoirement via ask_direction()
        - il perd 1 point d’énergie
        - il meurt si son énergie atteint 0
        """



class TestSharkReproduction:
    def test_shark_reproduce_at_reproduction_time(self):
        """
        Vérifie que :
        - quand l'âge atteint un multiple du reproduction_time du requin
        - un bébé requin apparaît à l’ancienne position
        - le parent est bien à la nouvelle position
        """


    def test_shark_no_reproduce_before_time(self):
        """
        Vérifie que :
        - avant le moment de reproduction,
        - aucun bébé requin n’apparaît
        """

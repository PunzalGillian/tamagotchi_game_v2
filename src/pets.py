from src.pet_controls import PetBase

class Bulbasaur(PetBase):
    def initialize_stats(self):
        self._weight = 2
        self._happiness = 5
        self._health = 7
        self._hunger = 6

class Jigglypuff(PetBase):
    def initialize_stats(self):
        self._weight = 1
        self._happiness = 8
        self._health = 4
        self._hunger = 5

class Charizard(PetBase):
    def initialize_stats(self):
        self._weight = 5
        self._happiness = 6
        self._health = 8
        self._hunger = 7

class Squirtle(PetBase):
    def initialize_stats(self):
        self._weight = 3
        self._happiness = 7
        self._health = 6
        self._hunger = 6

class Ghastly(PetBase):
    def initialize_stats(self):
        self._weight = 1
        self._happiness = 6
        self._health = 5
        self._hunger = 8

class Oddish(PetBase):
    def initialize_stats(self):
        self._weight = 2
        self._happiness = 7
        self._health = 7
        self._hunger = 5
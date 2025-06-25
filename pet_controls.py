from abc import ABC, abstractmethod

class PetBase(ABC):
    def __init__(self, name):
        self._name = name
        self._weight = 1
        self._happiness = 4
        self._health = 6
        self._hunger = 6

    @abstractmethod
    def initialize_stats(self):
        pass

    @property
    def name(self):
        return self._name

    @property
    def weight(self):
        return self._weight

    @property
    def happiness(self):
        return self._happiness

    @property
    def health(self):
        return self._health

    @property
    def hunger(self):
        return self._hunger

    def feed(self):
        if self._hunger < 10:
            self._hunger = min(10, self._hunger + 5)
            self._happiness = min(10, self._happiness + 5)
            return f"{self._name} was fed. \nHunger: {self._hunger}, \nHappiness: {self._happiness}"
        return f"{self._name} is not hungry."

    def play(self):
        self._happiness = min(10, self._happiness + 5)
        return f"{self._name} played! Happiness: {self._happiness}"

    def give_medicine(self):
        if self._health < 10:
            self._health = min(10, self._health + 5)
            return f"{self._name} received medicine. \nHealth: {self._health}"
        return f"{self._name}'s health is full."

    def status(self):
        return (
            f"\nName: {self._name}"
            f"\n\tWeight: {self._weight}kg"
            f"\n\tHappiness: {self._happiness}/10"
            f"\n\tHealth: {self._health}/10\n"
            f"\n\tHunger: {self._hunger}/10"
        )
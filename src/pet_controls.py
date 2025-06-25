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
        return f"{self._name} wants you to choose a food!"

    def play(self):
        self._happiness = min(10, self._happiness + 5)
        self._hunger = max(0, self._hunger - 3)
        return f"{self._name} played! Happiness: {self._happiness}, \nHunger: {self._hunger}"
    

    def give_medicine(self):
        if self._health < 10:
            self._health = min(10, self._health + 5)
            return f"{self._name} received medicine. \nHealth: {self._health}"
        return f"{self._name}'s health is full."

    def status(self):
        return (
            f"\n\tName: {self._name}\n"
            f"\n\tWeight: {self._weight}kg\n"
            f"\n\tHappiness: {self._happiness}/10\n"
            f"\n\tHealth: {self._health}/10\n"
            f"\n\tHunger: {self._hunger}/10\n"
        )

class PetControls:
    def __init__(self, pet):
        self.pet = pet

    def can_feed(self):
        return self.pet._hunger < 10

    def feed(self, food):
        if not self.can_feed():
            return "You're already full, come back later"
        self.pet._hunger = min(10, self.pet._hunger + food["hunger"])
        self.pet._happiness = min(10, self.pet._happiness + food["happiness"])
        if food["name"] == "Cake":
            return f"{food['name']} eaten!\nHunger +3,\nHappiness +3"
        elif food["name"] == "Milk":
            return f"{food['name']} eaten!\nHunger +5"
        return f"{food['name']} eaten!"

    def status(self):
        return (
            f"\nName: {self.pet._name}"
            f"\n\tWeight: {self.pet._weight}kg"
            f"\n\tHappiness: {self.pet._happiness}/10"
            f"\n\tHealth: {self.pet._health}/10\n"
            f"\n\tHunger: {self.pet._hunger}/10"
        )

    def play(self):
        self.pet._happiness = min(10, self.pet._happiness + 5)
        self.pet._hunger = max(0, self.pet._hunger - 3)
        return f"{self.pet._name} played! Happiness: {self.pet._happiness}, \nHunger: {self.pet._hunger}"

    def give_medicine(self):
        if self.pet._health < 10:
            self.pet._health = min(10, self.pet._health + 5)
            return f"{self.pet._name} received medicine. \nHealth: {self.pet._health}"
        return f"{self.pet._name}'s health is full."
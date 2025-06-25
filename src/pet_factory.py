from src.pets import Bulbasaur, Jigglypuff, Charizard, Squirtle, Ghastly, Oddish

class PetFactory:
    @staticmethod
    def create_pet(name):
        pets = {
            "Bulbasaur": Bulbasaur,
            "Jigglypuff": Jigglypuff,
            "Charizard": Charizard,
            "Squirtle": Squirtle,
            "Ghastly": Ghastly,
            "Oddish": Oddish
        }
        pet_class = pets.get(name)
        if pet_class:
            pet = pet_class(name)
            pet.initialize_stats()
            return pet
        raise ValueError("Unknown pet name")
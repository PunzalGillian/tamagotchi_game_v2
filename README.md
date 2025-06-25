# 🐾 Pokémon Tamagotchi

Welcome to **Pokémon Tamagotchi** — a fun, nostalgic desktop pet game where you hatch and take care of a Pokémon!

Built in **Python** with **PyQt5** and **Pygame**, this game lets you hatch a Pokémon from an egg, then feed, heal, and play with it — now with multiple food options and a fully **object-oriented** architecture!

🔗 **Live Demo**: Not available (local execution required)

![Python](https://img.shields.io/badge/Backend-Python-blue)
![PyQt5](https://img.shields.io/badge/GUI-PyQt5-green)
![Pygame](https://img.shields.io/badge/Sound-Pygame-red)
![OOP](https://img.shields.io/badge/OOP-Four%20Pillars-important)

## ✨ Features

- 🥚 **Pick an Egg**: Choose from iconic Pokémon like Bulbasaur, Jigglypuff, Charizard, Squirtle, and more!
- 🐣 **Hatch and Care**: After hatching, care for your Pokémon by:
  - 🔍 Checking its **Status** (health, hunger, happiness, sleep)
  - 💊 Giving it **Medicine** when it's sick
  - 🍽️ **Feeding** it with a variety of food choices (e.g., berry, candy, Poképuff)
  - 🎮 **Playing** a mini-game with it to improve happiness
- 🍎 **Food Selection Feature**: Different foods affect your Pokémon in unique ways — from restoring health to increasing happiness or weight.
- 🎶 **Sound Effects**: Custom sound alerts for hatching, actions, and attention.
- 🎨 **Custom UI**: Retro pixel background with a draggable, borderless window
- 🎮 **Simple Controls**:
  - `A` — Move left
  - `B` — Confirm
  - `C` — Move right

## 🧠 Object-Oriented Design

This project is built using the **four pillars of OOP**:

### 🔐 1. Encapsulation
All data (health, hunger, happiness, etc.) is managed within each Pokémon class. Interaction with the pet's stats happens through defined methods, hiding internal state and protecting integrity.

### 🧬 2. Inheritance
A base `Pokemon` class defines common behavior, while specific Pokémon (e.g., `Charizard`, `Squirtle`) inherit and extend those traits with custom stats or sounds.

### 🌀 3. Polymorphism
Each Pokémon subclass may override methods like `play()` or `feed()` to produce different effects or animations while using the same interface.

### 🧩 4. Abstraction
The main interface allows interaction with Pokémon through high-level commands (e.g., `pokemon.feed(selected_food)`), hiding complex logic behind simple actions.

## 🛠️ Built With

- **Python**
- **PyQt5** — for the GUI
- **Pygame** — for sound effects
- **OOP Principles** — for scalable architecture

## 🚀 How to Play

### 1. Install Dependencies
```bash
pip install PyQt5 pygame
2. Run the Game
bash
Copy
Edit
python tamagotchi.py
3. Controls
A — Move selection left

B — Confirm or activate option

C — Move selection right

4. Gameplay Tips
Keep an eye on your Pokémon’s status

Feed your Pokémon with different food types for varied effects

If your Pokémon looks sick, give it medicine

Play games with it to increase happiness!
```

## 📷 Screenshots
Coming soon…

## 🚧 Future Improvements
Add more Pokémon and evolution mechanics

Enhance animations and sound effects

Save/load pet progress across sessions

Improve mobile/touch UI support

Add multiplayer pet battles or trading features

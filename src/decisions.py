from PyQt5.QtCore import Qt

def back_to_menu(self):
    # Check for death before returning to menu
    if self.selected_pet and (self.selected_pet._hunger == 0 or self.selected_pet._health == 0):
        self.selected_pet._status = "Your pet died."
        self.pet_dead = True
        # Clear all other text/screens
        self.screen_states = {k: False for k in self.screen_states}
        self.texts = {k: "" for k in self.texts}
        self.texts["dead"] = self.selected_pet._status
        self.sound_manager.play("death")
        self.buttonA.setEnabled(False)
        self.buttonB.setEnabled(False)
        self.buttonC.setEnabled(False)
        self.update()
        return
    # Normal back to menu logic
    self.screen_states = {k: False for k in self.screen_states}
    self.menu_active = True
    self.update()

def menu_options(self):
    name = self.MENU_ITEMS[self.current_menu_index]["name"]
    self.menu_active = False
    self.screen_states = {k: False for k in self.screen_states}
    font = self.font()
    screen_w, screen_h = 162, 151
    if name == "Feed":
        self.choosing_food = True
        self.current_food_index = 0
        self.menu_active = False
        self.screen_states = {k: False for k in self.screen_states}
        self.update()
    elif name == "Status":
        raw_text = self.pet_controls.status()
        self.texts["status"] = self.wrap_text_to_box(raw_text, font, screen_w - 10, screen_h - 10)
        self.screen_states["status"] = True
        self.update()
    elif name == "Medicine":
        raw_text = self.pet_controls.give_medicine()
        self.texts["medicine"] = self.wrap_text_to_box(raw_text, font, screen_w - 10, screen_h - 10)
        self.screen_states["medicine"] = True
        self.update()
    elif name == "Play":
        raw_text = self.pet_controls.play()
        self.texts["play"] = self.wrap_text_to_box(raw_text, font, screen_w - 10, screen_h - 10)
        self.screen_states["play"] = True
        self.update()

def select_or_action(self):
    if self.choosing_food:
        food = self.food_names[self.current_food_index]
        food_info = self.food_data[food]
        if self.selected_pet._hunger >= 10:
            self.texts["feed"] = "You're already full, come back later"
        else:
            self.selected_pet._hunger = min(10, self.selected_pet._hunger + food_info["hunger"])
            self.selected_pet._happiness = min(10, self.selected_pet._happiness + food_info["happiness"])
            if food == "Cake":
                msg = f"{food} eaten!\nHunger +3,\nHappiness +3"
            elif food == "Milk":
                msg = f"{food} eaten!\nHunger +5"
            else:
                msg = f"{food} eaten!"
            self.texts["feed"] = msg
        self.screen_states = {k: False for k in self.screen_states}
        self.screen_states["feed"] = True
        self.choosing_food = False
        self.update()
        return
    if not self.selected_pet:
        name = self.egg_names[self.current_egg_index]
        self.selected_pet = self.PetFactory.create_pet(name)
        self.pet_controls = self.PetControls(self.selected_pet)
        self.sound_manager.play("hatch")
        self.QTimer.singleShot(500, self.activate_menu)
    elif self.menu_active:
        self.menu_options()
    elif self.any_subscreen():
        self.back_to_menu()
    self.update()

def next_egg_or_menu(self):
    if self.choosing_food:
        self.current_food_index = (self.current_food_index + 1) % len(self.food_names)
        self.update()
        return
    if not self.selected_pet:
        self.current_egg_index = (self.current_egg_index + 1) % len(self.egg_names)
    elif self.menu_active:
        self.current_menu_index = (self.current_menu_index + 1) % len(self.MENU_ITEMS)
    self.update()

def prev_egg_or_menu(self):
    if self.choosing_food:
        self.current_food_index = (self.current_food_index - 1) % len(self.food_names)
        self.update()
        return
    if not self.selected_pet:
        self.current_egg_index = (self.current_egg_index - 1) % len(self.egg_names)
    elif self.menu_active:
        self.current_menu_index = (self.current_menu_index - 1) % len(self.MENU_ITEMS)
    self.update()

def mousePressEvent(self, event):
    if event.button() == Qt.LeftButton:
        self.oldPosition = event.globalPos()

def mouseMoveEvent(self, event):
    if event.buttons() == Qt.LeftButton:
        delta = event.globalPos() - self.oldPosition
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPosition = event.globalPos()
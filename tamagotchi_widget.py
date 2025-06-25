from PyQt5.QtWidgets import QWidget, QPushButton
from PyQt5.QtGui import QPainter, QPainterPath, QPixmap, QPen, QColor, QFont
from PyQt5.QtCore import Qt, QRectF, QPoint, QTimer
from sound_manager import SoundManager
from pet_factory import PetFactory

class TamagotchiApp(QWidget):
    EGGS = {
        "Bulbasaur": "img/bulbasaur-egg.png",
        "Jigglypuff": "img/jigglypuff-egg.png",
        "Charizard": "img/charizard-egg.png",
        "Squirtle": "img/squirtle-egg.png",
        "Ghastly": "img/ghastly-egg.png",
        "Oddish": "img/oddish-egg.png"
    }
    PET_IMAGES = {
        "Bulbasaur": "img/bulbasaur.png",
        "Jigglypuff": "img/jigglypuff.png",
        "Charizard": "img/charizard.png",
        "Squirtle": "img/squirtleegg.png",
        "Ghastly": "img/ghastly.png",
        "Oddish": "img/oddish.png"
    }
    MENU_ITEMS = [
        {"name": "Status", "image": "img/heart.png"},
        {"name": "Medicine", "image": "img/medicine.png"},
        {"name": "Feed", "image": "img/feed.png"},
        {"name": "Play", "image": "img/play.png"}
    ]

    def __init__(self):
        super().__init__()
        self.setFixedSize(270, 318)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.oldPosition = QPoint(0, 0)

        self.sound_manager = SoundManager()
        self.egg_names = list(self.EGGS.keys())
        self.egg_images = {name: QPixmap(path) for name, path in self.EGGS.items()}
        self.pet_images = {name: QPixmap(path) for name, path in self.PET_IMAGES.items()}
        self.menu_images = {item["name"]: QPixmap(item["image"]) for item in self.MENU_ITEMS}
        self.bg_image = QPixmap("img/bg.png")

        self.current_egg_index = 0
        self.selected_pet = None
        self.menu_active = False
        self.current_menu_index = 0

        self.screen_states = {"status": False, "medicine": False, "feed": False, "play": False}
        self.texts = {"status": "", "medicine": "", "feed": "", "play": ""}

        self.setup_ui()
        self.sound_manager.play("start")

    def setup_ui(self):
        def make_btn(label, x, cb):
            btn = QPushButton(label, self)
            btn.setFixedSize(30, 30)
            btn.setStyleSheet("border-radius: 15px; background-color: lightgray; border: 3px solid rgb(63,99,171);")
            btn.move(x, 260)
            btn.clicked.connect(cb)
            return btn
        self.buttonA = make_btn("A", 73, self.prev_egg_or_menu)
        self.buttonB = make_btn("B", 120, self.select_or_action)
        self.buttonC = make_btn("C", 168, self.next_egg_or_menu)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        ellipse_path = QPainterPath(); ellipse_path.addEllipse(QRectF(0, 0, 270, 318))
        painter.setClipPath(ellipse_path)
        if not self.bg_image.isNull():
            painter.drawPixmap(0, 0, self.bg_image.scaled(270, 318))
        pen = QPen(QColor(63, 99, 171), 10)
        painter.setPen(pen); painter.setClipping(False)
        painter.drawEllipse(5, 5, 260, 308)
        screen_w, screen_h = 162, 151
        center_x, center_y = (self.width() - screen_w) // 2, (self.height() - screen_h) // 2
        screen = QRectF(center_x, center_y, screen_w, screen_h)
        painter.setBrush(QColor(200, 200, 200)); painter.setPen(pen)
        painter.drawRect(screen)

        # Draw pet if not in a sub-screen, else draw sub-screen text
        if self.selected_pet and not self.any_subscreen():
            pet_img = self.pet_images[self.selected_pet.name].scaled(85, 85)
            painter.drawPixmap((self.width() - 85) // 2, (self.height() - 85) // 2 - 15, pet_img)
        elif not self.selected_pet:
            name = self.egg_names[self.current_egg_index]
            egg = self.egg_images[name].scaled(65, 76)
            painter.drawPixmap((self.width() - 65) // 2, (self.height() - 75) // 2, egg)

        if self.menu_active:
            self.menu_layout(painter, center_x, center_y)

        painter.setPen(QPen(QColor(0, 0, 0)))
        painter.setFont(QFont("PixelOperator.ttf", 8))
        for key in self.screen_states:
            if self.screen_states[key]:
                painter.drawText(screen, Qt.AlignLeft | Qt.AlignTop, self.texts[key])

    def any_subscreen(self):
        return any(self.screen_states.values())

    def prev_egg_or_menu(self):
        if not self.selected_pet:
            self.current_egg_index = (self.current_egg_index - 1) % len(self.egg_names)
        elif self.menu_active:
            self.current_menu_index = (self.current_menu_index - 1) % len(self.MENU_ITEMS)
        self.update()

    def next_egg_or_menu(self):
        if not self.selected_pet:
            self.current_egg_index = (self.current_egg_index + 1) % len(self.egg_names)
        elif self.menu_active:
            self.current_menu_index = (self.current_menu_index + 1) % len(self.MENU_ITEMS)
        self.update()

    def select_or_action(self):
        if not self.selected_pet:
            name = self.egg_names[self.current_egg_index]
            self.selected_pet = PetFactory.create_pet(name)
            self.sound_manager.play("hatch")
            QTimer.singleShot(500, self.activate_menu)
        elif self.menu_active:
            self.menu_options()
        elif self.any_subscreen():
            self.back_to_menu()
        self.update()

    def activate_menu(self):
        self.menu_active = True
        self.update()

    def menu_layout(self, painter, center_x, center_y):
        item_w, item_h = 30, 30
        start_x, start_y = center_x + 12, center_y + 110
        for i, item in enumerate(self.MENU_ITEMS):
            item_x = start_x + i * (item_w + 5)
            scaled_menu_item = self.menu_images[item["name"]].scaled(item_w, item_h)
            painter.drawPixmap(item_x, start_y, scaled_menu_item)
            if i == self.current_menu_index:
                pen = QPen(QColor(63, 99, 171), 4)
                painter.setPen(pen)
                painter.drawRect(QRectF(item_x, start_y, item_w, item_h))

    def menu_options(self):
        name = self.MENU_ITEMS[self.current_menu_index]["name"]
        self.menu_active = False
        self.screen_states = {k: False for k in self.screen_states}
        if name == "Status":
            self.texts["status"] = self.selected_pet.status()
            self.screen_states["status"] = True
        elif name == "Medicine":
            self.texts["medicine"] = f"\n\n  {self.selected_pet.give_medicine()}"
            self.screen_states["medicine"] = True
        elif name == "Feed":
            self.texts["feed"] = f"\n\n  {self.selected_pet.feed()}"
            self.screen_states["feed"] = True
        elif name == "Play":
            self.texts["play"] = f"\n\n  {self.selected_pet.play()}"
            self.screen_states["play"] = True
        self.update()

    def back_to_menu(self):
        self.screen_states = {k: False for k in self.screen_states}
        self.menu_active = True
        self.update()

    # --- Draggable widget ---
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.oldPosition = event.globalPos()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            delta = event.globalPos() - self.oldPosition
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPosition = event.globalPos()
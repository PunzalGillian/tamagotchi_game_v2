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
        self.oldPosition = QPoint(0, 0)
        self.setFixedSize(270, 318)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.sound_manager = SoundManager()
        self.egg_names = list(self.EGGS.keys())
        self.egg_images = {}
        for name, path in self.EGGS.items():
            pixmap = QPixmap(path)
            if pixmap.isNull():
                print(f"Failed to load image: {path}")
            self.egg_images[name] = pixmap
        self.pet_images = {name: QPixmap(path) for name, path in self.PET_IMAGES.items()}
        self.menu_images = {item["name"]: QPixmap(item["image"]) for item in self.MENU_ITEMS}

        self.current_egg_index = 0
        self.selected_pet = None
        self.menu_active = False
        self.current_menu_index = 0
        self.bg_image = QPixmap("img/bg.png")

        self.is_status_screen = False
        self.is_medicine_screen = False
        self.is_feed_screen = False
        self.is_play_screen = False

        self.show_pet_image = True  # In __init__, default to True

        self.setup_ui()
        self.sound_manager.play("start")

    def setup_ui(self):
        self.buttonA = QPushButton("A", self)
        self.buttonA.setFixedSize(30, 30)
        self.buttonA.setStyleSheet("border-radius: 15px; background-color: lightgray; border: 3px solid rgb(63,99,171);")
        self.buttonA.move(73, 260)
        self.buttonA.clicked.connect(self.prev_egg_or_menu)

        self.buttonB = QPushButton("B", self)
        self.buttonB.setFixedSize(30, 30)
        self.buttonB.setStyleSheet("border-radius: 15px; background-color: lightgray; border: 3px solid rgb(63,99,171);")
        self.buttonB.move(120, 260)
        self.buttonB.clicked.connect(self.select_or_action)

        self.buttonC = QPushButton("C", self)
        self.buttonC.setFixedSize(30, 30)
        self.buttonC.setStyleSheet("border-radius: 15px; background-color: lightgray; border: 3px solid rgb(63,99,171);")
        self.buttonC.move(168, 260)
        self.buttonC.clicked.connect(self.next_egg_or_menu)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Draw round widget background
        ellipse_path = QPainterPath()
        ellipse_path.addEllipse(QRectF(0, 0, 270, 318))
        painter.setClipPath(ellipse_path)
        if not self.bg_image.isNull():
            bg_image = self.bg_image.scaled(270, 318)
            painter.drawPixmap(0, 0, bg_image)

        # Draw outline
        pen = QPen(QColor(63, 99, 171), 10)
        painter.setPen(pen)
        painter.setClipping(False)
        painter.drawEllipse(5, 5, 260, 308)

        # Draw screen
        screen_w, screen_h = 162, 151
        center_x = (self.width() - screen_w) // 2
        center_y = (self.height() - screen_h) // 2
        screen = QRectF(center_x, center_y, screen_w, screen_h)
        painter.setBrush(QColor(200, 200, 200))
        painter.setPen(pen)
        painter.drawRect(screen)

        # Draw pet image if hatched and NOT on a sub-screen
        if self.selected_pet and not (
            self.is_status_screen or self.is_medicine_screen or self.is_feed_screen or self.is_play_screen
        ):
            pet_img = self.pet_images[self.selected_pet.name].scaled(85, 85)
            painter.drawPixmap((self.width() - 85) // 2, (self.height() - 85) // 2 - 15, pet_img)

        # Draw egg if not hatched
        if not self.selected_pet:
            name = self.egg_names[self.current_egg_index]
            egg = self.egg_images[name].scaled(65, 76)
            painter.drawPixmap((self.width() - 65) // 2, (self.height() - 75) // 2, egg)

        # Draw menu if active
        if self.menu_active:
            self.menu_layout(painter, center_x, center_y)

        # Draw sub-screen text
        painter.setPen(QPen(QColor(0, 0, 0)))
        painter.setFont(QFont("PixelOperator.ttf", 8))
        if self.is_status_screen:
            painter.drawText(screen, Qt.AlignLeft | Qt.AlignTop, self.status_text)
        elif self.is_play_screen:
            painter.drawText(screen, Qt.AlignLeft | Qt.AlignTop, self.play_text)
        elif self.is_medicine_screen:
            painter.drawText(screen, Qt.AlignLeft | Qt.AlignTop, self.medicine_text)
        elif self.is_feed_screen:
            painter.drawText(screen, Qt.AlignLeft | Qt.AlignTop, self.feed_text)

    # --- Draggable widget ---
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.oldPosition = event.globalPos()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            delta = event.globalPos() - self.oldPosition
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPosition = event.globalPos()

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
        elif self.is_status_screen or self.is_medicine_screen or self.is_feed_screen or self.is_play_screen:
            self.back_to_menu()
        self.update()

    def activate_menu(self):
        self.menu_active = True
        self.show_pet_image = False  # Hide pet image when menu is active
        self.update()

    def menu_layout(self, painter, center_x, center_y):
        item_w = 30
        item_h = 30
        start_x = center_x + 12
        start_y = center_y + 110

        for i, item in enumerate(self.MENU_ITEMS):
            item_x = start_x + i * (item_w + 5)
            scaled_menu_item = self.menu_images[item["name"]].scaled(item_w, item_h)
            painter.drawPixmap(item_x, start_y, scaled_menu_item)
            if i == self.current_menu_index:
                pen = QPen(QColor(63, 99, 171), 4)
                painter.setPen(pen)
                painter.drawRect(QRectF(item_x, start_y, item_w, item_h))

    def menu_options(self):
        selected_menu = self.MENU_ITEMS[self.current_menu_index]["name"]
        if selected_menu == "Status":
            self.status()
        elif selected_menu == "Medicine":
            self.medicine()
        elif selected_menu == "Feed":
            self.feed()
        elif selected_menu == "Play":
            self.play()

    def back_to_menu(self):
        self.is_status_screen = False
        self.is_medicine_screen = False
        self.is_feed_screen = False
        self.is_play_screen = False
        self.menu_active = True
        self.update()

    def status(self):
        pet = self.selected_pet
        self.status_text = pet.status()
        self.is_status_screen = True
        self.menu_active = False
        self.update()

    def medicine(self):
        result = self.selected_pet.give_medicine()
        self.medicine_text = f"\n\n  {result}"
        self.is_medicine_screen = True
        self.menu_active = False
        self.update()

    def feed(self):
        result = self.selected_pet.feed()
        self.feed_text = f"\n\n  {result}"
        self.is_feed_screen = True
        self.menu_active = False
        self.update()

    def play(self):
        result = self.selected_pet.play()
        self.play_text = f"\n\n  {result}"
        self.is_play_screen = True
        self.menu_active = False
        self.update()
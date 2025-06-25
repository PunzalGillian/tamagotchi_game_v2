from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QPainterPath, QPixmap, QPen, QColor, QFont, QFontMetrics
from PyQt5.QtCore import Qt, QRectF, QPoint, QTimer
from sound_manager import SoundManager
from pet_factory import PetFactory
from pet_controls import PetControls
from tama_buttons import TamaButton, create_tama_buttons
from decisions import (
    back_to_menu, menu_options, select_or_action,
    next_egg_or_menu, prev_egg_or_menu,
    mousePressEvent, mouseMoveEvent
)

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

    FOODS = [
        {"name": "Milk", "image": "img/milk.png", "hunger": 5, "happiness": 0},
        {"name": "Cake", "image": "img/cake.png", "hunger": 3, "happiness": 3}
    ]


    def __init__(self):
        super().__init__()
        self.setFixedSize(270, 318)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.oldPosition = QPoint(0, 0)
        self.QTimer = QTimer

        self.PetFactory = PetFactory
        self.PetControls = PetControls
        self.sound_manager = SoundManager()
        self.egg_names = list(self.EGGS.keys())
        self.egg_images = {n: QPixmap(p) for n, p in self.EGGS.items()}
        self.pet_images = {n: QPixmap(p) for n, p in self.PET_IMAGES.items()}
        self.food_images = {f["name"]: QPixmap(f["image"]) for f in self.FOODS}
        self.menu_images = {i["name"]: QPixmap(i["image"]) for i in self.MENU_ITEMS}
        self.bg_image = QPixmap("img/bg.png")

        self.current_egg_index = 0
        self.selected_pet = None
        self.pet_controls = None
        self.menu_active = False
        self.current_menu_index = 0

        self.screen_states = {k: False for k in ["status", "medicine", "feed", "play"]}
        self.texts = {k: "" for k in self.screen_states}

        self.choosing_food = False
        self.current_food_index = 0
        self.food_names = [f["name"] for f in self.FOODS]
        self.food_data = {f["name"]: f for f in self.FOODS}

        # --- Assign decision functions BEFORE setup_ui ---
        self.back_to_menu = back_to_menu.__get__(self)
        self.menu_options = menu_options.__get__(self)
        self.select_or_action = select_or_action.__get__(self)
        self.next_egg_or_menu = next_egg_or_menu.__get__(self)
        self.prev_egg_or_menu = prev_egg_or_menu.__get__(self)
        self.mousePressEvent = mousePressEvent.__get__(self)
        self.mouseMoveEvent = mouseMoveEvent.__get__(self)

        self.setup_ui()
        self.sound_manager.play("start")

    def setup_ui(self):
        self.buttonA, self.buttonB, self.buttonC = create_tama_buttons(
            self, self.prev_egg_or_menu, self.select_or_action, self.next_egg_or_menu
        )

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
        painter.setBrush(QColor(200, 200, 200)); painter.setPen(QPen(QColor(63, 99, 171), 8))
        painter.drawRect(screen)

        # Draw pet or egg
        if self.selected_pet and not self.any_subscreen() and not self.choosing_food:
            pet_img = self.pet_images[self.selected_pet.name].scaled(85, 85)
            painter.drawPixmap((self.width() - 85) // 2, (self.height() - 85) // 2 - 15, pet_img)
        elif not self.selected_pet:
            name = self.egg_names[self.current_egg_index]
            egg = self.egg_images[name].scaled(65, 76)
            painter.drawPixmap((self.width() - 65) // 2, (self.height() - 75) // 2, egg)

        if self.menu_active:
            self.menu_layout(painter, center_x, center_y)

        # Draw wrapped, centered text for active screen
        font = QFont("PixelOperator.ttf", 8)
        painter.setFont(font)
        for key in self.screen_states:
            if self.screen_states[key]:
                wrapped = self.wrap_text_to_box(self.texts[key], font, screen_w - 20, screen_h - 10)  # 20px left/right padding
                painter.setPen(QPen(QColor(0, 0, 0)))
                if key == "status":
                    # Calculate vertical centering
                    metrics = QFontMetrics(font)
                    lines = wrapped.split('\n')
                    text_height = metrics.lineSpacing() * len(lines)
                    y_offset = center_y + (screen_h - text_height) // 2
                    x_offset = center_x + 10  # 10px left padding
                    for i, line in enumerate(lines):
                        painter.drawText(x_offset, y_offset + metrics.ascent() + i * metrics.lineSpacing(), line)
                else:
                    painter.drawText(screen, Qt.AlignCenter, wrapped)

        if self.choosing_food:
            food = self.food_names[self.current_food_index]
            img = self.food_images[food].scaled(75, 75)
            painter.drawPixmap((self.width() - 75) // 2, (self.height() - 75) // 2, img)
            return  # Skip drawing pet/egg/text while choosing food

    def any_subscreen(self):
        return any(self.screen_states.values())

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

    def wrap_text_to_box(self, text, font, max_width, max_height):
        metrics = QFontMetrics(font)
        words = text.split()
        lines, line = [], ""
        for word in words:
            test_line = f"{line} {word}".strip()
            if metrics.horizontalAdvance(test_line) > max_width and line:
                lines.append(line)
                line = word
            else:
                line = test_line
        if line: lines.append(line)
        line_height = metrics.lineSpacing()
        max_lines = max_height // line_height
        if len(lines) > max_lines:
            lines = lines[:max_lines]
            lines[-1] += " ..."
        return "\n".join(lines)


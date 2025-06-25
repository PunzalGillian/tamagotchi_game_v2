from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QPainterPath, QPixmap, QPen, QColor, QFont, QFontMetrics
from PyQt5.QtCore import Qt, QRectF, QPoint, QTimer
from src.sound_manager import SoundManager
from src.pet_factory import PetFactory
from src.pet_controls import PetControls
from src.tama_buttons import TamaButton, create_tama_buttons
from src.decisions import (
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
        self.setFixedSize(324, 382)
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

        self.pet_dead = False
        self._death_exit_scheduled = False

    # --- Add this reusable function ---
    def draw_centered_wrapped_text(self, painter, text, font, rect):
        """
        Draws wrapped text centered vertically and horizontally in the given rect.
        """
        wrapped = self.wrap_text_to_box(text, font, rect.width() - 20, rect.height() - 10)
        painter.setFont(font)
        painter.setPen(QPen(QColor(0, 0, 0)))
        metrics = QFontMetrics(font)
        lines = wrapped.split('\n')
        text_height = metrics.lineSpacing() * len(lines)
        y_offset = int(rect.top() + (rect.height() - text_height) // 2)
        for i, line in enumerate(lines):
            line_width = metrics.horizontalAdvance(line)
            x_offset = int(rect.left() + (rect.width() - line_width) // 2)
            painter.drawText(x_offset, y_offset + metrics.ascent() + i * metrics.lineSpacing(), line)

    def setup_ui(self):
        self.buttonA, self.buttonB, self.buttonC = create_tama_buttons(
            self, self.prev_egg_or_menu, self.select_or_action, self.next_egg_or_menu
        )

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        ellipse_path = QPainterPath(); ellipse_path.addEllipse(QRectF(0, 0, 324, 382))
        painter.setClipPath(ellipse_path)
        if not self.bg_image.isNull():
            painter.drawPixmap(0, 0, self.bg_image.scaled(324, 382))
        pen = QPen(QColor(63, 99, 171), 12)
        painter.setPen(pen); painter.setClipping(False)
        painter.drawEllipse(5, 5, 312, 370)
        screen_w, screen_h = 195, 181
        center_x, center_y = (self.width() - screen_w) // 2, (self.height() - screen_h) // 2
        screen = QRectF(center_x, center_y, screen_w, screen_h)
        painter.setBrush(QColor(200, 200, 200)); painter.setPen(QPen(QColor(63, 99, 171), 8))
        painter.drawRect(screen)

        # --- PET DEATH: Show only the death message, centered, and skip all other UI ---
        if getattr(self, "pet_dead", False):
            font = QFont("PixelOperator.ttf", 12)
            msg = self.texts.get("dead", "Your pet died.")
            self.draw_centered_wrapped_text(painter, msg, font, screen)
            return

        # Draw pet or egg
        if self.selected_pet and not self.any_subscreen() and not self.choosing_food and not getattr(self, "pet_dead", False):
            pet_img = self.pet_images[self.selected_pet.name].scaled(95, 95)
            painter.drawPixmap((self.width() - 95) // 2, (self.height() - 95) // 2 - 15, pet_img)
        elif not self.selected_pet:
            name = self.egg_names[self.current_egg_index]
            egg = self.egg_images[name].scaled(78, 91)
            painter.drawPixmap((self.width() - 78) // 2, (self.height() - 91) // 2, egg)

        if self.menu_active:
            self.menu_layout(painter, center_x, center_y)

        # Draw wrapped, centered text for active screen
        font = QFont("PixelOperator.ttf", 10)
        for key in self.screen_states:
            if self.screen_states[key]:
                if key == "status":
                    self.draw_centered_wrapped_text(painter, self.texts[key], font, screen)
                else:
                    painter.setFont(font)
                    painter.setPen(QPen(QColor(0, 0, 0)))
                    painter.drawText(screen, Qt.AlignCenter, self.wrap_text_to_box(self.texts[key], font, screen_w - 24, screen_h - 12))

        if self.choosing_food:
            food = self.food_names[self.current_food_index]
            img = self.food_images[food].scaled(90, 90)
            painter.drawPixmap((self.width() - 90) // 2, (self.height() - 90) // 2, img)
            return  # Skip drawing pet/egg/text while choosing food

    def any_subscreen(self):
        return any(self.screen_states.values())

    def activate_menu(self):
        self.menu_active = True
        self.update()

    def menu_layout(self, painter, center_x, center_y):
        item_w, item_h = 36, 36
        start_x, start_y = center_x + 15, center_y + 132
        for i, item in enumerate(self.MENU_ITEMS):
            item_x = start_x + i * (item_w + 6)
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


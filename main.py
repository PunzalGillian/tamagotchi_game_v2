import sys
from PyQt5.QtWidgets import QApplication
from src.tamagotchi_widget import TamagotchiApp

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TamagotchiApp()
    window.show()
    sys.exit(app.exec())
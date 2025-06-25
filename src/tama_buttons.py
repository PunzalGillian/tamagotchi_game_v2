from PyQt5.QtWidgets import QPushButton

class TamaButton(QPushButton):
    def __init__(self, label, parent=None, callback=None, x=0, y=0):
        super().__init__(label, parent)
        self.setFixedSize(36, 36)  # 30 * 1.2 = 36
        self.setStyleSheet(
            "border-radius: 18px; background-color: lightgray; border: 3px solid rgb(63,99,171);"
        )
        self.move(x, y)
        if callback:
            self.clicked.connect(callback)

def create_tama_buttons(parent, prev_cb, select_cb, next_cb):
    btn_a = TamaButton("A", parent, prev_cb, 88, 312)   # 73*1.2=88, 260*1.2=312
    btn_b = TamaButton("B", parent, select_cb, 144, 312) # 120*1.2=144
    btn_c = TamaButton("C", parent, next_cb, 202, 312)   # 168*1.2=202
    return btn_a, btn_b, btn_c
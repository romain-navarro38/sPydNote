import itertools
import json
from functools import partial

from PySide6.QtCore import Signal
from PySide6.QtGui import QFont, QColor, QPixmap, QIcon
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QTextEdit, QVBoxLayout, QSpinBox, QMenu, QToolButton, \
    QGridLayout, QWidgetAction

class ColorAction(QWidgetAction):
    colorSelected = Signal(QColor)

    def __init__(self, parent):
        QWidgetAction.__init__(self, parent)
        widget = QWidget(parent)
        layout = QGridLayout(widget)
        layout.setSpacing(0)
        layout.setContentsMargins(2, 2, 2, 2)
        palette = self.palette()
        count = len(palette)
        rows = count // round(count ** .5)
        for row in range(rows):
            for column in range(count // rows):
                color = palette.pop()
                button = QToolButton(widget)
                button.setAutoRaise(True)
                button.clicked[()].connect(
                    lambda color=color: self.handleButton(color))
                pixmap = QPixmap(16, 16)
                pixmap.fill(color)
                button.setIcon(QIcon(pixmap))
                layout.addWidget(button, row, column)
        self.setDefaultWidget(widget)

    def handleButton(self, color):
        self.parent().hide()
        self.colorSelected.emit(color)

    def palette(self):
        return [QColor(r * 255 // 3, g * 255 // 3, b * 255 // 2) for g, r, b in itertools.product(range(4), range(4), range(3))]


class ColorMenu(QMenu):
    def __init__(self, parent):
        QMenu.__init__(self, parent)
        self.colorAction = ColorAction(self)
        self.colorAction.colorSelected.connect(self.handleColorSelected)
        self.addAction(self.colorAction)

    def handleColorSelected(self, color):
        print(color.name())


# noinspection PyAttributeOutsideInit
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setup_ui()

    def setup_ui(self):
        self.create_widgets()
        self.modify_widgets()
        self.create_layouts()
        self.add_widgets_to_layouts()
        self.setup_connections()

    def create_widgets(self):
        self.btn_bold = QPushButton("G")
        self.btn_no_bold = QPushButton("noG")
        self.spin_size = QSpinBox()
        self.color_menu = QPushButton("color")
        self.te_content = QTextEdit()
        self.btn_save = QPushButton("Sauvegarder")
        self.btn_get_text = QPushButton("Recup json")

    def modify_widgets(self):
        self.spin_size.setMinimum(8)
        self.spin_size.setMaximum(20)
        self.spin_size.setSingleStep(2)

    def create_layouts(self):
        self.main_layout = QVBoxLayout(self)

    def add_widgets_to_layouts(self):
        self.main_layout.addWidget(self.btn_bold)
        self.main_layout.addWidget(self.btn_no_bold)
        self.main_layout.addWidget(self.spin_size)
        self.main_layout.addWidget(self.color_menu)
        self.main_layout.addWidget(self.te_content)
        self.main_layout.addWidget(self.btn_save)
        self.main_layout.addWidget(self.btn_get_text)

    def setup_connections(self):
        self.btn_bold.clicked.connect(partial(self.bold, True))
        self.btn_no_bold.clicked.connect(partial(self.bold, False))
        self.spin_size.valueChanged.connect(self.size_font)
        self.color_menu.clicked.connect(self.color)
        self.btn_save.clicked.connect(self.save)
        self.btn_get_text.clicked.connect(self.get_text)

    def bold(self, etat):
        font = QFont()
        font.setBold(etat)
        self.te_content.setCurrentFont(font)

    def size_font(self, value):
        font = QFont()
        font.setPointSize(value)
        self.te_content.setCurrentFont(font)

    def color(self):
        d = ColorMenu(self)
        d.show()

    def save(self):
        with open("essai_text_edit.json", 'w', encoding='utf-8') as f:
            json.dump(self.te_content.toHtml(), f, indent=4)

    def get_text(self):
        with open("essai_text_edit.json", 'r', encoding='utf-8') as f:
            content = json.load(f)
        self.te_content.setHtml(content)


if __name__ == '__main__':
    app = QApplication()
    window = MainWindow()
    window.show()
    app.exec()

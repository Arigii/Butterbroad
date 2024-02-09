import sys

from PyQt5 import uic
from PyQt5.QtCore import QMimeData, Qt, QPoint
from PyQt5.QtGui import QPixmap, QDrag, QDropEvent

from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QListWidgetItem, QListWidget, QMessageBox


class MainWin(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('win/MainWin.ui', self)
        self.is_open = False
        self.setAcceptDrops(True)
        self.widget.setVisible(False)
        self.pushButton.clicked.connect(self.change_open)
        self.pushButton_2.clicked.connect(self.change_open)
        self.ingredients = self.children()[1].children()[1].children()[1:]
        self.hamburger = []
        self.render_ingredients()

    def render_ingredients(self):
        for i in self.ingredients:
            if i.children()[1].children()[0].count() == 0:
                ingredients = Ingredient(i.objectName().split('_')[-1])
                ingredients.resize(i.size())
                i.children()[1].children()[0].addWidget(ingredients)

    def render_hamburger(self):
        self.listWidget.clear()
        for i in self.hamburger[::-1]:
            item = HamburgerItem(i.type_ingr)
            list_itwm = QListWidgetItem()
            self.listWidget.addItem(list_itwm)
            self.listWidget.setItemWidget(list_itwm, item)

    def dragEnterEvent(self, e):
        e.accept()

    def check_hamburger(self):
        lst = list(map(lambda i: i.type_ingr, self.hamburger))
        if lst[0] != 'bottom':
            self.ms = QMessageBox()
            self.ms.setWindowTitle('Игра окончена')
            self.ms.setText('Бутерброд должен начинаться с нижней булки')
            self.ms.setIcon(QMessageBox.Warning)
            self.ms.show()
            self.hamburger.clear()
            self.render_hamburger()
        if lst[0] == 'bottom' and lst[-1] == 'top':
            if len(lst) > 2 and any(list(map(lambda x: x not in ['top', 'bottom'], lst))):
                self.ms = QMessageBox()
                self.ms.setWindowTitle('Игра окончена')
                self.ms.setText('Бутерброд создан')
                self.ms.setIcon(QMessageBox.Information)
                self.ms.show()
                self.hamburger.clear()
                self.render_hamburger()
            elif len(lst) == 2:
                self.ms = QMessageBox()
                self.ms.setWindowTitle('Игра окончена')
                self.ms.setText('Это не Бутерброд')
                self.ms.setIcon(QMessageBox.Warning)
                self.ms.show()
                self.hamburger.clear()
                self.render_hamburger()


    def dropEvent(self, e: QDropEvent):
        pos = e.pos()
        widget = e.source()
        wdg = self.childAt(QPoint(int(pos.x()), int(pos.y())))
        if wdg.objectName() == "qt_scrollarea_viewport" or type(wdg) == HamburgerItem:
            self.hamburger.append(widget)
            self.render_ingredients()
            self.render_hamburger()
            self.check_hamburger()

    def change_open(self):
        self.is_open = not self.is_open
        self.pushButton.setVisible(self.is_open)
        self.widget.setVisible(not self.is_open)


class HamburgerItem(QLabel):
    def __init__(self, type_ingr: str):
        super().__init__()
        self.type_ingr = type_ingr
        self.setMinimumHeight(30)
        self.setPixmap(QPixmap(f"img/hamburger/{type_ingr}.svg"))


class Ingredient(QLabel):
    def __init__(self, type_ingr: str):
        super().__init__()
        self.type_ingr = type_ingr
        self.setPixmap(QPixmap(f"img/fridge/{type_ingr}.svg"))
        if type_ingr != 'onion':
            self.setScaledContents(True)

    def mouseMoveEvent(self, e):
        if e.buttons() == Qt.LeftButton:
            drag = QDrag(self)
            mime = QMimeData()
            drag.setMimeData(mime)

            pixmap = QPixmap(self.size())
            self.render(pixmap)
            drag.setPixmap(pixmap)

            drag.exec_(Qt.MoveAction)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWin()
    win.show()
    sys.exit(app.exec())

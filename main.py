from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from os import listdir
from os.path import isfile, join
import sys

class Ui_MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.list_of_labels = []
        self.rectangles = []
        self.photo_displayed = 0

        self.window = MainWindow

        self.window_width, self.window_height = 800, 600
        self.setMinimumSize(self.window_width, self.window_height)
        self.setWindowTitle('Fotograf')

        self.centralwidget = QtWidgets.QWidget(self.window)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(639, 0, 161, 201))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.open_btn = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.open_btn.setObjectName("open_btn")
        self.gridLayout.addWidget(self.open_btn, 0, 0, 1, 1)
        self.save_btn = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.save_btn.setObjectName("save_btn")
        self.gridLayout.addWidget(self.save_btn, 1, 0, 1, 1)
        self.stats_btn = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.stats_btn.setObjectName("stats_btn")
        self.gridLayout.addWidget(self.stats_btn, 3, 0, 1, 1)
        self.select_btn = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.select_btn.setObjectName("select_btn")
        self.gridLayout.addWidget(self.select_btn, 2, 0, 1, 1)
        self.list = QtWidgets.QListWidget(self.centralwidget)
        self.list.setGeometry(QtCore.QRect(640, 200, 161, 361))
        self.list.setObjectName("list")
        self.photo = QtWidgets.QLabel(self.centralwidget)
        self.photo.setGeometry(QtCore.QRect(-1, -5, 641, 531))
        self.photo.setText("")
        self.photo.setScaledContents(True)
        self.photo.setObjectName("photo")
        self.current_photo = QPixmap('grape.jpg')
        self.prev = QtWidgets.QPushButton(self.centralwidget)
        self.prev.setGeometry(QtCore.QRect(240, 530, 81, 32))
        self.prev.setObjectName("prev")
        self.next = QtWidgets.QPushButton(self.centralwidget)
        self.next.setGeometry(QtCore.QRect(320, 530, 81, 32))
        self.next.setObjectName("next")
        self.edit_btn = QtWidgets.QPushButton(self.centralwidget)
        self.edit_btn.setGeometry(QtCore.QRect(650, 210, 71, 32))
        self.edit_btn.setObjectName("edit_btn")
        self.remove_btn = QtWidgets.QPushButton(self.centralwidget)
        self.remove_btn.setGeometry(QtCore.QRect(720, 210, 71, 32))
        self.remove_btn.setObjectName("remove_btn")
        self.window.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        self.window.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        self.window.setStatusBar(self.statusbar)
        self.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        #laczenie przyciskow z metodami
        self.next.clicked.connect(self.next_photo)
        self.prev.clicked.connect(self.prev_photo)
        self.open_btn.clicked.connect(self.open_directory)
        self.save_btn.clicked.connect(self.save)
        self.select_btn.clicked.connect(self.select)
        self.edit_btn.clicked.connect(self.edit_label)
        self.remove_btn.clicked.connect(self.remove_label)

        self.begin = QtCore.QPoint()
        self.end = QtCore.QPoint()
        self.selecting = False

        self.show()


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.open_btn.setText(_translate("MainWindow", "Open"))
        self.save_btn.setText(_translate("MainWindow", "Save"))
        self.stats_btn.setText(_translate("MainWindow", "Show Statistics"))
        self.select_btn.setText(_translate("MainWindow", "Draw labels"))
        self.prev.setText(_translate("MainWindow", "<<"))
        self.next.setText(_translate("MainWindow", ">>"))
        self.edit_btn.setText(_translate("MainWindow", "Edit"))
        self.remove_btn.setText(_translate("MainWindow", "Remove"))


    #przelaczenie na kolejne zdjecie
    #do zrobienia: zmienianie sie listy z boxami przy zmianie zdjecia
    def next_photo(self):
        try:
            self.photo_displayed += 1
            if self.photo_displayed >= len(self.files):
                self.photo_displayed = 0
            self.current_photo = QtGui.QPixmap("{}/{}".format(self.chosen_dir, self.files[self.photo_displayed]))
            self.photo.setPixmap(self.current_photo)
            self.selecting = False
            self.select_btn.setText("Draw labels")
            self.rectangles = []
        except:
            print("Brak załadowanego folderu")


    #przelaczanie na poprzednie zdjecie
    #do zrobienia zmienianie sie listy z boxami przy zmianie zdjecia
    def prev_photo(self):
        try:
            self.photo_displayed -= 1
            if self.photo_displayed < 0:
                self.photo_displayed = len(self.files)-1
            self.current_photo = QtGui.QPixmap("{}/{}".format(self.chosen_dir, self.files[self.photo_displayed]))
            self.photo.setPixmap(self.current_photo)
            self.selecting = False
            self.select_btn.setText("Draw labels")
            self.rectangles = []
        except:
            print("Brak załadowanego folderu")


    def open_directory(self):
        #otwieranie folderow i wybranie folderu tu bedzie
        try:
            self.chosen_dir = QtWidgets.QFileDialog.getExistingDirectory(None, 'Select project folder:', '',
                                                              QtWidgets.QFileDialog.ShowDirsOnly)

            print(self.chosen_dir)
            self.files = [f for f in listdir(self.chosen_dir) if isfile(join(self.chosen_dir, f))
                          and f.lower().endswith(('.png', '.jpg', '.jpeg', '.pneg'))]
            print(self.files)
            self.photo.setPixmap(self.current_photo)
        except:
            pass

    def save(self):
        pass
        #zapisywanie

    def select(self):
        if not self.selecting:
            self.selecting = True
            self.begin = QPoint()
            self.end = QPoint()
            self.select_btn.setText("Drawing labels...")
            print('Drawing mode - true')
            self.photo.clear()

        elif self.selecting:
            self.selecting = False
            self.select_btn.setText("Draw labels")
            print('Drawing mode - false')
            self.photo.setPixmap(self.current_photo)

        #przelaczenie na tryb rysowania bounding boxow

    def show_stats(self):
        pass
        #wyswietlanie statystyk

    def edit_label(self):
        if not self.canvas.editing():
            return
        item = self.current_item()
        if not item:
            return
        text = self.label_dialog.pop_up(item.text())
        if text is not None:
            item.setText(text)
            item.setBackground(generate_color_by_text(text))
            self.set_dirty()
            self.update_combo_box()
        #edycja nazwy bounding boxa

    def remove_label(self):
        if shape is None:
            return
        item = self.shapes_to_items[shape]
        self.label_list.takeItem(self.label_list.row(item))
        del self.shapes_to_items[shape]
        del self.items_to_shapes[item]
        self.update_combo_box()
        #usuniecie zaznaczonego bounding boxa

    def save_rect(self, name, begin, end, photo_id):
        self.list_of_labels.append([name, begin, end, photo_id])

    def paintEvent(self, event):
        if self.selecting:
            super().paintEvent(event)
            qp = QPainter(self)
            qp.drawPixmap(QRect(-1, -5, 641, 531), self.current_photo)
            br = QBrush(QColor(255, 10, 10, 10))
            qp.setBrush(br)

            for rectangle in self.rectangles:
                qp.drawRect(rectangle)

            if not self.begin.isNull() and not self.end.isNull():
                qp.drawRect(QRect(self.begin, self.end).normalized())

    def mousePressEvent(self, event):
        if self.selecting:
            self.begin = event.pos()

    def mouseMoveEvent(self, event):
        if self.selecting:
            self.end = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if self.selecting:
            self.end = event.pos()
            r = QRect(self.begin, self.end).normalized()
            self.rectangles.append(r)

            self.textbox = QLineEdit(self)
            self.label_name, ok = QInputDialog.getText(self, 'Name label', 'Enter your label name:')
            if ok:
                self.save_rect(self.label_name, self.begin, self.end, self.photo_displayed)

            print (self.list_of_labels)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    sys.exit(app.exec_())

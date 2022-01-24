from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from os import listdir
from os.path import isfile, join
import sys
import datetime
import json
import imagesize

class Ui_MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.list_of_labels = []
        self.rectangles = []
        self.photo_displayed = 0
        self.categories = []
        self.files = []
        self.label_name = ""
        self.current_photo = None

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
        self.gridLayout.addWidget(self.stats_btn, 5, 0, 1, 1)
        self.load_btn = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.load_btn.setObjectName("load_btn")
        self.gridLayout.addWidget(self.load_btn, 2, 0, 1, 1)
        self.select_btn = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.select_btn.setObjectName("select_btn")
        self.gridLayout.addWidget(self.select_btn, 3, 0, 1, 1)
        self.name_btn = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.name_btn.setObjectName("name_btn")
        self.gridLayout.addWidget(self.name_btn, 4, 0, 1, 1)
        self.list = QtWidgets.QListWidget(self.centralwidget)
        self.list.setGeometry(QtCore.QRect(640, 200, 161, 361))
        self.list.setObjectName("list")
        self.photo = QtWidgets.QLabel(self.centralwidget)
        self.photo.setGeometry(QtCore.QRect(-1, -5, 641, 531))
        self.photo.setText("")
        self.photo.setScaledContents(True)
        self.photo.setObjectName("photo")
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

        self.description = QLabel(self)

        self.listwidget = QListWidget(self.centralwidget)
        self.listwidget.setGeometry(QtCore.QRect(650, 250, 142, 300))

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
        self.listwidget.itemClicked.connect(self.highlight_label)
        self.next.clicked.connect(self.next_photo)
        self.prev.clicked.connect(self.prev_photo)
        self.open_btn.clicked.connect(self.open_directory)
        self.save_btn.clicked.connect(self.save)
        self.name_btn.clicked.connect(self.name)
        self.load_btn.clicked.connect(self.load)
        self.select_btn.clicked.connect(self.select)
        self.edit_btn.clicked.connect(self.edit_label)
        self.remove_btn.clicked.connect(self.remove_label)
        self.stats_btn.clicked.connect(self.show_stats)

        self.begin = QtCore.QPoint()
        self.end = QtCore.QPoint()
        self.selecting = False

        self.show()


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.open_btn.setText(_translate("MainWindow", "Open"))
        self.save_btn.setText(_translate("MainWindow", "Save to COCO"))
        self.name_btn.setText(_translate("MainWindow", "Set label name"))
        self.load_btn.setText(_translate("MainWindow", "Load COCO file"))
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
            self.current_photo = QPixmap(str(self.chosen_dir) + "/" + str(self.files[0]))
            self.photo.setPixmap(self.current_photo)
        except:
            pass

    def save(self):
        data_coco = {}
        data_coco["info"] =\
            {
                "year": "2022",
                "version": "1.0",
                "description": "Test",
                "contributor": "karol",
                "url": "https://github.com/martaadamczyk0101/fotograf",
                "date_created": str(datetime.datetime.now())
            }
        data_coco["licenses"] =\
        [
            {
              "url": "http://creativecommons.org/licenses/by-nc-sa/2.0/",
              "id": 0,
              "name": "Attribution-NonCommercial-ShareAlike License"

            }
        ]

        data_coco["images"] = []

        for i in range(len(self.files)):
            width, height = imagesize.get(str(self.chosen_dir)+"/"+str(self.files[i]))
            dic = {"id": i,
                    "license": 0,
                    "file_name": self.files[i],
                    "height": height,
                    "width": width,
                    "date_captured": None
                   }
            data_coco["images"].append(dic)

        data_coco["categories"] = []

        for i in range(len(self.categories)):
            dic = {"id": i,
                   "category": self.categories[i]
                   }
            data_coco["categories"].append(dic)

        data_coco["annotations"] = []

        for i in range(len(self.list_of_labels)):
            for j in range(len(self.categories)):
                if self.categories[j] == self.list_of_labels[i][0]:
                    cat_id = j
            dic = {"id": i,
                    "image_id": self.list_of_labels[i][2],
                    "category_id": cat_id,
                    "bbox": self.list_of_labels[i][1],
                    "segmentation": None,
                    "area": None,
                    "iscrowd": None
                   }
            data_coco["annotations"].append(dic)

        print(data_coco)

        json.dump(data_coco, open("test.json", "w"), indent=4)

        #zapisywanie

    def load(self):
        path_coco = QFileDialog.getOpenFileName(self, "Load COCO file", "~", "JSON files (*.json)")
        with open(path_coco[0]) as jsonFile:
            loaded_data = json.load(jsonFile)
            jsonFile.close()

        self.list_of_labels = []

        for ann in loaded_data['annotations']:
            temp_list = [ann['category_id'], ann['bbox'], ann['image_id']]
            begin = QPoint(ann['bbox'][0], ann['bbox'][1])
            end = QPoint(ann['bbox'][2], ann['bbox'][3])
            r = QRect(begin, end)

            self.rectangles.append([r, ann['image_id']])
            self.list_of_labels.append(temp_list)

        for ann in self.list_of_labels:
            for category in loaded_data['categories']:
                if ann[0] == category['id']:
                    ann[0] = category['category']

        for label in self.list_of_labels:
            self.display_label(label[0], label[1])

        print(self.list_of_labels)

    def name(self):
        self.textbox = QLineEdit(self)
        self.label_name, ok = QInputDialog.getText(self, 'Name label', 'Enter your label name:')
        if ok:
            if self.label_name not in self.categories:
                self.categories.append(self.label_name)

    def select(self):
        if self.current_photo:
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
        print("xdd")
        stats = QMessageBox()
        stats.setWindowTitle("Statistics")

        labels_counted = {}

        for label in self.list_of_labels:
            if label[0] not in labels_counted:
                labels_counted[label[0]] = 1
            else:
                labels_counted[label[0]] = labels_counted[label[0]] + 1

        labels_counted = dict(sorted(labels_counted.items(),
                                     key=lambda item: item[1],
                                     reverse=True))
        #print(labels_counted)

        text = ""

        for lab in labels_counted:
            text += lab + ": " + str(labels_counted[lab]) + "\n"

        stats.setText("Number of files loaded: {} \nNumber of annotations: {} \n"\
                      .format(len(self.files),len(self.list_of_labels))+text)
        stats.exec_()



    def edit_label(self):
        edited_name, ok = QInputDialog.getText(self, 'Edit name', 'Edit name of the label:')
        if ok:
            for label in self.list_of_labels:
                if label[1] == self.current_label_cords:
                    label[0] = edited_name
            self.description.setText(edited_name)
            self.listwidget.currentItem().setText("{} {}".format(edited_name, self.current_label_cords))

    def remove_label(self):
        if self.list_of_labels:
            for label in self.list_of_labels:
                if label[1] == self.current_label_cords:
                    self.list_of_labels.remove(label)

            self.rectangles.remove(self.rectangles[self.listwidget.currentRow()])
            self.listwidget.takeItem(self.listwidget.currentRow())
            self.begin = QPoint(0, 0)
            self.end = QPoint(0, 0)
            self.description.setText("")
            self.update()

    def save_rect(self, name, cords, photo_id):
        self.list_of_labels.append([name, cords, photo_id])

    def display_label(self, name, cords):
        self.listwidget.addItem("{} {}".format(name, cords))

    def highlight_label(self, item):
        temp = item.text().split("[")
        name, cords = temp[0], temp[1]
        cords = cords[:-1].split(", ")
        cords = list(map(int, cords))
        self.current_label_cords = cords

        self.description.move(cords[0], cords[3]-5)
        self.description.setText(name)

    def paintEvent(self, event):
        if self.selecting:
            super().paintEvent(event)
            qp = QPainter(self)
            qp.drawPixmap(QRect(-1, -5, 641, 531), self.current_photo)
            br = QBrush(QColor(255, 10, 10, 80))
            qp.setBrush(br)
            print(self.rectangles)
            for rectangle in self.rectangles:
                if rectangle[1] == self.photo_displayed:
                    qp.drawRect(rectangle[0])

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

            self.rectangles.append([r, self.photo_displayed])


            self.cords = [self.begin.x(), self.begin.y(), self.end.x(), self.end.y()]
            self.save_rect(self.label_name, self.cords, self.photo_displayed)
            self.display_label(self.label_name, self.cords)

            print(self.list_of_labels)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    sys.exit(app.exec_())

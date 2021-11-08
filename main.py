from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from os import listdir
from os.path import isfile, join
#comment
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
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
        self.photo.setPixmap(QtGui.QPixmap("/Users/martaadamczyk/Desktop/img/img1.jpg"))
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
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

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


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.open_btn.setText(_translate("MainWindow", "Open"))
        self.save_btn.setText(_translate("MainWindow", "Save"))
        self.stats_btn.setText(_translate("MainWindow", "Show Statistics"))
        self.select_btn.setText(_translate("MainWindow", "Select"))
        self.prev.setText(_translate("MainWindow", "<<"))
        self.next.setText(_translate("MainWindow", ">>"))
        self.edit_btn.setText(_translate("MainWindow", "Edit"))
        self.remove_btn.setText(_translate("MainWindow", "Remove"))

        #do tego trzeba zrobic okienko z wybieraniem directory i te mydir ma byc pobierane przez klikniecie na wybrany folder
        self.mydir= "/Users/karol/Desktop/img"
        self.photo_displayed= 0
        self.files= [f for f in listdir(self.mydir) if isfile(join(self.mydir, f))]
        print(self.files)

    #przelaczenie na kolejne zdjecie
    #do zrobienia: zmienianie sie listy z boxami przy zmianie zdjecia
    def next_photo(self):
        self.photo_displayed+=1
        if self.photo_displayed>=len(self.files):
            self.photo_displayed=0
        self.photo.setPixmap(QtGui.QPixmap("{}/{}".format(self.mydir, self.files[self.photo_displayed])))

    #przelaczanie na poprzednie zdjecie
    #do zrobienia zmienianie sie listy z boxami przy zmianie zdjecia
    def prev_photo(self):
        self.photo_displayed-=1
        if self.photo_displayed<0:
            self.photo_displayed=len(self.files)-1
        self.photo.setPixmap(QtGui.QPixmap("{}/{}".format(self.mydir, self.files[self.photo_displayed])))

    def open_directory(self):
        print("otwarte")
        #otwieranie folderow i wybranie folderu tu bedzie

    def save(self):
        pass
        #zapisywanie

    def select(self):
        pass
        #przelaczenie na tryb rysowania bounding boxow

    def show_stats(self):
        pass
        #wyswietlanie statystyk

    def edit_label(self):
        pass
        #edycja nazwy bounding boxa

    def remove_label(self):
        pass
        #usuniecie zaznaczonego bounding boxa

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
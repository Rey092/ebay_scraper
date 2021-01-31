import csv  # for .csv creation
import itertools  # for infinite "for loop"
import re  # method .sub for some text editing
import threading

import pandas as pd  # excel
import requests  # raw data scraping
from PyQt5 import QtCore, QtGui, QtWidgets
from bs4 import BeautifulSoup  # get information from raw data

baselink = ""


class UiMainWindow(object):
    def __init__(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(801, 336)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setLayoutDirection(QtCore.Qt.LeftToRight)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setStyleSheet("background: rgb(170, 255, 127)rgb(237, 255, 226)")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.line1 = QtWidgets.QLineEdit(self.centralwidget)
        self.line1.setGeometry(QtCore.QRect(20, 40, 471, 31))
        self.line1.setObjectName("line1")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(500, 0, 291, 231))
        self.label.setStyleSheet("")
        self.label.setText("")
        self.label.setTextFormat(QtCore.Qt.PlainText)
        self.label.setPixmap(QtGui.QPixmap("F:/Pywork/Project1/project/1.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.button1 = QtWidgets.QPushButton(self.centralwidget)
        self.button1.setGeometry(QtCore.QRect(380, 80, 111, 31))
        self.button1.setStyleSheet(
            "background: qconicalgradient(cx:0, cy:0, angle:135, stop:0 rgba(255, 255, 0, 69), stop:0.375 rgba(255, 255, 0, 69), stop:0.423533 rgba(251, 255, 0, 145), stop:0.45 rgba(247, 255, 0, 208), stop:0.477581 rgba(255, 244, 71, 130), stop:0.518717 rgba(255, 218, 71, 130), stop:0.55 rgba(255, 255, 0, 255), stop:0.57754 rgba(255, 203, 0, 130), stop:0.625 rgba(255, 255, 0, 69), stop:1 rgba(255, 255, 0, 69))")
        self.button1.setObjectName("button1")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(20, 0, 471, 31))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(20, 80, 341, 31))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(20, 130, 471, 41))
        self.label_4.setObjectName("label_4")
        self.line1_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.line1_2.setGeometry(QtCore.QRect(20, 170, 471, 31))
        self.line1_2.setObjectName("line1_2")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(20, 210, 341, 31))
        self.label_5.setObjectName("label_5")
        self.button1_2 = QtWidgets.QPushButton(self.centralwidget)
        self.button1_2.setGeometry(QtCore.QRect(380, 210, 111, 31))
        self.button1_2.setStyleSheet(
            "background: qconicalgradient(cx:0, cy:0, angle:135, stop:0 rgba(255, 255, 0, 69), stop:0.375 rgba(255, 255, 0, 69), stop:0.423533 rgba(251, 255, 0, 145), stop:0.45 rgba(247, 255, 0, 208), stop:0.477581 rgba(255, 244, 71, 130), stop:0.518717 rgba(255, 218, 71, 130), stop:0.55 rgba(255, 255, 0, 255), stop:0.57754 rgba(255, 203, 0, 130), stop:0.625 rgba(255, 255, 0, 69), stop:1 rgba(255, 255, 0, 69))")
        self.button1_2.setObjectName("button1_2")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(110, 260, 611, 23))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 801, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.button1.clicked.connect(self.first_line_check)
        self.button1_2.clicked.connect(self.second_line_check)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def first_line_check(self):
        global baselink
        baselink = str(self.line1.text())
        launch_Thread1()

    def second_line_check(self):
        global baselink
        baselink = str(self.line1_2.text())
        launch_Thread1()

    def progress_update(self, max=10, min=0):
        self.progressBar.setProperty("value", min)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.button1.setText(_translate("MainWindow", "GO"))
        self.label_5.setText(_translate("MainWindow",
                                        "<html><head/><body><p><span style=\" font-size:10pt; "
                                        "font-style:italic;\">example:</span><span style=\" font-size:10pt;\"> "
                                        "Смартфон, Холодильник</span></p><p><br/></p></body></html>"))
        self.button1_2.setText(_translate("MainWindow", "GO"))


def launch_Thread1():
    t = threading.Thread(target=parser1, daemon=True)
    print("hi")
    t.start()
    print("hi2")


def launch_Thread2():
    t = threading.Thread(target=parser1, daemon=True)
    t.start()


def parser1():
    # Create rozetka_items as empty list. firstPage its basic url (also page 1). i its iteration (and also page) counter.
    rozetka_items = []
    firstPage = baselink
    i, k = 1, 1

    # for page in itertools.count(start=1):
    #     soup_ingr = requests.get(
    #         firstPage + "&page={}/".format(str(page)))
    #
    #     if soup_ingr.url == firstPage and k != 1:  # Check redirect to first page (pages out). If True -> break.
    #         break
    #     k += 1

    # Make a request
    for page in itertools.count(start=1):
        soup_ingr = requests.get(
            firstPage + "&page={}/".format(str(page)))
        soup = BeautifulSoup(soup_ingr.content, 'lxml')  # Lets cook the soup.

        if soup_ingr.url == firstPage and i != 1:  # Check redirect to first page (pages out). If True -> break.
            print("Page {} is Not Exist. End Scraping".format(i))
            break
        print("Page {} is uploaded".format(i))
        # UiMainWindow(MainWindow).progress_update(k, i)

        # Extract data according to instructions to 'info' and store it into 'rozetka_items'
        products = soup.select('.goods-tile__inner')
        for elem in products:
            title = elem.select('.goods-tile__title')[0].text \
                .replace(" Официальная гарантия", "")
            title = re.sub(r"\([^()]*\)", "", title)
            reviews = elem.select('.goods-tile__reviews-link')[0].text \
                .replace("Оставить отзыв", "0") \
                .replace(" отзыва", "") \
                .replace(" отзывов", "") \
                .replace(" отзыв", "")
            try:
                price = str(elem.select('.goods-tile__price-value')[0].text)
            except:
                price = "No Price"
            if "\xa0" in price:
                price.replace("\xa0", "")
            info = {
                "Название": title.strip(),
                "Отзывы": reviews.strip(),
                "Цена": price.strip()
            }
            rozetka_items.append(info)
        i += 1  # iteration & page counter +=1

    keys = rozetka_items[0].keys()  # get keys from 'rozetka_items'
    with open('products.csv', 'w', newline='') as output_file:  # write .csv
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(rozetka_items)

    read_file = pd.read_csv(r'products.csv')  # read csv with 'pandas' and convert it then
    read_file.to_excel(r'products.xlsx', index=None, header=True)

    print(".csv and .xls creation is done")


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = UiMainWindow(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

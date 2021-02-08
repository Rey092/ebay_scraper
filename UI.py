from PyQt5 import QtCore, QtGui, QtWidgets

import scraper


class Ui_MainWindow(object):
    def setup_ui(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(675, 121)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setEnabled(True)
        self.centralwidget.setMaximumSize(QtCore.QSize(675, 121))
        self.centralwidget.setObjectName("centralwidget")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(40, 20, 441, 21))
        self.lineEdit.setObjectName("lineEdit")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(460, -10, 241, 121))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(r"img\ebay-logo-1-1200x630-margin.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(250, 50, 231, 31))
        self.pushButton.setObjectName("pushButton")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(30, 60, 211, 16))
        self.label_2.setObjectName("label_2")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(40, 90, 611, 23))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(0, -10, 691, 171))
        self.label_3.setStyleSheet("")
        self.label_3.setText("")
        self.label_3.setPixmap(QtGui.QPixmap(r"img\GettyImages-1164051562-1024x683.jpg"))
        self.label_3.setObjectName("label_3")
        self.label_3.raise_()
        self.lineEdit.raise_()
        self.label.raise_()
        self.pushButton.raise_()
        self.label_2.raise_()
        self.progressBar.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        # self.pushButton.clicked.connect(self.press_button)
        self.pushButton.clicked.connect(self.start_qt_thread)
        self.translate_ui(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def translate_ui(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Ebay Scraper"))
        self.pushButton.setText(_translate("MainWindow", "Start"))
        self.label_2.setText(_translate("MainWindow",
                                        "<html><head/><body><p><span style=\" font-size:10pt; "
                                        "font-weight:600;\">Input Keyword and press "
                                        "&quot;Start&quot;</span></p></body></html>"))

    def start_qt_thread(self):
        keyword = str(self.lineEdit.text())
        thread_count = 1
        # thread_count = QtCore.QThreadPool.globalInstance().maxThreadCount()
        self.pushButton.setEnabled(False)
        self.lineEdit.setEnabled(False)
        for i in range(thread_count):
            print(f"Threads number: {i + 1}")
            runnable = Runnable(keyword, self.progressBar, self.pushButton, self.lineEdit)
            QtCore.QThreadPool.globalInstance().start(runnable)


class Runnable(QtCore.QRunnable):
    def __init__(self, keyword, progressbar, push, line):
        QtCore.QRunnable.__init__(self)
        self.push = push
        self.line = line
        self.keyword = keyword
        self.progressbar = progressbar

    def run(self):
        scraper.scraper(self.keyword, self.progressbar, self.push, self.line)

        # time.sleep(random.randint(700, 2500) / 1000)


def activate_ui():
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setup_ui(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

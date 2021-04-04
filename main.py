import sys 
from PyQt5 import QtWidgets
import ui.mainWindow 
import ui.dataWindow

class MainWindow(QtWidgets.QMainWindow, ui.mainWindow.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.searchButton.clicked.connect(self.gotoDataWindow)


    def gotoDataWindow(self):
        dataWindow = DataWindow()
        widget.addWidget(dataWindow)
        widget.setCurrentIndex(widget.currentIndex()+1)
        

class DataWindow(QtWidgets.QMainWindow, ui.dataWindow.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.gotoMainWindow)


    def gotoMainWindow(self):
        mainWindow = MainWindow()
        widget.addWidget(mainWindow)
        widget.setCurrentIndex(widget.currentIndex()+1)



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    widget = QtWidgets.QStackedWidget()
    mainWindow = MainWindow()
    dataWindow = DataWindow()
    widget.addWidget(mainWindow)
    widget.addWidget(dataWindow)
    widget.show()
    app.exec_()
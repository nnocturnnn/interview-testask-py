import sys 
from PyQt5 import QtWidgets
import ui.mainWindow as mainWindow
import ui.dataWindow as dataWindow

class WeatherMainWindow(QtWidgets.QMainWindow, mainWindow.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.searchButton.clicked.connect(self.gotoDataWindow)


    def gotoDataWindow(self):
        self.close()
        city = self.seachBox.text()
        self.twoWindow = WeatherDataWindow(city)
        self.twoWindow.show()
        

class WeatherDataWindow(QtWidgets.QMainWindow, dataWindow.Ui_MainWindow):
    data = ""
    def __init__(self,data):
        super().__init__()
        self.setupUi(self)
        self.data = data
        self.pushButton.clicked.connect(self.gotoMainWindow)

    def gotoMainWindow(self):
        self.close()
        self.twoWindow = WeatherMainWindow()
        self.twoWindow.show()


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = WeatherMainWindow()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main() 
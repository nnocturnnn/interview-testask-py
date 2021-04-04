import sys 
from PyQt5 import QtWidgets
import ui.mainWindow as mainWindow
import ui.dataWindow as dataWindow
import weather

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
    def __init__(self,place):
        super().__init__()
        self.setupUi(self)
        data = weather.get_owm_now(place)
        self.init_labels(data,place)
        self.pushButton.clicked.connect(self.gotoMainWindow)

    def init_labels(self, data, place):
        if not place:
            self.cityLabel.setText("Current city")
        else:
            self.cityLabel.setText(place)
        self.timeLabel.setText(data['time'].strftime("%m/%d/%Y, %H:%M:%S"))
        self.temperatureLabel.setText(data['temp']['temp'] + "°")
        self.statusLabel.setText(data['status'])
        self.max_minLabel.setText((data['temp']['temp_min'] + "°/" + 
                                    data['temp']['temp_max'] + "°"))

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
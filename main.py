import sys 
from PyQt5 import QtWidgets, QtGui
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
        self.timeLabel.setText(data['time'].strftime("%H:%M:%S"))
        self.temperatureLabel.setText(data['temp']['temp'] + "°")
        self.statusLabel.setText(data['status'])
        self.max_minLabel.setText((data['temp']['temp_min'] + "°/" + 
                                    data['temp']['temp_max'] + "°"))
        self.iconLabel.setPixmap(QtGui.QPixmap(f"./img/{data['status']}.png"))
        self.iconLabel.setScaledContents(True)
        list_data = weather.get_own_three_hour(place)
        list_box = [self.groupBox,self.groupBox_2,self.groupBox_3,self.groupBox_4]
        for i in range(len(list_box)):
            list_children = list_box[i].children()
            list_data_for_child = list_data[i]
            list_children[0].setText(list_data_for_child[0])
            list_children[1].setText(list_data_for_child[1]['temp'] + "°")
            list_children[2].setPixmap(QtGui.QPixmap(f"./img/{list_data_for_child[2]}.png"))
            list_children[2].setScaledContents(True)


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
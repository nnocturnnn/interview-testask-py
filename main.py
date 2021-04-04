import sys 
from PyQt5 import QtWidgets, QtGui, QtCore
import src.mainWindow as mainWindow
import src.dataWindow as dataWindow
import src.weather as weather

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
        self.init_labels(place)
        self.pushButton.clicked.connect(self.gotoMainWindow)

    def init_labels(self, place):
        list_box = [self.groupBox,self.groupBox_2,self.groupBox_3,self.groupBox_4]
        
        try:
            data = weather.get_owm_now(place)
            list_data = weather.get_own_three_hour(place)
        except:
            msgBox = QtWidgets.QMessageBox()
            msgBox.setIcon(QtWidgets.QMessageBox.Information)
            msgBox.setText("Error handl this city")
            returnValue = msgBox.exec()
        else:
            if not place:
                self.cityLabel.setText("Current city")
            else:
                self.cityLabel.setText(place)
            
            self.timeLabel.setText(data['time'].strftime("%H:%M"))
            self.temperatureLabel.setText(data['temp']['temp'] + "°")
            self.statusLabel.setText(data['status'])
            self.max_minLabel.setText((data['temp']['temp_min'] + "°/" + 
                                        data['temp']['temp_max'] + "°"))
            self.iconLabel.setPixmap(QtGui.QPixmap(f"./img/{data['status']}.png"))
            self.iconLabel.setScaledContents(True)

            for i in range(len(list_box)):
                list_child = list_box[i].children()
                data_for_child = list_data[i]
                list_child[0].setText(data_for_child[0])
                list_child[0].setAlignment(QtCore.Qt.AlignCenter)
                list_child[1].setText(data_for_child[1]['temp'] + "°")
                list_child[1].setAlignment(QtCore.Qt.AlignCenter)
                list_child[2].setPixmap(QtGui.QPixmap(f"./img/{data_for_child[2]}.png"))
                list_child[2].setScaledContents(True)


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
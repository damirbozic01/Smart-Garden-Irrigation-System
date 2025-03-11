import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QStatusBar
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QFont
import requests
import random


class SmartGarden(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Smart Garden")
        self.setGeometry(100, 100, 750, 635)
        
        self.manual_mode = False  
        self.city = "Varaždin"
        self.api_key = "YOUR_OPENWEATHER_API_KEY"  

        
        self.setup_ui()

        
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_data)
        self.timer.start(60000)  

        
        self.update_weather()
        self.update_moisture()

    def setup_ui(self):
        
        self.label_weather = QLabel("Weather", self)
        self.label_weather.setGeometry(10, 90, 711, 81)
        self.label_weather.setStyleSheet("background-color: rgb(0, 85, 255);")
        self.label_weather.setFont(QFont("Segoe UI", 22, QFont.Bold))
        self.label_weather.setAlignment(Qt.AlignCenter)

        self.label_moisture = QLabel("Moisture", self)
        self.label_moisture.setGeometry(10, 220, 711, 81)
        self.label_moisture.setStyleSheet("background-color: rgb(85, 0, 255);")
        self.label_moisture.setFont(QFont("Segoe UI", 22, QFont.Bold))
        self.label_moisture.setAlignment(Qt.AlignCenter)

        self.label_status = QLabel("Status", self)
        self.label_status.setGeometry(10, 340, 711, 71)
        self.label_status.setStyleSheet("background-color: rgb(255, 0, 0);")
        self.label_status.setFont(QFont("Segoe UI", 22, QFont.Bold))
        self.label_status.setAlignment(Qt.AlignCenter)

        
        self.push_button_manual = QPushButton("Manual", self)
        self.push_button_manual.setGeometry(194, 10, 361, 61)
        self.push_button_manual.setStyleSheet("background-color: rgb(0, 170, 0);")
        self.push_button_manual.setFont(QFont("Segoe UI", 26, QFont.Bold))
        self.push_button_manual.clicked.connect(self.manual_override)

        
        self.statusbar = QStatusBar(self)
        self.setStatusBar(self.statusbar)

    def update_data(self):
        if not self.manual_mode:
            self.update_weather()
            self.update_moisture()
            self.check_irrigation()

    def update_weather(self):
        url = f"http://api.openweathermap.org/data/2.5/weather?q={self.city}&appid={self.api_key}&units=metric"
        try:
            response = requests.get(url)
            data = response.json()

            if "rain" in data:
                weather_status = "Rainy"
            elif "snow" in data:
                weather_status = "Snowy"
            else:
                weather_status = "No Rain"

            self.label_weather.setText(f"Weather: {weather_status}")
        except:
            self.label_weather.setText("Weather: Error")

    def update_moisture(self):
        moisture_level = random.randint(10, 100) 
        self.label_moisture.setText(f"Moisture: {moisture_level}%")
        self.moisture_level = moisture_level

    def check_irrigation(self):
        if self.moisture_level < 30 and "Rainy" not in self.label_weather.text():
            self.label_status.setText("Status: Watering Garden")
            self.label_status.setStyleSheet("background-color: rgb(0, 255, 0);")
        else:
            self.label_status.setText("Status: No Need for Watering")
            self.label_status.setStyleSheet("background-color: rgb(255, 0, 0);")

    def manual_override(self):
        if not self.manual_mode:
            self.manual_mode = True
            self.label_status.setText("Status: Manual Watering")
            self.label_status.setStyleSheet("background-color: rgb(255, 165, 0);")
            self.push_button_manual.setText("Auto")
            self.push_button_manual.setStyleSheet("background-color: rgb(0, 85, 255);")
        else:
            self.manual_mode = False
            self.update_data()  
            self.push_button_manual.setText("Manual")
            self.push_button_manual.setStyleSheet("background-color: rgb(0, 170, 0);")


def main():
    app = QApplication(sys.argv)
    window = SmartGarden()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

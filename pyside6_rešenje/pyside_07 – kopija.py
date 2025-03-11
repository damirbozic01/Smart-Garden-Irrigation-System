import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile


class Calculator(QMainWindow):
    def __init__(self):
        super().__init__()

        ui_file = QFile("calculator.ui")
        loader = QUiLoader()
        self.ui = loader.load(ui_file, self)
        ui_file.close()

        self.setCentralWidget(self.ui)

        self.ui.button_zbroji.clicked.connect(self.zbroji)
        self.ui.button_oduzmi.clicked.connect(self.oduzmi)

    def zbroji(self):
        prvi_broj = int(self.ui.line_edit_prvi_broj.text())
        drugi_broj = int(self.ui.line_edit_drugi_broj.text())
        rezultat = prvi_broj + drugi_broj
        self.ui.line_edit_rezultat.setText(str(rezultat))

    def oduzmi(self):
        prvi_broj = int(self.ui.line_edit_prvi_broj.text())
        drugi_broj = int(self.ui.line_edit_drugi_broj.text())
        rezultat = prvi_broj - drugi_broj
        self.ui.line_edit_rezultat.setText(str(rezultat))


def main():
    app = QApplication()
    window = Calculator()
    window.ui.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

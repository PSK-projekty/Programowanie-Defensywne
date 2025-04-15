import sys
from PyQt5.QtWidgets import QApplication
from windows.main_window import MainWindow
from windows.login_window import LoginWindow

def main():
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

import sys
from ui.MainWindow import MainWindow
from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Breeze')
    app.setStyleSheet('''
        QWidget {
            font-size: 35px;
        }
    ''')

    window = MainWindow()
    window.show()

    try:
        sys.exit(app.exec_())
    except SystemExit:
        print('Closing Window...')

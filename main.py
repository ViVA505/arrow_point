import sys
from PyQt5.QtWidgets import QApplication
from app.widget import ArrowWindow


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ArrowWindow()
    window.show()
    sys.exit(app.exec_())

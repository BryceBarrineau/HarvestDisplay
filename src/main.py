import sys
from PyQt6.QtWidgets import QApplication

from ui import MainWindowUI

def main():
    app = QApplication(sys.argv)
    window = MainWindowUI()

    # Logic: connect button to function

    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
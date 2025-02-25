from PyQt6 import QtGui,QtWidgets
import sys
from main_window import MainWindow

app=QtWidgets.QApplication(sys.argv)
app.setWindowIcon(QtGui.QIcon(r"images/mine.png"))
window=MainWindow()
window.show()
sys.exit(app.exec())
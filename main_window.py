from PyQt6 import QtCore,QtGui,QtWidgets,QtPrintSupport
from game_widget import GameWidget
from settings_dialog import SettingsDialog
import re

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self,parent=None):
        QtWidgets.QMainWindow.__init__(self,parent,flags=QtCore.Qt.WindowType.Window | QtCore.Qt.WindowType.MSWindowsFixedSizeDialogHint)
        self.setWindowTitle("Сапер")
        self.setStyleSheet("CellLabel {font-size:18pt;font-family:Verdana;font-weight:bold;border:1px solid #9AA6A7;}")
        self.settings=QtCore.QSettings("FaaZMaaR","Minesweeper")
        if self.settings.value("Rows")==None:
            self.settings.setValue("Rows",10)
        if self.settings.value("Cols")==None:
            self.settings.setValue("Cols",10)
        if self.settings.value("Mines")==None:
            self.settings.setValue("Mines",20)
        self.game=GameWidget(self.settings.value("Rows"),self.settings.value("Cols"),self.settings.value("Mines"))
        self.game.restartButton.clicked.connect(self.newGame)
        self.setCentralWidget(self.game)
        menuBar=self.menuBar()
        menuGame=menuBar.addMenu("&Игра")
        action=menuGame.addAction(QtGui.QIcon(r"images/restart.png"),"Н&овая",QtGui.QKeySequence("Ctrl+N"),self.newGame)
        action.setStatusTip("Новая игра")
        action=menuGame.addAction("&Настройки...",QtGui.QKeySequence("Ctrl+U"),self.openGameSettings)
        action.setStatusTip("Задать размеры игрового поля и количество мин")
        menuGame.addSeparator()
        action=menuGame.addAction("&Выход",QtGui.QKeySequence("Ctrl+Q"),QtWidgets.QApplication.instance().quit)
        action.setStatusTip("Завершение работы программы")
        
        menuAbout=menuBar.addMenu("&Справка")
        action=menuAbout.addAction("О &программе...",self.aboutProgram)
        action.setStatusTip("Получение сведений о программе")
        action=menuAbout.addAction("О &Qt...",self.aboutQt)
        action.setStatusTip("Получение сведений о фреймворке Qt")
        statusBar=self.statusBar()
        statusBar.setSizeGripEnabled(False)
        statusBar.showMessage("\"Сапер\" приветствует Вас",20000)
        if self.settings.contains("X") and self.settings.contains("Y"):
            self.move(self.settings.value("X"),self.settings.value("Y"))
        
    def closeEvent(self,evt):
        g=self.geometry()
        self.settings.setValue("X",g.left())
        self.settings.setValue("Y",g.top())
        
    def newGame(self):
        self.game=GameWidget(self.settings.value("Rows"),self.settings.value("Cols"),self.settings.value("Mines"))
        self.setCentralWidget(self.game)
        self.game.restartButton.clicked.connect(self.newGame)
        
    def aboutProgram(self):
        QtWidgets.QMessageBox.about(self,"О программе","<center>\"Сапер\" v1.0.0<br><br>Компьютерная игра-головоломка, в которой необходимо найти все мины на игровом поле, используя числовые подсказки.<br><br>(c) FaaZMaaR, 2025")
        
    def aboutQt(self):
        QtWidgets.QMessageBox.aboutQt(self,title="О фреймворке Qt")
    
    def openGameSettings(self):
        dialog=SettingsDialog(self.settings.value("Rows"),self.settings.value("Cols"),self.settings.value("Mines"),self)
        result=dialog.exec()
        if result==QtWidgets.QDialog.DialogCode.Accepted:
            self.settings.setValue("Rows",dialog.spinRows.value())
            self.settings.setValue("Cols",dialog.spinCols.value())
            self.settings.setValue("Mines",dialog.spinMines.value())
            self.newGame()
            self.adjustSize()
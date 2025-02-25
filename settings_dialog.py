from PyQt6 import QtWidgets

class SettingsDialog(QtWidgets.QDialog):
    def __init__(self,rows,cols,mines,parent=None):
        QtWidgets.QDialog.__init__(self,parent)
        self.setWindowTitle("Настройки")
        self.resize(200,70)
        
        self.mainBox = QtWidgets.QVBoxLayout()
        
        self.labelRows = QtWidgets.QLabel("Количество строк")
        self.mainBox.addWidget(self.labelRows)
        self.spinRows=QtWidgets.QSpinBox()
        self.spinRows.setRange(10,20)
        self.spinRows.setValue(rows)
        self.spinRows.valueChanged[int].connect(self.onSpinsChanged)
        self.mainBox.addWidget(self.spinRows)
        
        self.labelCols=QtWidgets.QLabel("Количество столбцов")
        self.mainBox.addWidget(self.labelCols)
        self.spinCols=QtWidgets.QSpinBox()
        self.spinCols.setRange(10,40)
        self.spinCols.setValue(cols)
        self.spinCols.valueChanged[int].connect(self.onSpinsChanged)
        self.mainBox.addWidget(self.spinCols)
        
        self.labelMines=QtWidgets.QLabel("Количество мин")
        self.mainBox.addWidget(self.labelMines)
        self.spinMines=QtWidgets.QSpinBox()
        self.spinMines.setRange(1,self.getHalfMines())
        self.spinMines.setValue(mines)
        self.mainBox.addWidget(self.spinMines)
        
        self.hbox=QtWidgets.QHBoxLayout()
        self.btnOK=QtWidgets.QPushButton("&Принять")
        self.btnCancel=QtWidgets.QPushButton("&Отмена")
        self.btnCancel.setDefault(True)
        self.btnOK.clicked.connect(self.accept)
        self.btnCancel.clicked.connect(self.reject)
        self.hbox.addWidget(self.btnOK)
        self.hbox.addWidget(self.btnCancel)
        self.mainBox.addLayout(self.hbox)
        
        self.setLayout(self.mainBox)
        
    def getHalfMines(self):
        return self.spinRows.value()*self.spinCols.value()//2
    
    def onSpinsChanged(self,val):
        self.spinMines.setMaximum(self.getHalfMines())
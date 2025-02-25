from PyQt6 import QtCore,QtWidgets,QtGui

class CellLabel(QtWidgets.QLabel):
    colorRed="#FF0000"
    colorLime="#00FF00"
    colorBlue="#0000FF"
    colorCyan="#00FFFF"
    colorMagenta="#FF00FF"
    colorMaroon="#800000"
    colorPurple="#800080"
    colorNavy="#000080"
    colorGreen="#008000"
    colorWhiteSmoke="#F5F5F5"
    colorSlateGray="#708090"
    colorBlack="#000000"
    
    #icoMine=QtGui.QIcon(r"images/mine.png")
    #icoFlag=QtGui.QIcon(r"images/flag.png")
    
    cellSelected=QtCore.pyqtSignal(int,int,bool)
    
    def __init__(self,row,col,parent=None):
        QtWidgets.QLabel.__init__(self,parent)
        self.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.setFixedSize(30,30)
        self.setMargin(0)
        self.setText("")
        self.setScaledContents(True)
        self.row=row
        self.col=col
        self.isOpen=False
        self.isMine=False
        self.isMarked=False
        self.minesAround=0
        self.setColor()
        
    def mousePressEvent(self,evt):
        if evt.buttons() & QtCore.Qt.MouseButton.RightButton:
            button=True
        else:
            button=False
        self.cellSelected.emit(self.row,self.col,button)
        QtWidgets.QLabel.mousePressEvent(self,evt)
    
    def setColor(self):
        if not self.isOpen:
            self.bgColor=self.colorSlateGray
            if self.isMarked:
                self.setPixmap(QtGui.QPixmap(r"images/flag.png"))
            else:
                self.setPixmap(QtGui.QPixmap())
        else:
            if self.isMine:
                self.bgColor=self.colorRed
                self.setPixmap(QtGui.QPixmap(r"images/mine.png"))
            else:
                self.bgColor=self.colorWhiteSmoke
                if self.minesAround==0:
                    self.setText("")
                else:
                    self.setText(str(self.minesAround))
        self.fontColor=self.setFontColor()         
        self.setStyleSheet("background-color:"+self.bgColor+";color:"+self.fontColor+";")
        
    def setFontColor(self):
        match self.minesAround:
            case 1:
                return self.colorBlue
            case 2:
                return self.colorLime
            case 3:
                return self.colorMaroon
            case 4:
                return self.colorCyan
            case 5:
                return self.colorNavy
            case 6:
                return self.colorMagenta
            case 7:
                return self.colorGreen
            case 8:
                return self.colorPurple
            case _:
                return self.colorBlack
            
    def mark(self):
        self.isMarked=False if self.isMarked else True
        self.setColor()
        return -1 if self.isMarked else 1
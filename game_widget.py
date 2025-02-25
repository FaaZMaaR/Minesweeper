from PyQt6 import QtCore,QtGui,QtWidgets
from cell_label import CellLabel
from timer import Timer
import enum
import random

class GameStates(enum.Enum):    
    BEGIN=1
    GAME=2
    END=3

class GameWidget(QtWidgets.QWidget):
    def __init__(self,rows,cols,mines,parent=None):
        QtWidgets.QWidget.__init__(self,parent)
        self.rows=rows
        self.cols=cols
        self.mines=mines
        self.state=GameStates.BEGIN
        self.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)
        vBoxMain=QtWidgets.QVBoxLayout()
        frame1=QtWidgets.QFrame()
        frame1.setStyleSheet("background-color: #3414A4;border: 1px solid #3414A4;")
        grid=QtWidgets.QGridLayout()
        grid.setSpacing(0)
        self.cells=[[CellLabel(i,j) for j in range(self.cols)] for i in range(self.rows)]
        for i in range(self.rows):
            for j in range(self.cols):
                grid.addWidget(self.cells[i][j],i,j)
        for row in self.cells:
            for cell in row:
                cell.cellSelected.connect(self.onCellSelected)
        frame1.setLayout(grid)
        vBoxMain.addWidget(frame1,alignment=QtCore.Qt.AlignmentFlag.AlignHCenter)
        frame2=QtWidgets.QFrame()
        frame2.setFixedSize(300,80)
        hbox=QtWidgets.QHBoxLayout()
        hbox.setSpacing(20)
        self.markedLCD=QtWidgets.QLCDNumber(3)
        self.markedLCD.setStyleSheet("background-color: #101010;color: #FF0000;")
        self.markedLCD.setSegmentStyle(QtWidgets.QLCDNumber.SegmentStyle.Flat)
        self.markedLCD.display(self.mines)
        hbox.addWidget(self.markedLCD)
        self.restartButton=QtWidgets.QPushButton()
        self.restartButton.setIcon(QtGui.QIcon(r"images/restart.png"))
        self.restartButton.setIconSize(QtCore.QSize(50,50))
        hbox.addWidget(self.restartButton)
        self.timeLCD=QtWidgets.QLCDNumber(3)
        self.timeLCD.setStyleSheet("background-color: #101010;color: #FF0000;")
        self.timeLCD.setSegmentStyle(QtWidgets.QLCDNumber.SegmentStyle.Flat)
        self.timeLCD.display(0)
        hbox.addWidget(self.timeLCD)
        frame2.setLayout(hbox)
        vBoxMain.addWidget(frame2,alignment=QtCore.Qt.AlignmentFlag.AlignHCenter)
        
        self.setLayout(vBoxMain)
        
    def onCellSelected(self,row,col,button):
        if button:            
            self.markedLCD.display(self.markedLCD.intValue()+self.cells[row][col].mark())
        else:
            if self.cells[row][col].isMarked:
                return
            else:
                match self.state:
                    case GameStates.BEGIN:
                        self.timer=Timer()
                        self.timer.signal.connect(self.onTimer)
                        self.timer.start()
                        self.placeMines(row,col)
                        self.openCell(row,col)                        
                        self.state=GameStates.GAME
                    case GameStates.GAME:
                        self.openCell(row,col)
                    case _:
                        return
        
    def placeMines(self,row,col):
        mines=[True if i<self.mines else False for i in range(self.rows*self.cols)]
        random.shuffle(mines)
        currentCell=self.cols*row+col
        if mines[currentCell]:
            mines[currentCell]=False
            for i in range(len(mines)):
                if i!=currentCell:
                    if not mines[i]:
                        mines[i]=True
                        break
        i=0
        for cellsrow in self.cells:
            for cell in cellsrow:
                cell.isMine=mines[i]
                i+=1
    
    def openCell(self,row,col):
        if self.cells[row][col].isOpen:
            return
        self.cells[row][col].isOpen=True
        if not self.cells[row][col].isMine:
            self.countMines(row,col)
        else:
            self.openMines()
            self.state=GameStates.END
            self.timer.terminate()
            return
        self.cells[row][col].setColor()
        if self.cells[row][col].minesAround==0 and not self.cells[row][col].isMine:
            for i in range(-1,2):
                for j in range(-1,2):
                    if (row+i>=0 and row+i<self.rows) and (col+j>=0 and col+j<self.cols):
                        self.openCell(row+i,col+j)
        if self.checkAllOpened():
            self.state=GameStates.END
            self.timer.terminate()
    
    def openMines(self):
        for cellrow in self.cells:
            for cell in cellrow:
                if cell.isMine:
                    cell.isOpen=True
                    cell.setColor()
            
    def countMines(self,row,col):
        mines=0
        for i in range(-1,2):
            for j in range(-1,2):
                if (row+i>=0 and row+i<self.rows) and (col+j>=0 and col+j<self.cols) and self.cells[row+i][col+j].isMine:
                    mines+=1
        self.cells[row][col].minesAround=mines
        
    def onTimer(self,time):
        self.timeLCD.display(time)
        
    def checkAllOpened(self):
        for cellrow in self.cells:
            for cell in cellrow:
                if not cell.isOpen and not cell.isMine:
                    return False
        return True
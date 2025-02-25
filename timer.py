from PyQt6 import QtCore

class Timer(QtCore.QThread):
    signal=QtCore.pyqtSignal(int)
    
    def __init__(self,parent=None,graphArray=None,speed=1):
        QtCore.QThread.__init__(self,parent)
        self.time=0
        
    def run(self):
        while True:
            self.signal.emit(self.time)
            self.time+=1
            self.sleep(1)
            
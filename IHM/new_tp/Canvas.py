from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class Canvas(QWidget):

    def __init__(self, parent = None):
        QWidget.__init__(self, parent )
        self.setMinimumSize(100,100)
        self.pressed = False
        self.shape=0
        self.brushColor = Qt.black
        self.penColor = Qt.red
        print("class Canvas")

    def setShape(self,shape):
        self.shape=shape
        
    def setPenColor(self,color):
        self.penColor=color
    
    def setBrushColor(self,color):
        self.brushColor=color

    def reset(self):
        print("reset")

    def add_object(self):
        print("add object")

    def set_color(self, color ):
        print("set color")
        
    def paintEvent(self, event):
        if self.pressed:
            painter = QPainter(self)
            painter.setPen(self.penColor)
            painter.setBrush(self.brushColor)
            if self.shape==0:
                painter.drawRect(self.pStart.x(),self.pStart.y(),self.mousecurrent.x()-self.pStart.x(),self.mousecurrent.y()-self.pStart.y())
            if self.shape==1:
                painter.drawEllipse(self.pStart.x(),self.pStart.y(),self.mousecurrent.x()-self.pStart.x(),self.mousecurrent.y()-self.pStart.y())
            if self.shape==2:
                painter.drawLine(self.pStart.x(),self.pStart.y(),self.mousecurrent.x()-self.pStart.x(),self.mousecurrent.y()-self.pStart.y())
        
    def mousePressEvent(self, event):
        self.pressed = True
        self.pStart = event.pos()
        self.mousecurrent = event.pos()
        print("press: ", self.pStart)
        self.update()
    
    def mouseReleaseEvent(self, event):
        self.pressed = False
        self.mousecurrent = event.pos()
        print("release: ", event.pos())
        self.update()
        
    def mouseMoveEvent(self, event):
        self.mousecurrent = event.pos()
        self.update()
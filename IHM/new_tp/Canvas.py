from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class Canvas(QWidget):

    def __init__(self, parent = None):
        QWidget.__init__(self, parent )
        self.setMinimumSize(200,200)
        self.pressed = False
        self.shape=0
        self.shapeList=[]
        self.brushColor = Qt.black
        self.penColor = Qt.red
        self.mode = "draw"
        self.offset = QPoint(0, 0)
        self.OldOffset = QPoint(0, 0)
        print("class Canvas")

    def selectMode(self,m):
        self.mode = m

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
        
    def drawShapes(self,painter,shape,penColor,brushColor,start,end):
        painter.setPen(penColor)
        painter.setBrush(brushColor)
        if shape==0:
            painter.drawRect(start.x(),start.y(),end.x()-start.x(),end.y()-start.y())
        if shape==1:
            painter.drawEllipse(start.x(),start.y(),end.x()-start.x(),end.y()-start.y())
        if shape==2:
            painter.drawLine(start.x(),start.y(),end.x()-start.x(),end.y()-start.y())
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.translate(self.offset+self.OldOffset)
        if self.pressed:
            for s,p,b,sp,ep in self.shapeList:
                self.drawShapes(painter,s,p,b,sp,ep)
            if self.mode == "draw": 
                self.drawShapes(painter,self.shape,self.penColor,self.brushColor,self.pStart,self.mousecurrent)
        else:
            for s,p,b,sp,ep in self.shapeList:
                self.drawShapes(painter,s,p,b,sp,ep)
        
    def addShape(self):
        self.shapeList.append((self.shape,self.penColor,self.brushColor,self.pStart,self.mousecurrent))
        
    def mousePressEvent(self, event):
        self.pressed = True
        self.pStart = event.pos()-self.OldOffset
        self.mousecurrent = event.pos()-self.OldOffset
        if self.mode == "move":
            self.offset = self.mousecurrent-self.pStart 
        print("press: ", self.pStart)
        self.update()
    
    def mouseReleaseEvent(self, event):
        self.pressed = False
        self.mousecurrent = event.pos()-self.OldOffset
        print("release: ", event.pos())
        self.OldOffset += self.offset
        self.offset = QPoint(0, 0)
        if self.mode == "draw":
            self.addShape()
        self.update()
        
    def mouseMoveEvent(self, event):
        self.mousecurrent = event.pos()-self.OldOffset
        if self.mode == "move":
            self.offset = self.mousecurrent-self.pStart 
        self.update()
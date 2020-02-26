from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtChart import *


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
        self.lastPoint = QPoint(0, 0)
        self.selected = []
        self.lasso = QPolygon()
        print("class Canvas")

    def selectMode(self,m):
        self.mode = m
        self.selected = []
        self.update() 

    def setShape(self,shape):
        self.shape=shape
        
    def setPenColor(self,color):
        self.penColor=color
        if self.mode == "select" :
                self.modifyShape()
        self.update() 
                
    def setBrushColor(self,color):
        self.brushColor=color
        if self.mode == "select" :
            self.modifyShape()
        self.update() 

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
            painter.drawLine(start.x(),start.y(),end.x(),end.y())
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.translate(self.offset+self.OldOffset)
        if self.pressed:
            for s,p,b,sp,ep in self.shapeList:
                self.drawShapes(painter,s,p,b,sp,ep)
            if self.mode == "draw" and self.shape != 2: 
                self.drawShapes(painter,self.shape,self.penColor,self.brushColor,self.pStart,self.mousecurrent)
            if self.mode == "select" :
                painter.setPen(self.penColor)
                painter.setBrush(QColor("transparent"))  
                painter.drawPolygon(self.lasso)
        else:
            for s,p,b,sp,ep in self.shapeList :
                self.drawShapes(painter,s,p,b,sp,ep)
            if self.mode == "select" :
                if len(self.selected) != 0 :
                    for i in self.selected:
                        shape = self.shapeList[i]
                        self.drawShapes(painter, shape[0], QColor(0,0,255), QColor(255,255,255), shape[3], shape[4])
        
    def addShape(self):
        self.shapeList.append([self.shape,self.penColor,self.brushColor,self.pStart,self.mousecurrent])
            
    def addLine(self):
        self.shapeList.append((self.shape,self.penColor,self.brushColor,self.lastPoint,self.mousecurrent))
        
    def selectShapeLasso(self):
        for i in range(len(self.shapeList)):
            start = self.shapeList[i][3]
            end = self.shapeList[i][4]
            center = QPoint(end.x()-start.x()/2,end.y()-start.y()/2)
            if self.lasso.containsPoint(center,Qt.OddEvenFill) :
                self.selected.append(i)
                
    def selectShape(self):
        for i in range(len(self.shapeList)):
            start = self.shapeList[i][3]
            end = self.shapeList[i][4]
            r = QRect(start.x(),start.y(),end.x()-start.x(),end.y()-start.y())
            if r.contains(self.mousecurrent) :
                print(self.OldOffset)
                self.selected.append(i)
                
    def modifyShape(self) :
        for i in self.selected:
            self.shapeList[i][1] = self.penColor
            self.shapeList[i][2] = self.brushColor
            
    def createChartShape(self):
        chart =QChart() # Modèle
        chart.setTitle("Shapes")
        pie = QPieSeries()
        count = [0,0,0]
        for s in self.shapeList:
            count[s[0]] += 1
        s0 = QPieSlice("rect",count[0])
        s1 = QPieSlice("ellipse",count[1])
        s2 = QPieSlice("freeDrawing",count[2])
        pie.append(s0)
        pie.append(s1)
        pie.append(s2)
        chart.addSeries(pie)
        return chart
                
        
    def mousePressEvent(self, event):
        self.selected = []
        self.pressed = True
        self.lasso = QPolygon()
        self.pStart = event.pos()-self.OldOffset
        self.mousecurrent = event.pos()-self.OldOffset
        self.lastPoint = self.mousecurrent
        if self.mode == "move":
            self.offset = self.mousecurrent-self.pStart
        elif self.mode == "select" :
            self.selectShape()
        print("press: ", self.pStart)
        self.update()
    
    def mouseReleaseEvent(self, event):
        self.pressed = False
        self.mousecurrent = event.pos()-self.OldOffset
        print("release: ", event.pos())
        self.OldOffset += self.offset
        self.offset = QPoint(0, 0)
        if self.mode == "draw" and self.shape != 2:
            self.addShape()
        elif self.mode == "select" :
            self.selectShapeLasso()
        self.update()
        
    def mouseMoveEvent(self, event):
        self.lastPoint = self.mousecurrent
        self.mousecurrent = event.pos()-self.OldOffset
        if self.mode == "draw" and self.shape == 2:
            self.addLine()
        elif self.mode == "move":
            self.offset = self.mousecurrent-self.pStart 
        elif self.mode == "select" :
            self.lasso << self.mousecurrent
        self.update()
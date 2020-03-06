from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtChart import *


class Canvas(QWidget):

    def __init__(self, parent = None):
        QWidget.__init__(self, parent )
        self.setMinimumSize(500,200)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.white)
        self.setAutoFillBackground(True)
        self.setPalette(p)

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
        self.freePen = QPolygon()
        self.intersectPoint = QPoint(0,0)

        # STATS

        self.shapeCount = [0,0,0]
        self.penColorCount = dict()
        self.brushColorCount = dict()

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

    def setChartWidget(self,charts):
        self.charts = charts

    def updateShapeChart(self,s):
        self.shapeCount[s] += 1
        self.charts.updateShapeChart(self.shapeCount)

    def updateColorChart(self,p,b):
        print(p)

        """self.penColorCount[p] += 1
        self.brushColorCount[b] += 1
        self.charts.updateColorChart(self.penColorCount,self.brushColorCount)"""

    def reset(self):
        print("reset")

    def add_object(self):
        print("add object")

    def set_color(self, color ):
        print("set color")
        
    def drawShapes(self,painter,shape,penColor,brushColor,start,end,freePen):
        painter.setPen(penColor)
        painter.setBrush(brushColor)
        if shape==0:
            painter.drawRect(start.x(),start.y(),end.x()-start.x(),end.y()-start.y())
        if shape==1:
            painter.drawEllipse(start.x(),start.y(),end.x()-start.x(),end.y()-start.y())
        if shape==2:
            painter.drawPolygon(freePen)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.translate(self.offset+self.OldOffset)
        if self.pressed:
            for s,p,b,sp,ep,fp in self.shapeList:
                self.drawShapes(painter,s,p,b,sp,ep,fp)
            if self.mode == "draw":
                self.drawShapes(painter,self.shape,self.penColor,self.brushColor,self.pStart,self.mousecurrent,self.freePen)
            if self.mode == "select" :
                painter.setPen(self.penColor)
                painter.setBrush(QColor("transparent"))  
                painter.drawPolygon(self.lasso)
        else:
            for s,p,b,sp,ep,fp in self.shapeList :
                self.drawShapes(painter,s,p,b,sp,ep,fp)
            if self.mode == "select" :
                if len(self.selected) != 0 :
                    for i in self.selected:
                        shape = self.shapeList[i]
                        self.drawShapes(painter, shape[0], QColor(0,0,255), QColor(255,255,255), shape[3], shape[4],shape[5])
        
    def addShape(self):
        if self.shape !=2:
            self.shapeList.append([self.shape,self.penColor,self.brushColor,self.pStart,self.mousecurrent,None])
        else:
            self.shapeList.append([self.shape, self.penColor, self.brushColor,self.pStart,self.mousecurrent,QPolygon(self.freePen)])
        self.updateShapeChart(self.shape)
        self.updateColorChart(self.penColor,self.brushColor);
            
    def addLine(self):
        self.shapeList.append((self.shape,self.penColor,self.brushColor,self.lastPoint,self.mousecurrent))
        
    def selectShapeLasso(self):
        for i in range(len(self.shapeList)):
            start = self.shapeList[i][3]
            end = self.shapeList[i][4]
            center = QPoint(end.x()-start.x()/2,end.y()-start.y()/2)
            if self.lasso.containsPoint(center,Qt.OddEvenFill) :
                self.selected.append(i)
            if self.shapeList[i][0]==2:
                if not self.lasso.intersected(self.shapeList[i][5]).isEmpty():
                    self.selected.append(i)
                
    def selectShape(self):
        for i in range(len(self.shapeList)):
            start = self.shapeList[i][3]
            end = self.shapeList[i][4]
            r = QRect(start.x(),start.y(),end.x()-start.x(),end.y()-start.y())
            if r.contains(self.mousecurrent) :
                print(self.OldOffset)
                self.selected.append(i)
            if self.shapeList[i][0]==2:
                if self.shapeList[i][5].containsPoint(self.mousecurrent,Qt.OddEvenFill):
                    self.selected.append(i)
                
    def modifyShape(self) :
        for i in self.selected:
            self.shapeList[i][1] = self.penColor
            self.shapeList[i][2] = self.brushColor

    def scriboliDetect(self):
        point = QPointF(0, 0)
        l1 = QLineF(self.lasso[len(self.lasso) - 2], self.lasso[len(self.lasso) - 1])
        for j in range(max(0, len(self.lasso) - 100), len(self.lasso) - 20):
            l2 = QLineF(self.lasso[j], self.lasso[j + 1])

            if l1.intersect(l2, point) == 1:
                self.intersectPoint = point
                print("intersection detected : " + str(self.intersectPoint) + " ")

    def scriboliDo(self):
        end = self.lasso[-1]
        copy = self.shapeList.copy()
        if end.y() > self.intersectPoint.y():
            for i in self.selected:
                if copy[i] in self.shapeList:
                    self.shapeList.remove(copy[i])
                    print("scriboli supprime")
        self.selected = []

    def mousePressEvent(self, event):
        self.selected = []
        self.pressed = True
        self.lasso = QPolygon()
        self.freePen = QPolygon()
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
        if self.mode == "draw":
            self.addShape()
        elif self.mode == "select" :
            self.selectShapeLasso()
            if self.intersectPoint != QPoint(0,0) and len(self.lasso) > 0:
                self.scriboliDo()
        self.update()
        
    def mouseMoveEvent(self, event):
        self.lastPoint = self.mousecurrent
        self.mousecurrent = event.pos()-self.OldOffset
        if self.mode == "draw" and self.shape == 2:
            self.freePen << self.mousecurrent
        elif self.mode == "move":
            self.offset = self.mousecurrent-self.pStart 
        elif self.mode == "select" :
            self.lasso << self.mousecurrent
            if len(self.lasso) > 0:
                self.scriboliDetect()
        self.update()
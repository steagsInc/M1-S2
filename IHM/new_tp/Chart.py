from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtChart import *


class Chart(QWidget):

    def __init__(self, parent = None):
        QWidget.__init__(self, parent )
        self.setMinimumSize(100,500)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.createShapeChart())
        self.layout.addWidget(self.createButtonChart())
        self.setLayout(self.layout)
        
    def setChart(self,chart):
        print("class Chart")

    def createShapeChart(self):
        chart =QChart() # Modèle
        chart.setTitle("Shapes")
        bar = QPercentBarSeries()
        s0 = QBarSet("rect")<<0
        s1 = QBarSet("ellipse")<<0
        s2 = QBarSet("freeDrawing")<<0
        bar.append(s0)
        bar.append(s1)
        bar.append(s2)
        chart.addSeries(bar)
        self.shapeChart = [bar,s0,s1,s2]

        return QChartView(chart)

    def createButtonChart(self):
        chart =QChart() # Modèle
        chart.setTitle("Button")
        bar = QBarSeries()
        s0 = QBarSet("")<<0<<0<<0<<0<<0<<0<<0<<0
        bar.append(s0)
        chart.addSeries(bar)
        axisY = QValueAxis()
        axisY.setMax(20)
        chart.addAxis(axisY,Qt.AlignLeft)
        categories = QBarCategoryAxis()
        categories.append("pen")
        categories.append("brush")
        categories.append("rectangle")
        categories.append("ellipse")
        categories.append("free")
        categories.append("move")
        categories.append("draw")
        categories.append("select")
        chart.addAxis(categories,Qt.AlignBottom)
        bar.attachAxis(categories)
        bar.attachAxis(axisY)
        self.buttonChart = [bar, s0]
        return QChartView(chart)


    def updateShapeChart(self,c):
        self.shapeChart[1].replace(0,c[0])
        self.shapeChart[2].replace(0,c[1])
        self.shapeChart[3].replace(0,c[2])
        self.update()

    def updateButtonChart(self,c):
        self.buttonChart[1].replace(0, c[0])
        self.buttonChart[1].replace(1, c[1])
        self.buttonChart[1].replace(2, c[2])
        self.buttonChart[1].replace(3, c[3])
        self.buttonChart[1].replace(4, c[4])
        self.buttonChart[1].replace(5, c[5])
        self.buttonChart[1].replace(6, c[6])
        self.buttonChart[1].replace(7, c[7])
        self.update()
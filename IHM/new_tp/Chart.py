from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtChart import *


class Chart(QWidget):

    def __init__(self, parent = None):
        QWidget.__init__(self, parent )
        self.setMinimumSize(200,500)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.createShapeChart())
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

    def createColorChart(self):
        chart =QChart() # Modèle
        chart.setTitle("Colors")


    def updateShapeChart(self,c):
        self.shapeChart[1].replace(0,c[0])
        self.shapeChart[2].replace(0,c[1])
        self.shapeChart[3].replace(0,c[2])
        self.update()

    def updateColorChart(self,p,b):
        print(p)
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtChart import *


class Chart(QMainWindow):

    def __init__(self, parent = None):
        QWidget.__init__(self, parent )
        self.setMinimumSize(500,500)
        
    def setChart(self,chart):
        view =QChartView(chart)
        self.setCentralWidget(view)
        print("class Chart")
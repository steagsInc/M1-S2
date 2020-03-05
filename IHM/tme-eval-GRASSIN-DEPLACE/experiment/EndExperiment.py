from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
#import pandas as pd
#from PyQt5.QtChart import QChart, QChartView, QBarSeries, QBarSet, QValueAxis, QBarCategoryAxis


class EndExperiment(QWidget):
	def __init__(self, parent = None):
		QWidget.__init__(self, parent )
 
		#self.setFocusPolicy(Qt.StrongFocus)
		layout = QVBoxLayout(self)
		thanks_lab = QLabel()
		thanks_lab.setText("Fin de l'experience. Merci pour votre participation")		
		layout.addWidget(thanks_lab)


		#######################
		# read csv file
		#######################
		#read your csv file and add the header
		#df = pd.read_csv('./logs/participant_0.csv', names = [ "", "", ])
		#print(df)
		#
		#data = df.groupby(["condition", "size"], as_index=False )['duration'].mean()
		#print(data)


		##################
		# Qt Charts
		##################
		#self.summary_chart = QChart()
		#self.summary_chart_view = QChartView( self.summary_chart )
		#self.summary_chart_view.setRenderHint(QPainter.Antialiasing)
		#layout.addWidget( self.summary_chart_view )



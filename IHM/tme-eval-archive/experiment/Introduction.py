from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class Introduction(QWidget):

	def __init__(self, parent = None):
		QWidget.__init__(self, parent )
		self.participant_id = 0
		
		layout = QVBoxLayout(self)

		instructions_lab = QLabel()
		instructions_lab.setText("Merci pour votre participation a cette experience qui va durer 5 minutes. \n Indiquez votre identifiant participant et appuyez sur sur boutton pour commencer.")
		participant_list = QComboBox()
		for i in range(0,20):
			participant_list.addItem( str(i) )
		participant_list.activated.connect(self.set_participant_id)
		participant_lab = QLabel("Select your participant Id: ")
		hlayout = QHBoxLayout()
		hlayout.addWidget(participant_lab)
		hlayout.addWidget(participant_list)
		layout. addLayout(hlayout)
		
		layout.addWidget(instructions_lab)
		
		self.start_button = QPushButton("\n Start the Experiment \n ")
		layout.addWidget(self.start_button)


	###################################
	def set_participant_id(self, id):
		self.participant_id = id



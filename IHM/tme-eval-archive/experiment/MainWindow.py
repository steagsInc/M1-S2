import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from Introduction import *
from InterTrial import *
from Canvas import *
from EndExperiment import *
import numpy as np
import time

class MainWindow(QMainWindow):

    def __init__(self, parent = None ):
        QMainWindow.__init__(self, parent )
        self.resize(600, 500)
        self.index = 0
        self.participant_id =-1

        self.introduction = Introduction()
        self.introduction.start_button.clicked.connect(self.start_experiment)

        self.canvas = Canvas(self)
        self.canvas.stopTrial.connect(self.stop_trial)
        
        self.interTrial = InterTrial(self)
        self.interTrial.startTrial.connect(self.start_trial)

        self.endExperiment = EndExperiment(self)
        
        self.stack = QStackedWidget()
        self.stack.addWidget(self.introduction)
        self.stack.addWidget(self.interTrial)
        self.stack.addWidget(self.canvas)
        self.stack.addWidget(self.endExperiment)
         
        self.time = 0
        
        self.setCentralWidget(self.stack)
        
        self.load_experiment_plan()
        self.content = "ID,Trial,Type,Number,Result,Time\n"
        

    def start_experiment(self):
        self.participant_id = self.introduction.participant_id
        print("start epxeriment with participant", self.participant_id)
        found = False
        while not found:
            self.index = self.index+1
            found = self.update_trial_values()
        self.setup_trial()
        
            
    def update_trial_values(self):
            same_participant = True
            if self.index >= len(self.plan):     #end of the file
                return False
            trial_str = self.plan[self.index]
            trial_str = trial_str.replace('\r\n', '')
            trial = trial_str.split(',')
            id = int( trial[0])
            
            if id == self.participant_id:
                self.practice = True if trial[1] == 'true' else False
                self.block_id = trial[2]
                self.trial_id = trial[3]
                self.condition = trial[4]
                self.mat_size = int( trial[5] )
                same_participant = True
            else:
                same_participant = False
            return same_participant           


    def setup_trial(self):
        list = self.generate_stimulus()
        self.canvas.set_stimulus(list)
        self.canvas.setState(0)
        self.interTrial.set_block_trial(self.block_id, self.trial_id)
        self.interTrial.set_practice(self.practice)
        self.stack.setCurrentWidget(self.interTrial)


    def generate_stimulus(self):
        n = self.mat_size
        list = []
        print(self.condition)
        if self.condition == 'size': # TODO
            cond = ['Big','Small']
            distractor =  np.random.choice(cond, 1, p=[0.5,0.5])
            distractor = distractor[0]
            target = cond[1] if distractor == cond[0] else cond[0]
            self.pos_target = np.random.randint(n)
            for i in range(0,n):
                list.append(distractor)
            list[self.pos_target] = target

        elif self.condition == 'curvature': # TODO
            cond = ['Concavity_Big','Convexity_Big']
            distractor =  np.random.choice(cond, 1, p=[0.5,0.5])
            distractor = distractor[0]
            target = cond[1] if distractor == cond[0] else cond[0]
            self.pos_target = np.random.randint(n)
            for i in range(0,n):
                list.append(distractor)
            list[self.pos_target] = target

        elif self.condition == 'curvature & size': # TODO
            cond = ['Concavity_Big', 'Concavity_Small', 'Convexity_Big', 'Convexity_Small']
            target =  np.random.choice(cond, 1, p=[0.25,0.25, 0.25, 0.25])
            target = target[0]
            self.pos_target = np.random.randint(n)
            cond.remove(target)
            for i in range(0,n):
                distractor = np.random.choice(cond, 1, p=[0.333,0.333, 0.334])
                list.append(distractor[0])
            list[self.pos_target] = target
        return list

                 



    def start_trial(self):
        self.stack.setCurrentWidget(self.canvas)
        #print("start_trial -> target: ", self.pos_target)

        self.time = time.time()
        
        
    def stop_trial(self):
        selected_target = self.canvas.selected_target
        print("target vs. selected target: "+ str(self.pos_target) +  " vs. " + str(selected_target) )

        self.content += str(self.participant_id)+","+str(self.index)+","+self.condition+","+str(self.mat_size)+","+str(self.pos_target==selected_target)+","+str(-self.time)+"\n"


        self.index = self.index + 1
        if self.update_trial_values():
            self.setup_trial()
        else:
            print("End of the experiment. Thanks")
            self.stack.setCurrentWidget(self.endExperiment)
            
            ####################
            # TODO
            ####################
            title = "participant_" + str(self.participant_id)
            self.save_user_data(title, self.content)

        

    ####################
    def keyReleaseEvent(self, e):
        if e.key() == Qt.Key_Space:
            self.time -= time.time()
            if self.interTrial.isVisible():
                self.start_trial()
            elif self.canvas.isVisible():
                self.canvas.setState(1)
    

    ##############
    def load_experiment_plan(self):
        file = open('./experiment.csv', 'r') # TODO
        self.plan = file.readlines()
        file.close()

    ##############
    def save_user_data(self, title, content):
        with open('./logs/'+title + '.csv', 'w') as fileSave:
            fileSave.write(content)
            fileSave.close()

if __name__=="__main__":
   
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()
    app.exec_()

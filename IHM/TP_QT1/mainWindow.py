import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class MainWindow(QMainWindow):
    
    #############
    def __init__(self):
        QMainWindow.__init__(self)
        self.CreateActs()
        self.CreatefileMenu()
        self.Createtoolbar()
        self.statusBar()
        self.CreateCentralWidget("")
        print("constructeur de la class MainWindow")
        
        
    def CreateActs(self):
        self.newact = QAction(QIcon("new.png"), "Nouveau...", self)
        self.openact = QAction(QIcon("open.png"), "Ouvrir...", self)
        self.saveact = QAction(QIcon("save.png"), "Sauvegarder", self)
        self.closeact = QAction(QIcon("quit.png"), "Quitter", self)
        
        self.newact.setShortcut(QKeySequence("Ctrl+N"))
        self.openact.setShortcut(QKeySequence("Ctrl+O"))
        self.saveact.setShortcut(QKeySequence("Ctrl+S"))
        self.closeact.setShortcut(QKeySequence("Ctrl+Q"))
        
        self.newact.setStatusTip("Nouveau fichier")
        self.openact.setStatusTip("Ouvrir un fichier")
        self.saveact.setStatusTip("Sauvegarder le fichier")
        self.closeact.setStatusTip("Quitter")
        
        self.openact.triggered.connect(self.open)
        self.saveact.triggered.connect(self.save)
        self.closeact.triggered.connect(self.quit)

    def CreatefileMenu(self):
        bar = self.menuBar()
        fileMenu = bar.addMenu("Fichier")
        fileMenu.addAction(self.newact)
        fileMenu.addAction(self.openact)
        fileMenu.addAction(self.saveact)
        fileMenu.addAction(self.closeact)
    
    def Createtoolbar(self) :
        
        toolbar = self.addToolBar("Fichier")
        toolbar.addAction(self.newact)
        toolbar.addAction(self.openact)
        toolbar.addAction(self.saveact)
        toolbar.addAction(self.closeact)
    
    def CreateCentralWidget(self,text) :
        self.textedit = QTextEdit()
        self.setCentralWidget(self.textedit)
        
    def closeEvent(self, event):
        msg = QMessageBox()
        msg.setText("Voulez-vous quitter ?")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        if msg.exec() == QMessageBox.Ok : 
            event.accept()
        else:
            event.ignore()


    ###############
    def open(self):
        fileName = QFileDialog.getOpenFileName( self, "Ouvrir", "", "*.html")
        f = open(fileName[0],"r")
        text = f.read()
        f.close()
        self.textedit.setHtml(text)
        print(fileName)
    
    ###############
    def save(self):
        fileName = QFileDialog.getSaveFileName( self, "Sauvegarder", "", "*.html")
        f = open(fileName[0],"w")
        text = self.textedit.toHtml()
        text = f.write(text)
        f.close()
        print(fileName)       

    ###############
    def quit(self):
        msg = QMessageBox()
        msg.setText("Voulez-vous quitter ?")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        if msg.exec() == QMessageBox.Ok : 
            sys.exit()     

def main(args):
    print("Hello World")
    app = QApplication(args)
    r = MainWindow()
    r.show()
    app.exec()
    
    

if __name__ == "__main__":
    main(sys.argv) 
    
#Q1
#importer les dépendances
    
#Q2
#Il fallait créer l'application Qt puis l'exécuter 
    
#Q4
#Il faut faire "Action.triggered.connect(fonction)"
import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from Canvas import *
import resources

class MainWindow(QMainWindow):

    def __init__(self, parent = None ):
        QMainWindow.__init__(self, parent )
        
        self.CreateActs()
        self.CreatefileMenu()
        self.Createtoolbar()
        self.statusBar()
        self.CreateCentralWidget()
        print("constructeur de la class MainWindow")
        
        print( "init mainwindow")
        self.resize(600, 500)

        bar = self.menuBar()
        fileMenu = bar.addMenu("File")

        colorMenu = bar.addMenu("Color")
        actPen = fileMenu.addAction(QIcon(":/icons/pen.png"), "&Pen color", self.pen_color, QKeySequence("Ctrl+P"))
        actBrush = fileMenu.addAction(QIcon(":/icons/brush.png"), "&Brush color", self.brush_color, QKeySequence("Ctrl+B"))

        colorToolBar = QToolBar("Color")
        self.addToolBar( colorToolBar )
        colorToolBar.addAction( actPen )
        colorToolBar.addAction( actBrush )

        shapeMenu = bar.addMenu("Shape")
        actRectangle = fileMenu.addAction(QIcon(":/icons/rectangle.png"), "&Rectangle", self.rectangle )
        actEllipse = fileMenu.addAction(QIcon(":/icons/ellipse.png"), "&Ellipse", self.ellipse)
        actFree = fileMenu.addAction(QIcon(":/icons/free.png"), "&Free drawing", self.free_drawing)

        shapeToolBar = QToolBar("Shape")
        self.addToolBar( shapeToolBar )
        shapeToolBar.addAction( actRectangle )
        shapeToolBar.addAction( actEllipse )
        shapeToolBar.addAction( actFree )

        modeMenu = bar.addMenu("Mode")
        actMove = modeMenu.addAction(QIcon(":/icons/move.png"), "&Move", self.move)
        actDraw = modeMenu.addAction(QIcon(":/icons/draw.png"), "&Draw", self.draw)
        actSelect = modeMenu.addAction(QIcon(":/icons/select.png"), "&Select", self.select)

        modeToolBar = QToolBar("Navigation")
        self.addToolBar( modeToolBar )
        modeToolBar.addAction( actMove )
        modeToolBar.addAction( actDraw )
        modeToolBar.addAction( actSelect )

    ##############
    def CreateActs(self):
        self.newact = QAction(QIcon(":/icons/new.png"), "Nouveau...", self)
        self.openact = QAction(QIcon(":/icons/open.png"), "Ouvrir...", self)
        self.saveact = QAction(QIcon(":/icons/save.png"), "Sauvegarder", self)
        self.closeact = QAction(QIcon(":/icons/quit.png"), "Quitter", self)
        
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
    
    def CreateCentralWidget(self) :
        self.widget = QWidget()
        self.setCentralWidget(self.widget)
        self.layout = QVBoxLayout()
        self.widget.setLayout(self.layout)
        self.textEdit = QTextEdit()
        self.canvas = Canvas()
        self.layout.addWidget(self.canvas)
        self.layout.addWidget(self.textEdit)
        
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
        self.textEdit.setHtml(text)
        print(fileName)
    
    ###############
    def save(self):
        fileName = QFileDialog.getSaveFileName( self, "Sauvegarder", "", "*.html")
        f = open(fileName[0],"w")
        text = self.textEdit.toHtml()
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

    ##############
    def pen_color(self):
        self.log_action("choose pen color")
        colorD = QColorDialog()
        colorD.exec()
        self.canvas.setPenColor(colorD.selectedColor())

    def brush_color(self):
        self.log_action("choose brush color")
        colorD = QColorDialog()
        colorD.exec()
        self.canvas.setBrushColor(colorD.selectedColor())

    def rectangle(self):
        self.log_action("Shape mode: rectangle")
        self.canvas.setShape(0)

    def ellipse(self):
        self.log_action("Shape Mode: circle")
        self.canvas.setShape(1)

    def free_drawing(self):
        self.log_action("Shape mode: free drawing")
        self.canvas.setShape(2)

    def move(self):
        self.log_action("Mode: move")

    def draw(self):
        self.log_action("Mode: draw")

    def select(self):
        self.log_action("Mode: select")

    def log_action(self, str):
        content = self.textEdit.toPlainText()
        self.textEdit.setPlainText( content + "\n" + str)

if __name__=="__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()
    app.exec_()

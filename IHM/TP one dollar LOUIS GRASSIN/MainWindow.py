import sys
import numpy as np
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from gdrawer import GDrawer
from Canvas import Canvas

import pickle


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)

        self.thumbnail_size = 150
        self.resize(600, 500)

        bar = self.menuBar()
        fileMenu = bar.addMenu("File")
        actOpen = fileMenu.addAction(QIcon("./icons/open.png"), "&Open...", self.open, QKeySequence("Ctrl+O"))
        actSave = fileMenu.addAction(QIcon("./icons/save.png"), "&Save...", self.save, QKeySequence("Ctrl+S"))
        actQuit = fileMenu.addAction(QIcon("./icons/quit.png"), "&Quit...", self.quit, QKeySequence("Ctrl+Q"))

        fileToolBar = QToolBar("File")
        self.addToolBar(fileToolBar)
        fileToolBar.addAction(actOpen)
        fileToolBar.addAction(actSave)

        self.container = QWidget(self)
        v_layout = QVBoxLayout(self.container)
        self.container.setLayout(v_layout)

        self.gallery = self.create_template_gallery()
        v_layout.addWidget(self.gallery)

        self.canvas = Canvas()
        v_layout.addWidget(self.canvas)

        self.textEdit = QTextEdit(self)
        v_layout.addWidget(self.textEdit)

        self.setCentralWidget(self.container)

        self.canvas.selected_template.connect(self.set_action_on_gesture)

        name = ["Triangle", "X", "Rectangle", "Circle", "Check", "Caret", "Question", "Arrow", "left square bracket",
                "Right square bracket", "V", "Delete", "Left curly brace", "Right curly brace", "Star", "Pigtail"]

        d = pickle.load(open('./onedol_ds.pkl', 'rb'))

        data = d['dataset']

        labels = d['labels']

        label = -1
        all_gesture = False
        for g, l in zip(data, labels):
            if l != label:

                self.add_template_thumbnail(g, name[l])

                self.canvas.oneDollar.addTemplate(g, name[l])

                if not all_gesture:
                    label = l

    def create_template_gallery(self):
        gallery = QListWidget()
        gallery.setMinimumSize(600,200)

        gallery.setViewMode(QListView.IconMode)
        gallery.setUniformItemSizes(True)
        gallery.setIconSize(QSize(100, 100))

        return gallery

    def add_template_thumbnail(self, g, label):

        # draw the template path into a QIcon (icon)
        thumbnail_widget = GDrawer()
        thumbnail_widget.set_gesture_path(g, label)
        pix = QPixmap(thumbnail_widget.size())
        thumbnail_widget.render(pix, QPoint(), QRegion(0, 0, thumbnail_widget.width(), thumbnail_widget.height()));
        icon = QIcon(pix)

        QListWidgetItem(icon, label, self.gallery)

    #######################
    # TODO 9
    #######################
    def set_action_on_gesture(self, label, id, score):
        message = "template: " + label + " score: " + str(score)
        self.textEdit.setPlainText(message + "\n" + self.textEdit.toPlainText())

        self.gallery.setCurrentRow(id)

    ##############
    def open(self):
        fileName = QFileDialog.getOpenFileName(self, "Open file", ".")
        file = open(fileName[0], 'r')
        str = file.readlines()
        str = '\n'.join(str)
        self.textEdit.setHtml(str)
        file.close()

    ###############
    def save(self):
        fileName = QFileDialog.getSaveFileName(self, "Save file", ".")
        with open(fileName[0], 'w') as fileSave:
            string = self.textEdit.toPlainText()
            fileSave.write(string)
            fileSave.close()
            print("Save... ", fileName[0], " saved.")

    ###############
    def quit(self):
        box = QMessageBox()
        b = box.question(self, 'Exit?', "Do you really want to exit ?", QMessageBox.Yes | QMessageBox.No)
        box.setIcon(QMessageBox.Question)
        if b == QMessageBox.Yes:
            sys.exit()

    def closeEvent(self, event):
        # event.ignore()
        # self.quit()
        return

    def log_action(self, str):
        content = self.textEdit.toPlainText()
        self.textEdit.setPlainText(content + "\n" + str)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()

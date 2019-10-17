import requests
from bs4 import BeautifulSoup

from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit
from PyQt5.QtCore import pyqtSlot
from pyqtgraph.Qt import QtCore, QtGui

import sys
import time

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Get youtube subtitle'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.subtitleResult = ""
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.grid = QtGui.QGridLayout()

        self.label = QtGui.QLabel(self)
        self.label.setText("Video URL: ")
        self.grid.addWidget(self.label, 1, 1, 1, 1) 
        
        self.le = QtGui.QLineEdit("", self)
        self.grid.addWidget(self.le, 1, 2, 1, 2)

        self.radiobuttonEn = QtGui.QRadioButton("English", self)
        self.grid.addWidget(self.radiobuttonEn, 2, 1, 1, 1)
        self.radiobuttonJp = QtGui.QRadioButton("Japanese", self)
        self.grid.addWidget(self.radiobuttonJp, 2, 2, 1, 1)
        self.radiobuttonTc = QtGui.QRadioButton("Tranditional Chinese", self)
        self.grid.addWidget(self.radiobuttonTc, 2, 3, 1, 1)

        self.btnGp = QtGui.QButtonGroup(self)
        self.btnGp.addButton(self.radiobuttonEn, 1)
        self.btnGp.addButton(self.radiobuttonJp, 2)
        self.btnGp.addButton(self.radiobuttonTc, 3)
        self.lang = ''
        self.btnGp.buttonClicked.connect(self.radioBtnOnClicked)

        self.btnConvert = QtGui.QPushButton('Get subtitle', self)
        self.grid.addWidget(self.btnConvert, 3, 1, 1, 1)
        self.btnConvert.clicked.connect(self.convert)

        self.btnSave = QtGui.QPushButton('Save File', self)
        self.grid.addWidget(self.btnSave, 3, 2, 1, 1)
        self.btnSave.clicked.connect(self.file_save)
        self.btnSave.setEnabled(False)

        self.btnReet = QtGui.QPushButton('Reset', self)
        self.grid.addWidget(self.btnReet, 3, 3, 1, 1)
        self.btnReet.clicked.connect(self.reset)

        self.textbox = QtGui.QLabel(self)
        self.grid.addWidget(self.textbox, 4, 1, 1, 3)
        self.textbox.resize(100, 10)      
                
        self.setLayout(self.grid)
        self.show()

    # Set language according to which radio button is checked
    # reference: http://www.lingoes.net/en/translator/langcode.htm
    def radioBtnOnClicked(self):
        sender = self.sender()
        if sender == self.btnGp:
            if self.btnGp.checkedId() == 1:
                self.lang = "en"
            elif self.btnGp.checkedId() == 2:
                self.lang = "ja"
            elif self.btnGp.checkedId() == 3:
                self.lang = "zh-TW"

    # Clear the content of textbox and reset the status of btnSave
    def reset(self):
        self.textbox.setText("")
        self.btnSave.setEnabled(False)

    def convert(self):
        self.btnConvert.setEnabled(False)
    
        if len(self.le.text()) > 0:
            self.textbox.setText("Converting... Please wait.")
            vidId = self.le.text().replace("https://www.youtube.com/watch?v=", "")
            self.radiobutton = self.sender()

            if len(vidId) >0 and self.lang != "":
                self.get_subtitle(vidId)
            if self.lang == "":
                self.textbox.setText("Please select a language.")
        else:
            self.textbox.setText("Please input the URL.")

        self.btnConvert.setEnabled(True)

    @pyqtSlot()
    def get_subtitle(self, vidIdIn):
        
        subtitleURL = 'http://video.google.com/timedtext?lang='
        vidSubtitle = subtitleURL + self.lang + '&v=' + vidIdIn

        resp = requests.get(vidSubtitle)
        soup = BeautifulSoup(resp.text, 'html.parser')

        subtitleTexts = soup.find_all("text")
        if len(subtitleTexts) == 0:
            self.textbox.setText("No subtitles found.")
            self.btnSave.setEnabled(False)
        else:
            self.subtitleResult = ""

            for subText in subtitleTexts:
                line = subText.text

                if(line.find("&#39;")): 
                    line = line.replace("&#39;", "'")
                if(line.find("&quot;")):
                    line = line.replace("&quot;", "\"")
                if(line.find("\n")):
                    line = line.replace("\n", " ")

                self.subtitleResult += line
                self.subtitleResult += " "
            
            self.textbox.setText("Subtitle generated.")
            self.btnSave.setEnabled(True)

    def file_save(self):
        name = QtGui.QFileDialog.getSaveFileName(self, 'Save File')
        if(len(self.subtitleResult) > 0):
            # Only save file with path whose lenth if greater than 0
            if(len(str(name[0])) > 0 ):
                textFile = open(str(name[0]), "w")
                textFile.write(self.subtitleResult)
                textFile.write(" ")
                textFile.close()
                self.textbox.setText("Subtitle saved.")
        else:
            self.textbox.setText("No content to save.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
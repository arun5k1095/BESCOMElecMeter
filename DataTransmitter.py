#DataTransMitter
# Tool = "BESCOM ElecMeter"
# HandcraftedBy : "AIVolved"\
# Version = "1.0"
# LastModifiedOn : "3rd Mar 2022"
import Resources
from threading import*
import json,requests
import urllib.request
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from threading import*
import os
import sys
import time
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
import requests
import urllib.request
import time
import webbrowser
from datetime import datetime



def showUserInfo(message):
   msgBox = QMessageBox()
   msgBox.setIcon(QMessageBox.Information)
   msgBox.setText(message)
   msgBox.setWindowTitle("Status Update")
   msgBox.setStandardButtons(QMessageBox.Ok)
   msgBox.show()

   returnValue = msgBox.exec()
   if returnValue == QMessageBox.Ok: pass
   else: pass


if __name__ == "__main__":

    Aplication = QApplication(sys.argv)
    MainWindowGUI = QWidget()
    MainWindowGUI.setFixedSize(680, 280)
    MainWindowGUI.setWindowTitle('BESCOMElecMeter Data Transmitter')
    MainWindowGUI.setStyleSheet("background-color: black;")
    MainWindowGUI.setObjectName("MainMenu");
    IconFilepath = ":/resources/AI_Volved.ico"
    MainWindowGUI.setStyleSheet("QWidget#MainMenu{background-image: url(:/resources/TransmitWallpaper.jpg);}");
    MainWindowGUI.setWindowIcon(QtGui.QIcon(IconFilepath))


    Label = QLabel(" Data",MainWindowGUI)
    Label.move(1,20)
    Label.setStyleSheet("color: white;")
    Label.setFont(QFont('Times', 12))
    Label.setFixedSize(600,50)

    LabelStatus = QLabel("Transmit Status: NA", MainWindowGUI)
    LabelStatus.move(52, 100)
    LabelStatus.setStyleSheet("color: white;")
    LabelStatus.setFixedSize(300, 45)


    EditBox = QLineEdit(MainWindowGUI)
    EditBox.setFixedSize(600,50)
    EditBox.setStyleSheet("border-color: yellow;border-width: 2px;")


    EditBox.move(60,20)
    EditBox.setText("$MM,00000,120,120,121,1,$S1,00000,120,120,121,0,$S2,00000,120,120,121,0")
    #e4.textChanged.connect(self.textchanged)

    prevSentTime = 0
    currTransmitAttemptTime =0
    def transmit_date():
        global prevSentTime,currTransmitAttemptTime
        currTransmitAttemptTime = time.time()

        if (currTransmitAttemptTime-prevSentTime) > 20 :
             pass
        else :
            showUserInfo("Attempt after min 20 seconds have elapsed since last data Transmit to server"+\
                         "\n"+"Time elapsed : "+str(currTransmitAttemptTime-prevSentTime)[0:5]+" seconds")
            return

        try:
            data = EditBox.text().strip()
            PUSHKEYURL = "https://api.thingspeak.com/update?api_key=X26Q6CXU4TVYR5GP&field1="
            req = PUSHKEYURL+data
            response = urllib.request.urlopen(req)
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S:%f")
            LabelStatus.setText(str("Status: Successful at "+str(current_time)+" Hrs"))
            prevSentTime = time.time()
        except Exception as error :
            LabelStatus.setText(str(error))




    Button = QPushButton("Transmit" , MainWindowGUI)
    Button.setFixedSize(80,45)
    Button.setStyleSheet("background-color: green;")
    Button.move(570,100)
    Button.clicked.connect(transmit_date)

    MainWindowGUI.show()
    sys.exit(Aplication.exec_())


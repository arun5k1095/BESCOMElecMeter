# Tool = "BESCOM ElecMeter"
# HandcraftedBy : "Atharvan Technoligical Development Center (ATDC)"\
# Web : www.atharvantechsys.com
# Version = "1.4"
# LastModifiedOn : "5th April 2022"


#!/usr/bin/python3
# -*- coding: utf-8 -*-

import Resources
import copy
import requests
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from threading import*
import os
import sys
import time
import datetime
from PyQt5.QtWidgets import *
from PyQt5 import QtGui

MMPrev = [11111, 0, 0, 0, 0]
S1Prev = [11111, 0, 0, 0, 0]
S2Prev = [11111, 0, 0, 0, 0]


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

   #msgBox.buttonClicked.connect(msgButtonClick)
   #returnValue = msgBox.exec()


class Label():
    def __init__(self , text):
        self.Label = QLabel(text)
        self.Label.setFixedSize(80, 40)
        self.Label.setFont(QFont('Times', 14))
        #self.Label.setStyleSheet("border: 1px solid dodgerblue;")
        self.Label.setAlignment(Qt.AlignCenter)


class  LCDDisplay():
    def __init__(self , value):
        self.LCD = QLCDNumber()
        self.LCD.setStyleSheet("color: rgb(20, 114, 175)")
        self.LCD.setStyleSheet("background-color: #C5D6D0")
        self.LCD.setFont(QFont('Times', 14))
        self.LCD.setFixedSize(80, 40)
        self.LCD.display(str(value))


class TaskControlBtn:
    def __init__(self, Cord_X, Cord_Y, Iconname):
        self.button = QPushButton(MainWindowGUI)
        self.button.move(Cord_X, Cord_Y)
        self.button.resize(37, 37)
        self.button.show()



# Acquire relative paths of files
def resource_path(relative_path):
   try:
        base_path = sys._MEIPASS
   except Exception:
        base_path = os.path.abspath(".")
   return os.path.join(base_path, relative_path)
#IconFilepath = resource_path(":/resources/AI_Volved.ico")
IconFilepath = ":/resources/electricity_13643.ico"

def GenerateLog():
    ServerGETUrl = " https://api.thingspeak.com/channels/1664584/feeds.json"
    recievedData = requests.get(url=ServerGETUrl, verify=False)
    data = recievedData.json()

    Log = []
    for DataField in data["feeds"]:
        F1 = DataField["field1"]

        if F1 is not None:
            field = F1
        else: field = "Invalid Data"

        data = "Updated: " + str(DataField["created_at"]) + " UTC, Data:  " + field
        Log.append(data)

    LogFile = open("Log_BESCOMElecMTR.txt", "w+")

    for index in range(len(Log)):
        LogFile.write(Log[index] + "\n")
    LogFile.close()

    showUserInfo("Log File has been successfully Generated.")

def updatefields(MM,S1,S2):
    global MOverallHealth_Label

    def ERRnoERRARb(data,LCDObj):
        if data=="1":
            LCDObj.LCD.setStyleSheet("background-color: #F5C6BE")
            return "1"
        else :
            LCDObj.LCD.setStyleSheet("background-color: #C5D6D0")
            return "0"



    MM_R.LCD.display(ERRnoERRARb(MM[0][0],MM_R))
    MM_B.LCD.display(ERRnoERRARb(MM[0][1],MM_B))
    MM_Y.LCD.display(ERRnoERRARb(MM[0][2],MM_Y))
    MM_N.LCD.display(ERRnoERRARb(MM[0][3],MM_N))
    MM_G.LCD.display(ERRnoERRARb(MM[0][4],MM_G))
    MM_Phase_R.LCD.display(MM[1])
    MM_Phase_Y.LCD.display(MM[2])
    MM_Phase_B.LCD.display(MM[3])

    S1_R.LCD.display(ERRnoERRARb(S1[0][0],S1_R))
    S1_B.LCD.display(ERRnoERRARb(S1[0][1],S1_B))
    S1_Y.LCD.display(ERRnoERRARb(S1[0][2],S1_Y))
    S1_N.LCD.display(ERRnoERRARb(S1[0][3],S1_N))
    S1_G.LCD.display(ERRnoERRARb(S1[0][4],S1_G))

    S1_Phase_R.LCD.display(S1[1])
    S1_Phase_Y.LCD.display(S1[2])
    S1_Phase_B.LCD.display(S1[3])

    S2_R.LCD.display(ERRnoERRARb(S2[0][0],S2_R))
    S2_B.LCD.display(ERRnoERRARb(S2[0][1],S2_B))
    S2_Y.LCD.display(ERRnoERRARb(S2[0][2],S2_Y))
    S2_N.LCD.display(ERRnoERRARb(S2[0][3],S2_N))
    S2_G.LCD.display(ERRnoERRARb(S2[0][4],S2_G))

    S2_Phase_R.LCD.display(S2[1])
    S2_Phase_Y.LCD.display(S2[2])
    S2_Phase_B.LCD.display(S2[3])


    MCCBstatus = "NA"
    S1status = "NA"
    S2status = "NA"
    errFlag = 0
    if (MM[4] == "1") :
        MCCBstatus = "MCCB        :   ON"
    else :
        MCCBstatus = "MCCB        :   OFF"
        errFlag = 1

    if (S1[4] == "0") :
        S1status = "S1 COMM  :   OK"
    else:
            S1status = "S1 COMM  :   NOT OK"
            errFlag= 1
    if (S2[4] == "0"):
        S2status = "S2 COMM  :   OK"
    else:
        S2status = "S2 COMM  :   NOT OK"
        errFlag = 1
    if errFlag :
        MOverallHealth_Label.Label.setStyleSheet("QLabel {color : red; }");
    else: MOverallHealth_Label.Label.setStyleSheet("QLabel {color : green; }");

    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M:%S:%f")

    StatusUpdate = "Live Status:"+"\n\n"+MCCBstatus +"\n"+ S1status +"\n"+ S2status + "\n\n"+"Last synched Time: "+current_time
    MOverallHealth_Label.Label.setText(StatusUpdate)


def ArbitrateTask():
    try:
        if not Task1.is_alive():
            Task1.start()
        else: showUserInfo("Server Synch already initiated")
    except Exception as error : showUserInfo(error)
DataLogTable = {}
def StartOperation():
    global StartOperationBtn,DataLogTable,MMPrev,S1Prev,S2Prev
    StartOperationBtn.setStyleSheet(
            "QPushButton {border: 1px blue;border-radius: 5px;  background-color: green; color : white;}""QPushButton::hover"
            "{"
            "background-color : #228B22;"
            "}")
    StartOperationBtn.setText("Connected")

    while(1):
        ServerGETUrl = " https://api.thingspeak.com/channels/1664584/feeds.json"
        recievedData = requests.get(url=ServerGETUrl, verify=False)
        data = recievedData.json()
        #print(data)

        LastUpdatedData = data["feeds"][-1]["field1"].split("$")[1:]

        def LogTablUpdate():
            global DataLogTable,MMPrev,S1Prev,S2Prev

            DataLogTable.clear()


            for DataField in data["feeds"]:
                #print(DataField)
                MMData=str(DataField["field1"]).strip().split("$")[1]
                S1Data=str(DataField["field1"]).strip().split("$")[2]
                S2Data=str(DataField["field1"]).strip().split("$")[3]

                MMData = MMData[3:len(MMData)-1]
                S1Data = S1Data[3:len(S1Data)-1]
                S2Data = S2Data[3:]
                DataLogTable[DataField["created_at"].replace("Z","").replace("T"," ")] = [MMData,S1Data,S2Data]

            #print(DataLogTable)
            DataLogTableTimeStamps = list(DataLogTable.keys())

            if len(DataLogTableTimeStamps) > 5:
                DataLogTableTimeStamps = list(DataLogTable.keys())[-5:]

            for row in range(len(DataLogTableTimeStamps)) :
                TimeInIST = datetime.datetime.strptime(str(DataLogTableTimeStamps[row]),'%Y-%m-%d %H:%M:%S') \
                           + datetime.timedelta(hours=5,minutes=30)
                LogTable.setItem(row, 0, QTableWidgetItem(str(TimeInIST)))
                LogTable.setItem(row, 1, QTableWidgetItem(DataLogTable[DataLogTableTimeStamps[row]][0]))
                LogTable.setItem(row, 2, QTableWidgetItem(DataLogTable[DataLogTableTimeStamps[row]][1]))
                LogTable.setItem(row, 3, QTableWidgetItem(DataLogTable[DataLogTableTimeStamps[row]][2]))
                LogTable.update()



        try:
            if data["feeds"][-1]["field1"] is not None:

                MM = LastUpdatedData[0].split(",")[1:]
                S1 = LastUpdatedData[1].split(",")[1:]
                S2 = LastUpdatedData[2].split(",")[1:]
            else :
                MM = [11111,0,0,0,0]
                S1 = [11111,0,0,0,0]
                S2 = [11111,0,0,0,0]
        except :
            MM = [11111, 0, 0, 0, 0]
            S1 = [11111, 0, 0, 0, 0]
            S2 = [11111, 0, 0, 0, 0]
        try:



            if(MM!=MMPrev or S1!=S1Prev or S2!=S2Prev):
                updatefields(MM, S1, S2)

            MMPrev = copy.deepcopy(MM)
            S1Prev = copy.deepcopy(S1)
            S2Prev = copy.deepcopy(S2)
        except Exception as error:
            print(error)
            continue
        LogTablUpdate()
        MainWindowGUI.update()
        time.sleep(3)



Task1 = Thread(target=StartOperation)

if __name__ == "__main__":

    Aplication = QApplication(sys.argv)
    MainWindowGUI = QWidget()
    MainWindowGUI.setFixedSize(1366, 768)
    MainWindowGUI.setWindowTitle('BESCOM ElecMeter')
    MainWindowGUI.setStyleSheet("background-color: white;")
    MainWindowGUI.setObjectName("MainMenu");
    #QString qwidgetStyle = "QWidget#MainMenu {background-image: url(background.jpg);}";
    #qwidgetStyle = "QWidget#MainMenu {background-image: url(background.jpg); border: 5px solid rgba(3, 5, 28, 1);}";
    MainWindowGUI.setStyleSheet("QWidget#MainMenu{background-image: url(:/resources/Wallpaper.jpg) no-repeat center center fixed;}")
    MainWindowGUI.setWindowIcon(QtGui.QIcon(IconFilepath))

    Xfactor = -170
    Yfactor = 40
    #MM_Data_Frame.setStyleSheet("QFrame { background-color: dodgerblue } ");
    #MM_Data_Frame.setFrameStyle(QFrame.Panel | QFrame.Raised)
    # Label_RBYNG_Frame.setStyleSheet("QFrame {  background-color : rgba(255, 255, 255, 10); }")

    Label_RBYNG_Frame = QFrame(MainWindowGUI)
    Label_RBYNG_Frame.move(500+Xfactor, 10+Yfactor)
    Label_RBYNG_Frame.setStyleSheet("background-color: 	darkgrey")

    MM_Data_Frame = QFrame(MainWindowGUI)
    MM_Data_Frame.move(500+Xfactor, 110+Yfactor)
    S1_Data_Frame = QFrame(MainWindowGUI)
    S1_Data_Frame.move(500+Xfactor, 190+Yfactor-30)
    S2_Data_Frame = QFrame(MainWindowGUI)
    S2_Data_Frame.move(500+Xfactor, 270+Yfactor-60)

    MM_PhaseData_Frame = QFrame(MainWindowGUI)
    MM_PhaseData_Frame.move(980+Xfactor, 110+Yfactor)
    S1_PhaseData_Frame = QFrame(MainWindowGUI)
    S1_PhaseData_Frame.move(980+Xfactor, 190+Yfactor-30)
    S2_PhaseData_Frame = QFrame(MainWindowGUI)
    S2_PhaseData_Frame.move(980+Xfactor, 270+Yfactor-60)

    MS_Frame = QFrame(MainWindowGUI)
    MS_Frame.move(370+Xfactor, 110 + Yfactor)
    Phase_Frame = QFrame(MainWindowGUI)
    Phase_Frame.move(980+Xfactor, 10 + Yfactor)
    Phase_Frame.setStyleSheet("background-color: 	darkgrey")
    DataLog_Frame = QFrame(MainWindowGUI)
    DataLog_Frame.move(1600+Xfactor, 50 + Yfactor)


    MOverallHealth_Frame = QFrame(MainWindowGUI)
    MOverallHealth_Frame.move(1270+Xfactor, 10 + 380)
    MOverallHealth_Label = Label("Live Status : NA")
    MOverallHealth_Label.Label.setFont(QFont('Times', 8))
    MOverallHealth_Label.Label.setFixedSize(400, 300)
    MOverallHealth_Label.Label.setAlignment(Qt.AlignLeft)
    MOverallHealth_Frame_DataFramelayout = QHBoxLayout(MOverallHealth_Frame)
    MOverallHealth_Frame_DataFramelayout.addWidget(MOverallHealth_Label.Label)
    MOverallHealth_Frame_DataFramelayout.setContentsMargins(0, 0, 0, 0)

    MM_R_Label = Label("R")
    MM_R_Label.Label.setFixedSize(75, 40)
    MM_R_Label.Label.setStyleSheet("color : red; ");
    MM_B_Label = Label("Y")
    MM_B_Label.Label.setFixedSize(75, 40)
    MM_B_Label.Label.setStyleSheet("color : yellow;  ");
    MM_Y_Label = Label("B")
    MM_Y_Label.Label.setFixedSize(75, 40)
    MM_Y_Label.Label.setStyleSheet("color : blue;  ");
    MM_N_Label = Label("P")
    MM_N_Label.Label.setFixedSize(75, 40)
    MM_G_Label = Label("N")
    MM_G_Label.Label.setFixedSize(75, 40)
    MM_G_Label.Label.setStyleSheet("color : brown;  ");

    MM_Label = Label("MM")
    S1_Label = Label("S1")
    S2_Label = Label("S2")

    Phase1_Label = Label("ϕR")
    Phase1_Label.Label.setFixedSize(80, 60)
    Phase2_Label = Label("ϕY")
    Phase2_Label.Label.setFixedSize(80, 60)
    Phase3_Label = Label("ϕB")
    Phase3_Label.Label.setFixedSize(80, 60)

    MM_R = LCDDisplay("0")
    MM_B = LCDDisplay("0")
    MM_Y = LCDDisplay("0")
    MM_N = LCDDisplay("0")
    MM_G = LCDDisplay("0")

    MM_Phase_R = LCDDisplay("0")
    MM_Phase_Y = LCDDisplay("0")
    MM_Phase_B = LCDDisplay("0")

    S1_R = LCDDisplay("0")
    S1_B = LCDDisplay("0")
    S1_Y = LCDDisplay("0")
    S1_N = LCDDisplay("0")
    S1_G = LCDDisplay("0")

    S1_Phase_R = LCDDisplay("0")
    S1_Phase_Y = LCDDisplay("0")
    S1_Phase_B = LCDDisplay("0")

    S2_R = LCDDisplay("0")
    S2_B = LCDDisplay("0")
    S2_Y = LCDDisplay("0")
    S2_N = LCDDisplay("0")
    S2_G = LCDDisplay("0")

    S2_Phase_R = LCDDisplay("0")
    S2_Phase_Y = LCDDisplay("0")
    S2_Phase_B = LCDDisplay("0")

    #MainWindowGUI.horizontalGroupBox = QGroupBox("MM")

    MM_Data_Framelayout = QHBoxLayout(MM_Data_Frame)
    MM_Data_Framelayout.addWidget(MM_R.LCD)
    MM_Data_Framelayout.addWidget(MM_B.LCD)
    MM_Data_Framelayout.addWidget(MM_Y.LCD)
    MM_Data_Framelayout.addWidget(MM_N.LCD)
    MM_Data_Framelayout.addWidget(MM_G.LCD)
    MM_Data_Frame.setLayout(MM_Data_Framelayout)
    MM_Data_Framelayout.setContentsMargins(0, 0, 0, 0)

    S1_Data_Framelayout = QHBoxLayout(S1_Data_Frame)
    S1_Data_Framelayout.addWidget(S1_R.LCD)
    S1_Data_Framelayout.addWidget(S1_B.LCD)
    S1_Data_Framelayout.addWidget(S1_Y.LCD)
    S1_Data_Framelayout.addWidget(S1_N.LCD)
    S1_Data_Framelayout.addWidget(S1_G.LCD)
    S1_Data_Frame.setLayout(S1_Data_Framelayout)
    S1_Data_Framelayout.setContentsMargins(0, 0, 0, 0)

    S2_Data_Framelayout = QHBoxLayout(S2_Data_Frame)
    S2_Data_Framelayout.addWidget(S2_R.LCD)
    S2_Data_Framelayout.addWidget(S2_B.LCD)
    S2_Data_Framelayout.addWidget(S2_Y.LCD)
    S2_Data_Framelayout.addWidget(S2_N.LCD)
    S2_Data_Framelayout.addWidget(S2_G.LCD)
    S2_Data_Frame.setLayout(S2_Data_Framelayout)
    S2_Data_Framelayout.setContentsMargins(0, 0, 0, 0)


    MS_Framelayout = QVBoxLayout(MS_Frame)
    MS_Framelayout.addWidget(MM_Label.Label)
    MS_Framelayout.addWidget(S1_Label.Label)
    MS_Framelayout.addWidget(S2_Label.Label)
    MS_Framelayout.setContentsMargins(0, 0, 0, 0)


    layout = QHBoxLayout(Label_RBYNG_Frame)
    layout.addWidget(MM_R_Label.Label)
    layout.addWidget(MM_B_Label.Label)
    layout.addWidget(MM_Y_Label.Label)
    layout.addWidget(MM_N_Label.Label)
    layout.addWidget(MM_G_Label.Label)
    Label_RBYNG_Frame.setLayout(layout)

    MS_Framelayout = QHBoxLayout(Phase_Frame)
    MS_Framelayout.addWidget(Phase1_Label.Label)
    MS_Framelayout.addWidget(Phase2_Label.Label)
    MS_Framelayout.addWidget(Phase3_Label.Label)
    MS_Framelayout.setContentsMargins(0, 0, 0, 0)

    MS_DataFramelayout = QHBoxLayout(MM_PhaseData_Frame)
    MS_DataFramelayout.addWidget(MM_Phase_R.LCD)
    MS_DataFramelayout.addWidget(MM_Phase_Y.LCD)
    MS_DataFramelayout.addWidget(MM_Phase_B.LCD)
    MS_DataFramelayout.setContentsMargins(0, 0, 0, 0)

    MS_DataFramelayout = QHBoxLayout(S1_PhaseData_Frame)
    MS_DataFramelayout.addWidget(S1_Phase_R.LCD)
    MS_DataFramelayout.addWidget(S1_Phase_Y.LCD)
    MS_DataFramelayout.addWidget(S1_Phase_B.LCD)
    MS_DataFramelayout.setContentsMargins(0, 0, 0, 0)

    MS_DataFramelayout = QHBoxLayout(S2_PhaseData_Frame)
    MS_DataFramelayout.addWidget(S2_Phase_R.LCD)
    MS_DataFramelayout.addWidget(S2_Phase_Y.LCD)
    MS_DataFramelayout.addWidget(S2_Phase_B.LCD)
    MS_DataFramelayout.setContentsMargins(0, 0, 0, 0)





    StartOperationBtn = QPushButton(MainWindowGUI)
    StartOperationBtn.setText('Connect')
    StartOperationBtn.move(1350+Xfactor, 10 + Yfactor)
    StartOperationBtn.resize(140, 50)
    StartOperationBtn.setStyleSheet(
            "QPushButton {border: 1px blue;border-radius: 5px;  background-color: #075691; color : white;}""QPushButton::hover"
            "{"
            "background-color : #1a85b4;"
            "}")
    StartOperationBtn.show()
    StartOperationBtn.clicked.connect(ArbitrateTask)

    SaveLog = QPushButton(MainWindowGUI)
    SaveLog.setText('Save Log')
    SaveLog.move(1350+Xfactor, 10 + Yfactor+60)
    SaveLog.resize(140, 50)
    SaveLog.setStyleSheet(
            "QPushButton {border: 1px blue;border-radius: 5px;  background-color: #075691; color : white;}""QPushButton::hover"
            "{"
            "background-color : #1a85b4;"
            "}")
    SaveLog.show()
    SaveLog.clicked.connect(GenerateLog)

    LogTable = QTableWidget(MainWindowGUI)
    LogTable.setRowCount(20)
    LogTable.setColumnCount(4)
    LogTable.setFixedSize(740,250)
    LogTable.setStyleSheet("background-color: 	lightgrey")
    LogTable.move(500+Xfactor, 380)
    TimeLable = QTableWidgetItem("Time stamp (IST)")
    MMDataLable = QTableWidgetItem("MM Data")
    S1DataLable = QTableWidgetItem("S1 Data")
    S2DataLable = QTableWidgetItem("S2 Data")
    LogTable.setHorizontalHeaderItem(0, TimeLable)
    LogTable.setHorizontalHeaderItem(1, MMDataLable)
    LogTable.setHorizontalHeaderItem(2, S1DataLable)
    LogTable.setHorizontalHeaderItem(3, S2DataLable)

    #MM_N.LCD.display("99")

    MainWindowGUI.showMaximized()
    sys.exit(Aplication.exec_())
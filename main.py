from PyQt6 import QtGui
from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.uic import loadUi
import sys
from pars import getRasp



class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        loadUi("main.ui", self)
        self.setWindowIcon(QtGui.QIcon('icon.png'))
        self.setWindowTitle("SUAI Schedule")
        self.weekNumK = 0
        self.setSemester()
        self.currDate = self.calendarWidget.selectedDate().toPyDate()
        self.updateRasp()


        # -------------------начальные значения групп итд-------------#
        self.currGroup = 0
        self.currProf = 0
        self.currBlock = 0
        self.currAud = 0

        # -------------------заполнение выборов группы итд-------------#
        self.group_comboBox.addItems(schedule.group)
        self.prof_comboBox.addItems(schedule.prof)
        self.block_comboBox.addItems(schedule.block)
        self.aud_comboBox.addItems(schedule.aud)

        #--------------------выбог группы итд---------------------------#
        self.group_comboBox.currentIndexChanged.connect(self.groupChanged)
        self.prof_comboBox.currentIndexChanged.connect(self.profChanged)
        self.block_comboBox.currentIndexChanged.connect(self.blockChanged)
        self.aud_comboBox.currentIndexChanged.connect(self.audChanged)

        self.todayButton.clicked.connect(self.setDateOnToday)  # кнопка сегодня
        self.calendarWidget.selectionChanged.connect(self.calendarDateChanged)#отслеживание изменения даты


    def groupChanged(self):
        self.currGroup = self.group_comboBox.currentIndex()
        schedule.newRasp(self.currGroup,self.currProf,self.currBlock,self.currAud)
        self.updateRasp()
    def profChanged(self):
        self.currProf = self.prof_comboBox.currentIndex()
        schedule.newRasp(self.currGroup, self.currProf, self.currBlock, self.currAud)
        self.updateRasp()
    def blockChanged(self):
        self.currBlock = self.block_comboBox.currentIndex()
        schedule.newRasp(self.currGroup, self.currProf, self.currBlock, self.currAud)
        self.updateRasp()
    def audChanged(self):
        self.currAud = self.aud_comboBox.currentIndex()
        schedule.newRasp(self.currGroup, self.currProf, self.currBlock, self.currAud)
        self.updateRasp()

    def calendarDateChanged(self):
        self.currDate=self.calendarWidget.selectedDate().toPyDate()
        #print("date changed to",self.currDate.weekday())
        self.updateRasp()
        #print(schedule.weekstr[currDate.weekday()])
    def setDateOnToday(self):
        self.calendarWidget.setSelectedDate(QDate.currentDate())
    def updateRasp(self):
        if (self.currDate.isocalendar()[1]+self.weekNumK) % 2==0:
            self.schedule_label.setText(schedule.weekup[self.currDate.weekday()])
        else:
            self.schedule_label.setText(schedule.weekdown[self.currDate.weekday()])
        self.info_label.setText(schedule.info[0]+schedule.legends+schedule.offschedulestr)
    def setSemester(self):
        fallSemStart=QDate(QDate.currentDate().year(),9,1)
        fallSemEnd=QDate(QDate.currentDate().year(),12,31)
        springSemStart=QDate(QDate.currentDate().year(),1,1)
        springSemEnd=QDate(QDate.currentDate().year(),5,31)

        if fallSemStart < QDate.currentDate() < fallSemEnd:
            self.calendarWidget.setMinimumDate(fallSemStart)
            self.calendarWidget.setMaximumDate(fallSemEnd)
        elif springSemStart < QDate.currentDate() < springSemEnd:
            self.calendarWidget.setMinimumDate(springSemStart)
            self.calendarWidget.setMaximumDate(springSemEnd)
        else:
            self.calendarWidget.setMinimumDate(QDate.currentDate())
            self.calendarWidget.setMaximumDate(QDate.currentDate())

        if fallSemStart.weekNumber()[0]%2==1:
            self.weekNumK=1


def window():
    app=QApplication(sys.argv)
    app.setApplicationName("SUAI Schedule")
    win = MyWindow()
    win.show()
    sys.exit(app.exec())


schedule = getRasp()
#schedule.printRasp()
window()



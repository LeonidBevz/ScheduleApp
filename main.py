from PyQt6 import QtGui
from PyQt6.QtGui import QTextCharFormat, QColor
from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QApplication,QWidget, QMainWindow, QFileDialog
from PyQt6.uic import loadUi
import sys
from pars import getRasp
from pathlib import Path
from plan import EdPlan


class MyWindow(QMainWindow):

    def __init__(self):
        super(MyWindow, self).__init__()
        loadUi("main.ui", self)
        self.setWindowIcon(QtGui.QIcon('icon.png'))
        self.setWindowTitle("SUAI Schedule")
        self.weekNumK = 0
        self.setSemester()
        self.currDate = self.calendarWidget.selectedDate().toPyDate()
        self.setCellsColour(self.SemStart,self.SemEnd)
        self.updateRasp()
        self.filename_edit=""
        self.currCourse=self.courseSpinBox.value()-1
        self.lineEdits=[self.lineEdit0,self.lineEdit1,self.lineEdit2,self.lineEdit3,self.lineEdit4,self.lineEdit5,self.lineEdit6,self.lineEdit7,self.lineEdit8,self.lineEdit9]
        self.spinBoxes=[self.spinBox0,self.spinBox1,self.spinBox2,self.spinBox3,self.spinBox4,self.spinBox5,self.spinBox6,self.spinBox7,self.spinBox8,self.spinBox9]

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

        self.fileDialogButton.clicked.connect(self.planFileChanged)
        self.todayButton.clicked.connect(self.setDateOnToday)  # кнопка сегодня
        self.calendarWidget.selectionChanged.connect(self.calendarDateChanged)#отслеживание изменения даты
        self.courseSpinBox.valueChanged.connect(self.updateCourse)


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
    def startFileDialog(self):
        filename, ok = QFileDialog.getOpenFileName(self,"Выбрать файл учебного плана","","Таблица (*.xlsx)")
        if filename:
            path = Path(filename)
            self.filename_edit=str(path)

    def setSemester(self):
        fallSemStart=QDate(QDate.currentDate().year(),9,1)
        fallSemEnd=QDate(QDate.currentDate().year(),12,31)
        springSemStart=QDate(QDate.currentDate().year(),1,1)
        springSemEnd=QDate(QDate.currentDate().year(),5,31)

        if fallSemStart < QDate.currentDate() < fallSemEnd:
            self.calendarWidget.setMinimumDate(fallSemStart)
            self.calendarWidget.setMaximumDate(fallSemEnd)
            self.SemStart=fallSemStart
            self.SemEnd=fallSemEnd
        elif springSemStart < QDate.currentDate() < springSemEnd:
            self.calendarWidget.setMinimumDate(springSemStart)
            self.calendarWidget.setMaximumDate(springSemEnd)
            self.SemStart = springSemStart
            self.SemEnd = springSemEnd
        else:
            self.calendarWidget.setMinimumDate(QDate.currentDate())
            self.calendarWidget.setMaximumDate(QDate.currentDate())

        if fallSemStart.weekNumber()[0]%2==1:
            self.weekNumK=1

    def setCellBlue(self, date):
        style = QTextCharFormat()
        style.setBackground(QColor(99, 189, 235))
        self.calendarWidget.setDateTextFormat(date,style)
    def setCellRed(self, date):
        style = QTextCharFormat()
        style.setBackground(QColor(231, 165, 156))
        self.calendarWidget.setDateTextFormat(date,style)
    def setCellsColour(self,startDate,endDate):
        while startDate<=endDate:
            if (startDate.weekNumber()[0]+self.weekNumK) % 2==0:
                self.setCellRed(startDate)
            else:
                self.setCellBlue(startDate)
            startDate=startDate.addDays(1)

    def planFileChanged(self):
        self.startFileDialog()
        Plan.getPlanFromFile(self.filename_edit)
        if len(Plan.planint)!=0:
            self.updatePlanLabels()
            self.updateWeekColors()
            self.courseSpinBox.setMaximum(len(Plan.planint))
    def updateCourse(self):
        self.currCourse=self.courseSpinBox.value()-1
        self.updatePlanLabels()
    def updateWeekColors(self):
        print("ты думал тут что-то будет")
    def updatePlanLabels(self):
        for i in range(len(Plan.planint[self.currCourse])):
            self.lineEdits[i].setText(Plan.plan[self.currCourse][i])
            self.spinBoxes[i].setValue(Plan.planint[self.currCourse][i])
    #def blockPlanLabelsValues(self):
    #    for i in range(10):
    #        self.lineEdits[i].
    #        self.spinBoxes[i].


#class PlanCellWidget(QWidget):
#    def __init__(self):
#        loadUi("planCellWidget.ui",self)

def window():
    app=QApplication(sys.argv)
    app.setApplicationName("SUAI Schedule")
    win = MyWindow()
    win.show()
    sys.exit(app.exec())


Plan=EdPlan()
schedule = getRasp()
window()




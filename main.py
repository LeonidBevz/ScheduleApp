from PyQt6 import QtGui
from PyQt6.QtGui import QTextCharFormat, QColor
from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QErrorMessage
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
        self.setWindowTitle("Schedule App")
        self.weekNumK = 0
        self.setSemester()
        self.currDate = self.calendarWidget.selectedDate().toPyDate()
        self.setCellsColourRB(self.SemStart, self.SemEnd)
        self.updateRasp()
        self.filename_edit = ""
        self.currCourse = self.courseSpinBox.value() - 1
        self.lineEdits = [self.lineEdit0, self.lineEdit1, self.lineEdit2, self.lineEdit3, self.lineEdit4,
                          self.lineEdit5, self.lineEdit6, self.lineEdit7, self.lineEdit8, self.lineEdit9]
        self.dspinBoxes = [self.dspinBox0, self.dspinBox1, self.dspinBox2, self.dspinBox3, self.dspinBox4,
                           self.dspinBox5, self.dspinBox6, self.dspinBox7, self.dspinBox8, self.dspinBox9]
        self.colors = [QColor(225, 204, 90), QColor(193, 63, 254), QColor(47, 204, 255), QColor(32, 255, 105),
                       QColor(32, 53, 255), QColor(255, 32, 137), QColor(255, 147, 32), QColor(61, 129, 0),
                       QColor(255, 240, 0), QColor(255, 51, 51)]

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

        # --------------------выбог группы итд---------------------------#
        self.group_comboBox.currentIndexChanged.connect(self.groupChanged)
        self.prof_comboBox.currentIndexChanged.connect(self.profChanged)
        self.block_comboBox.currentIndexChanged.connect(self.blockChanged)
        self.aud_comboBox.currentIndexChanged.connect(self.audChanged)

        self.fileDialogButton.clicked.connect(self.planFileChanged)
        self.todayButton.clicked.connect(self.setDateOnToday)  # кнопка сегодня
        self.calendarWidget.selectionChanged.connect(self.calendarDateChanged)  # отслеживание изменения даты
        self.courseSpinBox.valueChanged.connect(self.updateCourse)
        self.blockValues.clicked.connect(self.blockPlanLabels)
        self.unblockValues.clicked.connect(self.unblockPlanLabels)
        self.clearAllButton.clicked.connect(self.clearPlan)

    def groupChanged(self):
        self.currGroup = self.group_comboBox.currentIndex()
        schedule.newRasp(self.currGroup, self.currProf, self.currBlock, self.currAud)
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
        self.currDate = self.calendarWidget.selectedDate().toPyDate()
        self.updateRasp()
        # print(self.currEdWeekNumber(self.calendarWidget.selectedDate()))
        # print(schedule.weekstr[currDate.weekday()])

    def setDateOnToday(self):
        self.calendarWidget.setSelectedDate(QDate.currentDate())

    def updateRasp(self):
        if self.currEdWeekNumber(self.calendarWidget.selectedDate()) % 2 == 1:
            self.schedule_label.setText(schedule.weekup[self.currDate.weekday()])
        else:
            self.schedule_label.setText(schedule.weekdown[self.currDate.weekday()])
        self.info_label.setText(schedule.info[0] + schedule.legends + schedule.offschedulestr)

    def startFileDialog(self):
        filename, ok = QFileDialog.getOpenFileName(self, "Выбрать файл учебного плана", "", "Таблица (*.xlsx)")
        if filename:
            path = Path(filename)
            self.filename_edit = str(path)

    def setSemester(self):
        if Plan.plan == []:
            fallSemStart = QDate(QDate.currentDate().year(), 9, 1)
            fallSemEnd = QDate(QDate.currentDate().year(), 12, 31)
            springSemStart = QDate(QDate.currentDate().year(), 1, 1)
            springSemEnd = QDate(QDate.currentDate().year(), 5, 31)

            if fallSemStart < QDate.currentDate() < fallSemEnd:
                self.SemStart = fallSemStart
                self.SemEnd = fallSemEnd
            elif springSemStart < QDate.currentDate() < springSemEnd:
                self.SemStart = springSemStart
                self.SemEnd = springSemEnd
            else:
                self.calendarWidget.setMinimumDate(QDate.currentDate())
                self.calendarWidget.setMaximumDate(QDate.currentDate())
        else:
            if QDate.currentDate().month() <= 12 and QDate.currentDate().month() >= 9:
                self.SemStart = QDate(QDate.currentDate().year(), 9, 1)
                self.SemEnd = QDate(QDate.currentDate().year() + 1, 8, 31)
            else:
                self.SemStart = QDate(QDate.currentDate().year() - 1, 9, 1)
                self.SemEnd = QDate(QDate.currentDate().year(), 8, 31)
        self.calendarWidget.setMinimumDate(self.SemStart)
        self.calendarWidget.setMaximumDate(self.SemEnd)

    def setCellFGBlue(self, date):
        style = QTextCharFormat()
        style.setForeground(QColor(99, 189, 235))
        self.calendarWidget.setDateTextFormat(date, style)

    def setCellFGRed(self, date):
        style = QTextCharFormat()
        style.setForeground(QColor(231, 165, 156))
        self.calendarWidget.setDateTextFormat(date, style)

    def setCellsColourRB(self, startDate, endDate):
        while startDate <= endDate:
            if self.currEdWeekNumber(startDate) % 2 == 1:
                self.setCellFGRed(startDate)
            else:
                self.setCellFGBlue(startDate)
            startDate = startDate.addDays(1)

    def planFileChanged(self):
        self.courseSpinBox.setValue(1)
        self.startFileDialog()
        if Plan.getPlanFromFile(self.filename_edit) == -1:
            self.errMessage("Неверный файл!")
            return
        #Plan.getPlanFromFile(self.filename_edit)

        self.updatePlanLabels()
        if Plan.sum[self.currCourse] != 52:
            self.clearCellColors()
            self.errMessage("Неверное количество недель(не 52), если используется файл, проверьте нет ли в плане пустых ячеек.")
        else:
            self.updateWeekColors()
        self.courseSpinBox.setMaximum(len(Plan.planFloat))
        self.setSemester()

    def updateCourse(self):
        self.currCourse = self.courseSpinBox.value() - 1
        self.updatePlanLabels()
        self.updateWeekColors()

    def setCellBGColor(self, date, color):
        style = QTextCharFormat()
        style.setBackground(color)
        # if self.currEdWeekNumber(date) % 2 == 1: #изменение цветов дат по четности
        #    style.setForeground(QColor(231, 165, 156))
        # else:
        #    style.setForeground(QColor(99, 189, 235))
        self.calendarWidget.setDateTextFormat(date, style)

    def clearCellColors(self):
        startDate = self.SemStart
        while startDate <= self.SemEnd:
            self.setCellBGColor(startDate, QColor(255, 255, 255))
            startDate = startDate.addDays(1)

    def updateWeekColors(self):
        self.clearCellColors()
        startDate = self.SemStart
        lastWeek = 1
        for i in range(len(Plan.plan[self.currCourse])):
            while self.currEdWeekNumber(startDate) - lastWeek < int(Plan.planFloat[self.currCourse][i]):
                self.setCellBGColor(startDate, self.colors[i])
                startDate = startDate.addDays(1)

                # if self.currEdWeekNumber(startDate) % 2 == 1:
                #    self.setCellFGRed(startDate)
                # else:
                #    self.setCellFGBlue(startDate)

            lastWeek = self.currEdWeekNumber(startDate)
            # self.currEdWeekNumber(startDate)

    def updatePlanLabels(self):
        for i in range(10):
            self.lineEdits[i].setText("")
            self.dspinBoxes[i].setValue(0)
        if len(Plan.planFloat) != 0:
            for i in range(len(Plan.planFloat[self.currCourse])):
                self.lineEdits[i].setText(Plan.plan[self.currCourse][i])
                self.dspinBoxes[i].setValue(Plan.planFloat[self.currCourse][i])
        # print(Plan.sum[self.currCourse])

    def blockPlanLabels(self):
        newNames = []
        newNums = []
        for i in range(10):
            self.lineEdits[i].setEnabled(False)
            self.dspinBoxes[i].setEnabled(False)
            newNames.append(self.lineEdits[i].text())
            newNums.append(self.dspinBoxes[i].value())
        Plan.setPlan(newNames, newNums, self.currCourse)
        if Plan.sum[self.currCourse] != 52:
            self.errMessage(
                "Неверное количество недель(не 52), если используется файл, проверьте нет ли в плане пустых ячеек.")
        else:
            self.setSemester()
            self.updateWeekColors()
            # self.lineEdits[i].setVisible(False)
            # self.spinBoxes[i].setVisible(False)

    def unblockPlanLabels(self):
        for i in range(10):
            self.lineEdits[i].setEnabled(True)
            self.dspinBoxes[i].setEnabled(True)

    def errMessage(self, message):
        errorMessage = QErrorMessage()
        errorMessage.setWindowTitle("Error")
        errorMessage.setWindowIcon(QtGui.QIcon('error.png'))
        errorMessage.showMessage(message)
        errorMessage.exec()

    def currEdWeekNumber(self, date):
        if date.month() <= 12 and date.month() >= 9:
            return date.weekNumber()[0] - QDate(date.year(), 9, 1).weekNumber()[0] + 1
        else:
            return QDate(date.year() - 1, 12, 31).weekNumber()[0] - QDate(date.year() - 1, 9, 1).weekNumber()[0] + \
                   date.weekNumber()[0] + 1

    def clearPlan(self):
        self.clearCellColors()
        Plan.plan = []
        Plan.planFloat = []
        Plan.sum = []
        self.courseSpinBox.setValue(1)
        self.courseSpinBox.setMaximum(1)
        print(self.currCourse)
        self.updatePlanLabels()
        self.setSemester()
        self.setCellsColourRB(self.SemStart, self.SemEnd)

    # def blockPlanLabelsValues(self):
    #    for i in range(10):
    #        self.lineEdits[i].
    #        self.spinBoxes[i].


# class PlanCellWidget(QWidget):
#    def __init__(self):
#        super().__init__()
#        loadUi("planCellWidget.ui", self)
#        print()

def window():
    app = QApplication(sys.argv)
    app.setApplicationName("SUAI Schedule")
    win = MyWindow()
    win.show()
    sys.exit(app.exec())


Plan = EdPlan()

schedule = getRasp()
window()

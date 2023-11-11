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
        self.currDate = self.calendarScheduleWidget.selectedDate().toPyDate()
        self.setCellsColourRB(self.SemStart, self.SemEnd)
        self.updateRasp()
        self.filename_edit = ""
        self.currCourse = self.courseSpinBox.value() - 1
        self.PlanYearSpinBox.setValue(QDate.currentDate().year())
        self.currentPlanYear = self.currCourse + self.PlanYearSpinBox.value()

        self.lineEdits = [self.lineEdit0, self.lineEdit1, self.lineEdit2, self.lineEdit3, self.lineEdit4,
                          self.lineEdit5, self.lineEdit6, self.lineEdit7, self.lineEdit8, self.lineEdit9]
        self.dspinBoxes = [self.dspinBox0, self.dspinBox1, self.dspinBox2, self.dspinBox3, self.dspinBox4,
                           self.dspinBox5, self.dspinBox6, self.dspinBox7, self.dspinBox8, self.dspinBox9]
        for i in self.dspinBoxes:
            i.valueChanged.connect(self.updateSum)

        self.colors = [QColor(119, 221, 119), QColor(255, 155, 170), QColor(220, 208, 255), QColor(255, 178, 139),
                       QColor(252, 232, 131), QColor(198, 223, 144), QColor(153, 255, 153), QColor(175, 218, 252),
                       QColor(62, 180, 137), QColor(175, 238, 238)]
        self.PlanCalendars = [self.calendarPWidget0, self.calendarPWidget1, self.calendarPWidget2,
                              self.calendarPWidget3,
                              self.calendarPWidget4, self.calendarPWidget5, self.calendarPWidget6,
                              self.calendarPWidget7,
                              self.calendarPWidget8, self.calendarPWidget9, self.calendarPWidget10,
                              self.calendarPWidget11]
        self.StartPlanYearChanged()
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
        self.calendarScheduleWidget.selectionChanged.connect(self.calendarDateChanged)  # отслеживание изменения даты
        self.courseSpinBox.valueChanged.connect(self.updateCourse)
        self.blockValues.clicked.connect(self.blockPlanLabels)
        self.unblockValues.clicked.connect(self.unblockPlanLabels)
        self.clearAllButton.clicked.connect(self.clearPlan)

        self.PlanYearSpinBox.valueChanged.connect(self.StartPlanYearChanged)

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
        self.currDate = self.calendarScheduleWidget.selectedDate().toPyDate()
        self.updateRasp()
        # print(self.currEdWeekNumber(self.calendarScheduleWidget.selectedDate()))
        # print(schedule.weekstr[currDate.weekday()])

    def setDateOnToday(self):
        self.calendarScheduleWidget.setSelectedDate(QDate.currentDate())

    def updateRasp(self):
        if self.currEdWeekNumber(self.calendarScheduleWidget.selectedDate()) % 2 == 1:
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
            self.calendarScheduleWidget.setMinimumDate(QDate.currentDate())
            self.calendarScheduleWidget.setMaximumDate(QDate.currentDate())

        self.calendarScheduleWidget.setMinimumDate(self.SemStart)
        self.calendarScheduleWidget.setMaximumDate(self.SemEnd)

    def setCellFGBlue(self, date):
        style = QTextCharFormat()
        style.setForeground(QColor(99, 189, 235))
        self.calendarScheduleWidget.setDateTextFormat(date, style)

    def setCellFGRed(self, date):
        style = QTextCharFormat()
        style.setForeground(QColor(231, 165, 156))
        self.calendarScheduleWidget.setDateTextFormat(date, style)

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
        # Plan.getPlanFromFile(self.filename_edit)

        self.updatePlanLabels()
        if Plan.sum[self.currCourse] != 52:
            self.clearCellColors()
            self.errMessage(
                "Неверное количество недель(не 52), если используется файл, проверьте нет ли в плане пустых ячеек.")

        self.updateWeekColors()
        self.courseSpinBox.setMaximum(len(Plan.planFloat))

    def updateCourse(self):
        self.currCourse = self.courseSpinBox.value() - 1
        self.currentPlanYear = self.currCourse + self.PlanYearSpinBox.value()
        self.PlanYearLabel.setText(f"{self.currentPlanYear} - {self.currentPlanYear + 1}")
        self.setPlanCalendarsInterval(self.currentPlanYear)
        self.updatePlanLabels()
        self.clearCellColors()
        self.updateWeekColors()

    def setCellBGColor(self, date, color, calendar):
        style = QTextCharFormat()
        style.setBackground(color)
        calendar.setDateTextFormat(date, style)

    def clearCellColors(self):
        startDate = QDate(self.currentPlanYear, 9, 1)
        while startDate <= QDate(self.currentPlanYear + 1, 9, 1):
            self.setCellBGColor(startDate, QColor(255, 255, 255), self.PlanCalendars[(startDate.month() + 3) % 12])
            if startDate.day() == 1:
                self.PlanCalendars[(startDate.month() + 3) % 12].setStyleSheet(
                    "#qt_calendar_calendarview::item:selected {background-color: #ffffff}")
            startDate = startDate.addDays(1)

    # def updateWeekColors(self): #старая
    #    if Plan.plan == []:
    #        return
    #    self.clearCellColors()
    #    startDate = QDate(self.currentPlanYear, 9, 1)
    #    lastWeek = 1
    #    for i in range(len(Plan.plan[self.currCourse])):
    #        while 0 <= self.currEdWeekNumber(startDate) - lastWeek < int(Plan.planFloat[self.currCourse][i]):
    #            self.setCellBGColor(startDate, self.colors[i], self.PlanCalendars[(startDate.month() + 3) % 12])
    #            startDate = startDate.addDays(1)
    #        lastWeek = self.currEdWeekNumber(startDate)

    def updateWeekColors(self):
        if Plan.plan == []:
            return
        self.clearCellColors()
        startDate = QDate(self.currentPlanYear, 9, 1)
        tempPlan = Plan.planFloat[self.currCourse].copy()
        # стиль выделения для первого календаря
        self.PlanCalendars[0].setStyleSheet(
            f"#qt_calendar_calendarview::item:selected{{	background-color: rgb({self.colors[0].red()},{self.colors[0].green()},{self.colors[0].blue()});}}")
        while self.currEdWeekNumber(startDate) == 1:
            self.setCellBGColor(startDate, self.colors[0], self.PlanCalendars[(startDate.month() + 3) % 12])
            startDate = startDate.addDays(1)
        tempPlan[0] -= 1
        for i in range(len(tempPlan)):
            for j in range(int(tempPlan[i] * 7)):
                self.setCellBGColor(startDate, self.colors[i], self.PlanCalendars[(startDate.month() + 3) % 12])
                if startDate.day() == 1:  # установка цвета выбранной даты
                    self.PlanCalendars[(startDate.month() + 3) % 12].setStyleSheet(
                        f"#qt_calendar_calendarview::item:selected{{	background-color: rgb({self.colors[i].red()},{self.colors[i].green()},{self.colors[i].blue()});}}")
                startDate = startDate.addDays(1)
            if startDate.dayOfWeek() == 7:
                self.setCellBGColor(startDate, self.colors[i], self.PlanCalendars[(startDate.month() + 3) % 12])
                if startDate.day() == 1:
                    self.PlanCalendars[(startDate.month() + 3) % 12].setStyleSheet(
                        f"#qt_calendar_calendarview::item:selected{{	background-color: rgb({self.colors[i].red()},{self.colors[i].green()},{self.colors[i].blue()});}}")
                startDate = startDate.addDays(1)

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
            newNames.append(self.lineEdits[i].text())
            newNums.append(self.dspinBoxes[i].value())
        Plan.setPlan(newNames, newNums, self.currCourse)

        if Plan.sum[self.currCourse] != 52:
            self.errMessage(
                "Неверное количество недель(не 52), если используется файл, проверьте нет ли в плане пустых ячеек.")
        else:
            for i in range(10):
                self.lineEdits[i].setEnabled(False)
                self.dspinBoxes[i].setEnabled(False)

        self.updateWeekColors()

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
        if date.weekNumber()[0] >= QDate(date.year(), 9, 1).weekNumber()[0]:
            if date.weekNumber()[0] != 1:
                return date.weekNumber()[0] - QDate(date.year(), 9, 1).weekNumber()[0] + 1
            else:
                prevdate = date.addDays(-7)
                return prevdate.weekNumber()[0] - QDate(date.year(), 9, 1).weekNumber()[0] + 2
        else:
            if QDate(date.year() - 1, 12, 31).weekNumber()[0] != 1:
                return self.currEdWeekNumber(QDate(date.year() - 1, 12, 31)) + date.weekNumber()[0]
            else:
                return self.currEdWeekNumber(QDate(date.year() - 1, 12, 31)) + date.weekNumber()[0] - 1

    def clearPlan(self):
        self.clearCellColors()
        Plan.plan = []
        Plan.planFloat = []
        Plan.sum = []
        self.courseSpinBox.setValue(1)
        self.courseSpinBox.setMaximum(1)
        self.updatePlanLabels()

    def setPlanCalendarsInterval(self, year):
        for i in range(12):
            if i < 3:
                self.PlanCalendars[i].setMinimumDate(QDate(year, 9 + i, 1))
                self.PlanCalendars[i].setMaximumDate(QDate(year, 10 + i, 1).addDays(-1))
                self.PlanCalendars[i].setSelectedDate(QDate(year, 9 + i, 1))
            elif i == 3:
                self.PlanCalendars[i].setMinimumDate(QDate(year, 12, 1))
                self.PlanCalendars[i].setMaximumDate(QDate(year + 1, 1, 1).addDays(-1))
                self.PlanCalendars[i].setSelectedDate(QDate(year, 12, 1))
            else:
                self.PlanCalendars[i].setMinimumDate(QDate(year + 1, (9 + i) % 12, 1))
                self.PlanCalendars[i].setMaximumDate(QDate(year + 1, (10 + i) % 12, 1).addDays(-1))
                self.PlanCalendars[i].setSelectedDate(QDate(year + 1, (9 + i) % 12, 1))

    def StartPlanYearChanged(self):
        self.currentPlanYear = self.currCourse + self.PlanYearSpinBox.value()
        self.PlanYearLabel.setText(f"{self.currentPlanYear} - {self.currentPlanYear + 1}")
        self.setPlanCalendarsInterval(self.currentPlanYear)
        self.clearCellColors()
        self.updateWeekColors()

    def updateSum(self):
        weeksSum = 0
        for i in self.dspinBoxes:
            weeksSum += i.value()
        self.weekSumLabel.setText(f"Текущая сумма учебных недель: {weeksSum}")


def window():
    app = QApplication(sys.argv)
    app.setApplicationName("SUAI Schedule")
    win = MyWindow()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    Plan = EdPlan()
    schedule = getRasp()
    window()

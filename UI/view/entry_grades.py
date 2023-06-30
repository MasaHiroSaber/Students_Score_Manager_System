from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QFrame, QGridLayout, QLabel
import pymysql
from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QFrame, QGridLayout
from qfluentwidgets import TableWidget, ComboBox, PrimaryPushButton, InfoBar, InfoBarPosition, PushButton, CheckBox, \
    LineEdit
from PyQt5 import QtCore, QtWidgets
from UI.global_var import globalVal
from .gallery_interface import GalleryInterface
from ..common.style_sheet import StyleSheet
from UI.connectDataBase import db_select, db_update
from PyQt5.QtCore import Qt

global status


class EntryGrades(GalleryInterface):
    current_instance = None

    def __init__(self, parent=None):
        super().__init__(
            title='成绩录入',
            subtitle='此功能可以录入学生课程成绩',
            parent=parent
        )
        EntryGrades.current_instance = self

        self.addExampleCard(
            title=self.tr('课程成绩录入'),
            widget=TableFrame(self)
        )

    @classmethod
    def infoBar_success(cls, success_info):
        InfoBar.success(
            title='成功!',
            content=success_info,
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP_RIGHT,
            duration=2000,
            parent=cls.current_instance
        )

    @classmethod
    def infoBar_error(cls, error_info):
        InfoBar.error(
            title='失败!',
            content=error_info,
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP_RIGHT,
            duration=2000,
            parent=cls.current_instance
        )


class Frame(QFrame):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.gBoxLayout = QGridLayout(self)

        # self.hBoxLayout = QHBoxLayout(self)
        self.gBoxLayout.setContentsMargins(0, 8, 0, 0)
        self.setObjectName('frame')
        StyleSheet.VIEW_INTERFACE.apply(self)

    def addWidget(self, widget, row, col, rowspan, colspan):
        self.gBoxLayout.addWidget(widget, row, col, rowspan, colspan)

    def addItem(self, item, row, col, rowspan, colspan):
        self.gBoxLayout.addItem(item, row, col, rowspan, colspan)


class TableFrame(Frame):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.cno = None
        self.term = None
        self.cname = None
        sql1 = f"SELECT DISTINCT cname FROM tea_course_info WHERE tno = '{globalVal.global_list[0]}'"
        course_info = db_select(sql1)

        self.spacer_widget = QWidget(self)
        self.spacer_widget.setFixedSize(10, 20)
        self.addWidget(self.spacer_widget, 0, 0, 1, 1)

        course_list = []
        for i in course_info:
            course_list.append(i[0])
        self.comboBox_1 = ComboBox(self)
        self.comboBox_1.addItems(course_list)
        self.comboBox_1.setCurrentIndex(0)
        self.comboBox_1.setMaximumWidth(150)
        self.addWidget(self.comboBox_1, 0, 1, 1, 1)

        self.button_1 = PrimaryPushButton(self.tr('选择课程'), self)
        self.button_1.setMaximumWidth(80)
        self.addWidget(self.button_1, 0, 2, 1, 1)

        self.comboBox_2 = ComboBox(self)
        self.comboBox_2.setCurrentIndex(0)
        self.comboBox_2.setMaximumWidth(150)
        self.addWidget(self.comboBox_2, 0, 3, 1, 1)

        self.button_2 = PrimaryPushButton(self.tr('选择学期'), self)
        self.button_2.setMaximumWidth(80)
        self.addWidget(self.button_2, 0, 4, 1, 1)

        self.spacer_widget = QWidget(self)
        self.spacer_widget.setFixedSize(40, 20)
        self.addWidget(self.spacer_widget, 0, 5, 1, 1)

        self.button_3 = PrimaryPushButton(self.tr('查询'), self)
        self.button_3.setMaximumWidth(60)
        self.addWidget(self.button_3, 0, 6, 1, 1)

        self.CheckBox = CheckBox(self.tr('只显示未录入成绩学生'), self)
        self.addWidget(self.CheckBox, 0, 7, 1, 1)

        self.spacer_widget_2 = QWidget(self)
        self.spacer_widget_2.setFixedSize(10, 10)
        self.addWidget(self.spacer_widget_2, 1, 0, 1, 1)

        self.comboBox_3 = ComboBox(self)
        self.comboBox_3.setCurrentIndex(0)
        self.comboBox_3.setMaximumWidth(200)
        self.addWidget(self.comboBox_3, 2, 1, 1, 1)

        self.lineEdit = LineEdit(self)
        self.lineEdit.setPlaceholderText('请输入成绩')
        self.lineEdit.setMaximumWidth(100)
        self.addWidget(self.lineEdit, 2, 2, 1, 1)

        self.button_4 = PrimaryPushButton(self.tr('录入成绩'), self)
        self.button_4.setMaximumWidth(80)
        self.addWidget(self.button_4, 2, 3, 1, 1)

        self.button_1.clicked.connect(self.get_course)
        self.button_1.clicked.connect(self.course_term)
        self.button_2.clicked.connect(self.get_term)
        self.button_3.clicked.connect(self.stu_table)
        self.button_4.clicked.connect(self.entry_grade)

        # self.button = PrimaryPushButton(self.tr('查询学生列表'), self)
        # self.button.setMaximumWidth(100)
        # self.addWidget(self.button, 0, 2, 1, 1)

        # self.button.clicked.connect(self.query)

        sql2 = f"SELECT * FROM stu_course"
        stuInfos = db_select(sql2)

        self.table = TableWidget(self)
        self.addWidget(self.table, 3, 0, 1, 8)

        self.table.verticalHeader().hide()
        self.table.setColumnCount(5)
        self.table.setEditTriggers(self.table.NoEditTriggers)
        self.table.setSortingEnabled(True)

        self.table.setRowCount(len(stuInfos))
        self.table.setHorizontalHeaderLabels([
            self.tr('学号'), self.tr('姓名'),
            self.tr('课程名'), self.tr('成绩'),
            self.tr('学期')
        ])

        self.setFixedSize(860, 400)
        self.table.resizeColumnsToContents()
        self.table.setColumnWidth(0, 150)
        self.table.setColumnWidth(1, 100)
        self.table.setColumnWidth(2, 300)
        self.table.setColumnWidth(3, 150)
        self.table.setColumnWidth(4, 150)

    def stu_table(self):
        global status
        try:
            self.table.clearContents()
            if self.CheckBox.isChecked():
                sql3 = f"SELECT * FROM stu_course WHERE cno = '{self.cno}' AND term = '{self.term}' AND score IS NULL"

            else:
                sql3 = f"SELECT * FROM stu_course WHERE cno = '{self.cno}' AND term = '{self.term}'"
            Stu_query = db_select(sql3)

            Stu_list_table = []
            Stu_list_combo = []

            for i in Stu_query:
                insert_list = [i[0], i[1], i[3], i[5], i[7]]
                insert_list_combo = str(i[0]) + ' ' + str(i[1])
                Stu_list_table.append(insert_list)
                Stu_list_combo.append(insert_list_combo)

            self.comboBox_3.clear()
            self.comboBox_3.addItems(Stu_list_combo)

            if len(Stu_list_table) == 0:
                raise Exception

            for i, Stu in enumerate(Stu_list_table):
                for j in range(5):
                    self.table.setItem(i, j, QTableWidgetItem(str(Stu[j])))

            self.setFixedSize(860, 400)
            self.table.resizeColumnsToContents()
            self.table.setColumnWidth(0, 150)
            self.table.setColumnWidth(1, 100)
            self.table.setColumnWidth(2, 300)
            self.table.setColumnWidth(3, 150)
            self.table.setColumnWidth(4, 150)

            EntryGrades.infoBar_success('操作成功')

        except:
            EntryGrades.infoBar_error('操作失败')

    def get_course(self):
        self.cname = self.comboBox_1.currentText()
        sql5 = f"SELECT DISTINCT cno FROM courses WHERE cname = '{self.cname}' AND ctno = '{globalVal.global_list[0]}'"
        cno_info = db_select(sql5)
        self.cno = cno_info[0][0]

    def course_term(self):
        sql4 = f"SELECT term FROM tea_course_info WHERE tno = '{globalVal.global_list[0]}' AND cname = '{self.cname}'"
        term_info = db_select(sql4)

        term_list = []
        for i in term_info:
            term_list.append(i[0])

        print(term_list)

        self.comboBox_2.clear()
        self.comboBox_2.addItems(sorted(term_list))

    def get_term(self):
        self.term = self.comboBox_2.currentText()

    def entry_grade(self):
        sno = self.comboBox_3.currentText().split(' ')[0]
        score = self.lineEdit.text().split()[0]

        if eval(score) >= 0 and eval(score) <= 100:
            try:

                sql6 = f"UPDATE sc SET score = '{score}' WHERE sno = '{sno}' AND cno = '{self.cno}' AND term = '{self.term}'"
                db_update(sql6)

                self.stu_table()

            except:
                EntryGrades.infoBar_error('操作失败')

        else:
            EntryGrades.infoBar_error('成绩应在0-100之间')

from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QFrame, QGridLayout, QLabel
import pymysql
from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QFrame, QGridLayout
from qfluentwidgets import TableWidget, ComboBox, PrimaryPushButton, InfoBar, InfoBarPosition, PushButton
from PyQt5 import QtCore, QtWidgets
from UI.global_var import globalVal
from .gallery_interface import GalleryInterface
from ..common.style_sheet import StyleSheet
from UI.connectDataBase import db_select
from PyQt5.QtCore import Qt

global status


class InfoScore(GalleryInterface):
    current_instance = None

    def __init__(self, parent=None):
        super().__init__(
            title='成绩查询',
            subtitle='此功能可以查询您的成绩',
            parent=parent
        )
        InfoScore.current_instance = self

        self.addExampleCard(
            title=self.tr('学期成绩查询'),
            widget=TableFrame(self)
        )

    @classmethod
    def infoBar_success(cls):
        InfoBar.success(
            title='√',
            content="查询成功",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP_RIGHT,
            duration=2000,
            parent=cls.current_instance
        )

    @classmethod
    def infoBar_error(cls):
        InfoBar.error(
            title='×',
            content="查询失败",
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

        sql1 = f"SELECT DISTINCT term FROM stu_course WHERE sno = '{globalVal.global_list[0]}'"
        term_info = db_select(sql1)

        self.spacer_widget = QWidget(self)
        self.spacer_widget.setFixedSize(10, 20)
        self.addWidget(self.spacer_widget, 0, 0, 1, 1)

        term_list = []
        for i in term_info:
            term_list.append(i[0])
        self.comboBox = ComboBox(self)
        self.comboBox.addItems(term_list)
        self.comboBox.setCurrentIndex(0)
        self.comboBox.setMaximumWidth(150)
        self.addWidget(self.comboBox, 0, 1, 1, 1)

        self.button = PrimaryPushButton(self.tr('查询'), self)
        self.button.setMaximumWidth(100)
        self.addWidget(self.button, 0, 2, 1, 1)

        self.button.clicked.connect(self.query)
        self.button.clicked.connect(self.credit_stu)
        self.button.clicked.connect(self.avg_stu)

        gl_username = globalVal.global_list[0]
        sql2 = f"SELECT * FROM stu_course WHERE sno = '{gl_username}' AND term = '{self.comboBox.currentText()}'"
        classInfos = db_select(sql2)

        self.label_1 = QtWidgets.QLabel(self)
        self.label_1.setText('            此学期总学分:')
        self.addWidget(self.label_1, 0, 5, 1, 1)

        self.label_2 = QtWidgets.QLabel(self)
        self.label_2.setText('        此学期平均成绩:')
        self.addWidget(self.label_2, 0, 3, 1, 1)


        self.button_credit = PushButton(self)
        self.button_credit.setMaximumWidth(60)
        self.addWidget(self.button_credit, 0, 6, 1, 1)

        self.button_gpa = PushButton(self)
        self.button_gpa.setMaximumWidth(60)
        self.addWidget(self.button_gpa, 0, 4, 1, 1)

        self.table = TableWidget(self)
        self.addWidget(self.table, 1, 0, 1, 8)

        self.table.verticalHeader().hide()
        self.table.setColumnCount(8)
        self.table.setEditTriggers(self.table.NoEditTriggers)
        self.table.setSortingEnabled(True)

        self.table.setRowCount(len(classInfos) * 5)
        self.table.setHorizontalHeaderLabels([
            self.tr('学号'), self.tr('姓名'), self.tr('课程号'),
            self.tr('课程名'), self.tr('教师'), self.tr('成绩'),
            self.tr('学分'), self.tr('学期')
        ])

        self.setFixedSize(860, 400)
        self.table.resizeColumnsToContents()
        self.table.setColumnWidth(3, 300)


    def credit_stu(self):
        try:
            gl_username = globalVal.global_list[0]
            sql2 = f"SELECT SUM(ccredit) FROM stu_course WHERE sno = '{gl_username}' AND term = '{self.comboBox.currentText()}'"
            credit_query = db_select(sql2)
            self.button_credit.setText(str(credit_query[0][0]))

        except:
            pass

    def avg_stu(self):
        try:
            gl_username = globalVal.global_list[0]
            sql3 = f"SELECT AVG(score) FROM stu_course WHERE sno = '{gl_username}' AND term = '{self.comboBox.currentText()}'"
            avg_query = db_select(sql3)
            self.button_gpa.setText(str(avg_query[0][0]))

        except:
            pass


    def query(self):
        global status
        try:
            gl_username = globalVal.global_list[0]
            sql2 = f"SELECT * FROM stu_course WHERE sno = '{gl_username}' AND term = '{self.comboBox.currentText()}'"
            classInfos_query = db_select(sql2)

            if len(classInfos_query) == 0:
                raise Exception

            for i, classInfo in enumerate(classInfos_query):
                for j in range(8):
                    self.table.setItem(i, j, QTableWidgetItem(str(classInfo[j])))

            self.setFixedSize(860, 400)
            self.table.resizeColumnsToContents()
            self.table.setColumnWidth(3, 300)
            InfoScore.infoBar_success()

        except:
            InfoScore.infoBar_error()

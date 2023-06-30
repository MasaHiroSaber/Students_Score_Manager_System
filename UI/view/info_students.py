import pymysql
from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QFrame, QHBoxLayout
from qfluentwidgets import PushButton, FlowLayout, TableWidget
from UI.connectDataBase import db_select
from UI.global_var import globalVal
from .gallery_interface import GalleryInterface
from ..common.style_sheet import StyleSheet


class InfoStudents(GalleryInterface):

    def __init__(self, parent=None):
        super().__init__(
            title='基本信息',
            subtitle='此功能可以查询您的基本信息',
            parent=parent
        )

        self.addExampleCard(
            self.tr('基本信息'),
            self.createWidget(),
            stretch=1
        )

        self.addExampleCard(
            self.tr('选课情况'),
            widget=TableFrame(self)
        )

    def createWidget(self, animation=False):
        gl_username = globalVal.global_list[0]
        sql1 = f"select * from students where sno = '{gl_username}'"
        stu_info = db_select(sql1)
        sql2 = f"select * from department where dno = '{stu_info[0][5]}'"
        department_info = db_select(sql2)
        sql3 = f"select SUM(ccredit) from stu_course where sno = '{gl_username}'"
        credit_info = db_select(sql3)
        sql4 = f"select AVG(score) from stu_course where sno = '{gl_username}'"
        avg_info = db_select(sql4)
        texts = [
            self.tr('学号:' + str(stu_info[0][0])), self.tr('姓名:' + stu_info[0][1]),
            self.tr('年龄:' + str(stu_info[0][2])), self.tr('性别:' + stu_info[0][3]),
            self.tr('班级:' + stu_info[0][4]), self.tr('学院:' + department_info[0][1]),
            self.tr('已修学分:' + str(credit_info[0][0])), self.tr('平均成绩:' + str(avg_info[0][0]))
        ]

        widget = QWidget()
        layout = FlowLayout(widget, animation)

        layout.setContentsMargins(0, 0, 0, 0)
        layout.setVerticalSpacing(20)
        layout.setHorizontalSpacing(10)

        for text in texts:
            layout.addWidget(PushButton(text))
        return widget


class Frame(QFrame):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.hBoxLayout = QHBoxLayout(self)
        self.hBoxLayout.setContentsMargins(0, 8, 0, 0)

        self.setObjectName('frame')
        StyleSheet.VIEW_INTERFACE.apply(self)

    def addWidget(self, widget):
        self.hBoxLayout.addWidget(widget)


class TableFrame(Frame):

    def __init__(self, parent=None):
        super().__init__(parent)

        gl_username = globalVal.global_list[0]
        sql3 = f"select * from stu_course where sno = '{gl_username}'"
        classInfos = db_select(sql3)


        self.table = TableWidget(self)
        self.addWidget(self.table)

        self.table.verticalHeader().hide()
        self.table.setColumnCount(8)
        self.table.setEditTriggers(self.table.NoEditTriggers)
        self.table.setSortingEnabled(True)

        self.table.setRowCount(len(classInfos) * 2)
        self.table.setHorizontalHeaderLabels([
            self.tr('学号'), self.tr('姓名'), self.tr('课程号'),
            self.tr('课程名'), self.tr('讲师'), self.tr('成绩'),
            self.tr('学分'), self.tr('学期')
        ])

        for i, classInfo in enumerate(classInfos):
            for j in range(8):
                self.table.setItem(i, j, QTableWidgetItem(str(classInfo[j])))

        self.setFixedSize(860, 400)
        self.table.resizeColumnsToContents()
        self.table.setColumnWidth(3, 300)

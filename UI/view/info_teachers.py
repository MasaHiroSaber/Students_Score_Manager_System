import pymysql
from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QFrame, QHBoxLayout
from qfluentwidgets import PushButton, FlowLayout, TableWidget
from UI.connectDataBase import db_select
from UI.global_var import globalVal
from .gallery_interface import GalleryInterface
from ..common.style_sheet import StyleSheet


class InfoTeachers(GalleryInterface):

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
            self.tr('授课概况'),
            widget=TableFrame(self)
        )

    def createWidget(self, animation=False):
        gl_username = globalVal.global_list[0]
        sql1 = f"select * from teachers where tno = '{gl_username}'"
        tea_info = db_select(sql1)
        sql2 = f"select * from department where dno = '{tea_info[0][4]}'"
        department_info = db_select(sql2)

        texts = [
            self.tr('工号:' + str(tea_info[0][0])), self.tr('姓名:' + tea_info[0][1]),
            self.tr('年龄:' + str(tea_info[0][2])), self.tr('性别:' + tea_info[0][3]),
            self.tr('学院:' + department_info[0][1])
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
        sql3 = f"select * from tea_course_info where tno = '{gl_username}'"
        classInfos = db_select(sql3)
        classInfos_list = []
        for i in classInfos:
            insert_list = [i[2], i[3], i[4], i[5], i[6], i[7]]
            classInfos_list.append(insert_list)



        self.table = TableWidget(self)
        self.addWidget(self.table)

        self.table.verticalHeader().hide()
        self.table.setColumnCount(6)
        self.table.setEditTriggers(self.table.NoEditTriggers)
        self.table.setSortingEnabled(True)

        self.table.setRowCount(len(classInfos_list) * 2)
        self.table.setHorizontalHeaderLabels([
            self.tr('课程号'), self.tr('课程名'), self.tr('课时'),
            self.tr('学分'),self.tr('学生人数'), self.tr('学期')
        ])

        for i, classInfos_list in enumerate(classInfos_list):
            for j in range(6):
                self.table.setItem(i, j, QTableWidgetItem(str(classInfos_list[j])))

        self.setFixedSize(860, 400)
        self.table.resizeColumnsToContents()
        self.table.setColumnWidth(0, 100)
        self.table.setColumnWidth(1, 300)
        self.table.setColumnWidth(2, 100)
        self.table.setColumnWidth(3, 100)
        self.table.setColumnWidth(4, 100)
        self.table.setColumnWidth(5, 150)

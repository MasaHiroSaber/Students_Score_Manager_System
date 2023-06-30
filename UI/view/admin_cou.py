# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QCompleter, QTableWidgetItem
from PyQt5.QtWidgets import QWidget, QFrame, QGridLayout
from qfluentwidgets import ComboBox, InfoBar, InfoBarPosition, SearchLineEdit, PrimaryPushButton, TableWidget, LineEdit, \
    MessageBox

from UI.connectDataBase import db_select, db_update, db_insert, db_delete
from .gallery_interface import GalleryInterface
from ..common.style_sheet import StyleSheet


class AdminCou(GalleryInterface):
    current_instance = None

    def __init__(self, parent=None):
        super().__init__(
            title='课程信息操作',
            subtitle='',
            parent=parent
        )
        AdminCou.current_instance = self

        self.addExampleCard(
            title=self.tr('课程信息查询'),
            widget=SearchCourseFrame(self)
        )

        self.addExampleCard(
            title=self.tr('课程信息修改'),
            widget=EditCourseFrame(self)
        )

        self.addExampleCard(
            title=self.tr('课程信息添加'),
            widget=AddCourseFrame(self)
        )

        self.addExampleCard(
            title=self.tr('课程信息删除'),
            widget=DelTeaFrame(self)
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
        self.gBoxLayout.setContentsMargins(0, 8, 0, 0)
        self.setObjectName('frame')
        StyleSheet.VIEW_INTERFACE.apply(self)

    def addWidget(self, widget, row, col, rowspan, colspan):
        self.gBoxLayout.addWidget(widget, row, col, rowspan, colspan)

    def addItem(self, item, row, col, rowspan, colspan):
        self.gBoxLayout.addItem(item, row, col, rowspan, colspan)


class SearchCourseFrame(Frame):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.cno = None
        self.ctno = None
        self.tname = None
        self.cname = None
        self.chours = None
        self.ccredit = None

        sql1 = "SELECT courses.cno, courses.ctno, teachers.tname, courses.cname, courses.chours, courses.ccredit " \
               "FROM courses INNER JOIN teachers ON courses.ctno = teachers.tno"
        self.all_courses_info = db_select(sql1)

        self.cno_list = self.listCreate(self.all_courses_info, 0)
        self.ctno_list = self.listCreate(self.all_courses_info, 1)
        self.tname_list = sorted(set(self.listCreate(self.all_courses_info, 2)))
        self.cname_list = set(self.listCreate(self.all_courses_info, 3))
        self.chours_list = sorted(set(self.listCreate(self.all_courses_info, 4)))
        self.ccredit_list = sorted(set(self.listCreate(self.all_courses_info, 5)))

        # self.spacer_widget = QWidget(self)
        # self.spacer_widget.setFixedSize(10, 20)
        # self.addWidget(self.spacer_widget, 0, 0, 1, 1)

        self.SearchLineEdit_cno = SearchLineEdit(self)
        self.SearchLineEdit_cno.setPlaceholderText('请输入课程号')
        self.SearchLineEdit_cno.setClearButtonEnabled(True)
        self.SearchLineEdit_cno.setFixedWidth(200)
        self.completer_tno = QCompleter(self.cno_list, self.SearchLineEdit_cno)
        self.completer_tno.setCaseSensitivity(Qt.CaseInsensitive)
        self.SearchLineEdit_cno.setCompleter(self.completer_tno)
        self.addWidget(self.SearchLineEdit_cno, 0, 0, 1, 1)

        self.SearchLineEdit_ctno = SearchLineEdit(self)
        self.SearchLineEdit_ctno.setPlaceholderText('请输入教师号')
        self.SearchLineEdit_ctno.setClearButtonEnabled(True)
        self.SearchLineEdit_ctno.setFixedWidth(200)
        self.completer_ctno = QCompleter(self.ctno_list, self.SearchLineEdit_ctno)
        self.completer_ctno.setCaseSensitivity(Qt.CaseInsensitive)
        self.SearchLineEdit_ctno.setCompleter(self.completer_ctno)
        self.addWidget(self.SearchLineEdit_ctno, 0, 1, 1, 2)

        self.SearchLineEdit_tname = SearchLineEdit(self)
        self.SearchLineEdit_tname.setPlaceholderText('请输入教师姓名')
        self.SearchLineEdit_tname.setClearButtonEnabled(True)
        self.SearchLineEdit_tname.setFixedWidth(200)
        self.completer_tname = QCompleter(self.tname_list, self.SearchLineEdit_tname)
        self.completer_tname.setCaseSensitivity(Qt.CaseInsensitive)
        self.SearchLineEdit_tname.setCompleter(self.completer_tname)
        self.addWidget(self.SearchLineEdit_tname, 0, 3, 1, 2)

        self.SearchLineEdit_cname = SearchLineEdit(self)
        self.SearchLineEdit_cname.setPlaceholderText('请输入课程名')
        self.SearchLineEdit_cname.setClearButtonEnabled(True)
        self.SearchLineEdit_cname.setFixedWidth(200)
        self.completer_cname = QCompleter(self.cname_list, self.SearchLineEdit_cname)
        self.completer_cname.setCaseSensitivity(Qt.CaseInsensitive)
        self.SearchLineEdit_cname.setCompleter(self.completer_cname)
        self.addWidget(self.SearchLineEdit_cname, 1, 0, 1, 2)

        self.comboBox_chours = ComboBox(self)
        self.comboBox_chours.addItems(self.chours_list)
        self.comboBox_chours.addItems(["全部"])
        self.comboBox_chours.setCurrentIndex(0)
        self.comboBox_chours.setMaximumWidth(90)
        self.addWidget(self.comboBox_chours, 1, 1, 1, 1)

        self.comboBox_credit = ComboBox(self)
        self.comboBox_credit.addItems(self.ccredit_list)
        self.comboBox_credit.addItems(["全部"])
        self.comboBox_credit.setCurrentIndex(0)
        self.comboBox_credit.setMaximumWidth(90)
        self.addWidget(self.comboBox_credit, 1, 2, 1, 1)

        self.SearchButton = PrimaryPushButton(self)
        self.SearchButton.setText('查询')
        self.SearchButton.setFixedSize(80, 30)
        self.addWidget(self.SearchButton, 1, 6, 1, 1)

        self.table = TableWidget(self)
        self.addWidget(self.table, 2, 0, 1, 8)

        self.table.verticalHeader().hide()
        self.table.setColumnCount(6)
        self.table.setEditTriggers(self.table.NoEditTriggers)
        self.table.setSortingEnabled(True)

        self.table.setRowCount(len(self.all_courses_info))
        self.table.setHorizontalHeaderLabels([
            self.tr('课程号'), self.tr('课程教师工号'), self.tr('课程教师姓名'),
            self.tr('课程名'), self.tr('课时'), self.tr('学分')
        ])

        for i, every_courses in enumerate(self.all_courses_info):
            for j in range(6):
                self.table.setItem(i, j, QTableWidgetItem(str(every_courses[j])))

        self.SearchButton.clicked.connect(self.course_search)

        self.setFixedSize(860, 400)
        self.table.resizeColumnsToContents()
        self.table.setColumnWidth(0, 100)
        self.table.setColumnWidth(1, 160)
        self.table.setColumnWidth(2, 160)
        self.table.setColumnWidth(3, 250)
        self.table.setColumnWidth(4, 100)
        self.table.setColumnWidth(5, 100)

    def course_search(self):
        try:
            self.cno = self.SearchLineEdit_cno.text()
            self.ctno = self.SearchLineEdit_ctno.text()
            self.tname = self.SearchLineEdit_tname.text()
            self.cname = self.SearchLineEdit_cname.text()
            self.chours = self.comboBox_chours.currentText()
            self.ccredit = self.comboBox_credit.currentText()

            sql2 = "SELECT courses.cno, courses.ctno, teachers.tname, courses.cname, courses.chours, courses.ccredit " \
                   "FROM courses INNER JOIN teachers ON courses.ctno = teachers.tno"

            if self.cno != '':
                sql2 += " WHERE courses.cno = '%s'" % self.cno

            if self.ctno != '':
                if self.cno != '':
                    sql2 += " AND courses.ctno = '%s'" % self.ctno
                else:
                    sql2 += " WHERE courses.ctno = '%s'" % self.ctno

            if self.tname != '':
                if self.cno != '' or self.ctno != '':
                    sql2 += " AND teachers.tname = '%s'" % self.tname
                else:
                    sql2 += " WHERE teachers.tname = '%s'" % self.tname

            if self.cname != '':
                if self.cno != '' or self.ctno != '' or self.tname != '':
                    sql2 += " AND courses.cname = '%s'" % self.cname
                else:
                    sql2 += " WHERE courses.cname = '%s'" % self.cname

            if self.chours != '全部':
                if self.cno != '' or self.ctno != '' or self.tname != '' or self.cname != '':
                    sql2 += " AND courses.chours = '%s'" % self.chours
                else:
                    sql2 += " WHERE courses.chours = '%s'" % self.chours

            if self.ccredit != '全部':
                if self.cno != '' or self.ctno != '' or self.tname != '' or self.cname != '' or self.chours != '全部':
                    sql2 += " AND courses.ccredit = '%s'" % self.ccredit
                else:
                    sql2 += " WHERE courses.ccredit = '%s'" % self.ccredit

            sql2 += " ORDER BY courses.cno"

            print(sql2)

            coursesInfos_query = db_select(sql2)

            if len(coursesInfos_query) == 0:
                raise Exception

            self.table.clearContents()
            for i, courseInfo in enumerate(coursesInfos_query):
                for j in range(6):
                    self.table.setItem(i, j, QTableWidgetItem(str(courseInfo[j])))

            self.setFixedSize(860, 400)
            self.table.resizeColumnsToContents()
            self.table.setColumnWidth(0, 100)
            self.table.setColumnWidth(1, 160)
            self.table.setColumnWidth(2, 160)
            self.table.setColumnWidth(3, 250)
            self.table.setColumnWidth(4, 100)
            self.table.setColumnWidth(5, 100)
            AdminCou.infoBar_success('查询成功！')

        except:
            AdminCou.infoBar_error('查询失败！')

    def listCreate(self, input_list, index):
        output_list = []
        for i in input_list:
            output_list.append(str(i[index]))
        return output_list


class EditCourseFrame(Frame):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.ctno_edit = None
        self.cname_edit = None
        self.chours_edit = None
        self.credit_edit = None

        sql1 = "SELECT courses.cno FROM courses INNER JOIN teachers ON courses.ctno = teachers.tno"

        self.all_course_info = db_select(sql1)

        self.cno_list = self.listCreate(self.all_course_info, 0)

        self.SearchLineEdit_cno = SearchLineEdit(self)
        self.SearchLineEdit_cno.setPlaceholderText('请选择修改的课程号')
        self.SearchLineEdit_cno.setClearButtonEnabled(True)
        self.SearchLineEdit_cno.setFixedWidth(250)
        self.completer_cno = QCompleter(self.cno_list, self.SearchLineEdit_cno)
        self.completer_cno.setCaseSensitivity(Qt.CaseInsensitive)
        self.SearchLineEdit_cno.setCompleter(self.completer_cno)
        self.addWidget(self.SearchLineEdit_cno, 0, 0, 1, 1)

        self.LineEdit_tno = LineEdit(self)
        self.LineEdit_tno.setPlaceholderText('请输入修改后的教师号')
        self.LineEdit_tno.setClearButtonEnabled(True)
        self.LineEdit_tno.setFixedWidth(250)
        self.addWidget(self.LineEdit_tno, 1, 0, 1, 1)

        self.LineEdit_cname = LineEdit(self)
        self.LineEdit_cname.setPlaceholderText('请输入修改后的课程名')
        self.LineEdit_cname.setClearButtonEnabled(True)
        self.LineEdit_cname.setFixedWidth(250)
        self.addWidget(self.LineEdit_cname, 1, 1, 1, 1)

        self.LineEdit_chours = LineEdit(self)
        self.LineEdit_chours.setPlaceholderText('请输入修改后的学时')
        self.LineEdit_chours.setClearButtonEnabled(True)
        self.LineEdit_chours.setFixedWidth(250)
        self.addWidget(self.LineEdit_chours, 2, 0, 1, 1)

        self.LineEdit_credit = LineEdit(self)
        self.LineEdit_credit.setPlaceholderText('请输入修改后的学分')
        self.LineEdit_credit.setClearButtonEnabled(True)
        self.LineEdit_credit.setFixedWidth(250)
        self.addWidget(self.LineEdit_credit, 2, 1, 1, 1)


        self.EditButton = PrimaryPushButton(self)
        self.EditButton.setText('修改')
        self.addWidget(self.EditButton, 3, 0, 1, 2)

        self.EditButton.clicked.connect(self.EditCourse)

    def EditCourse(self):
        self.cno_edit = self.SearchLineEdit_cno.text()
        self.tno_edit = self.LineEdit_tno.text()
        self.cname_edit = self.LineEdit_cname.text()
        self.chours_edit = self.LineEdit_chours.text()
        self.credit_edit = self.LineEdit_credit.text()


        sql3 = "UPDATE courses"

        if self.cno_edit == '' and self.tno_edit == '' and self.cname_edit == '' and self.chours_edit == '' and self.credit_edit == '':
            AdminCou.infoBar_error('请输入修改后的信息！')
            return

        if self.tno_edit != '':
            sql3 += f" SET ctno = '{self.tno_edit}'"

        if self.cname_edit != '':
            if self.tno_edit != '':
                sql3 += f", cname = '{self.cname_edit}'"
            else:
                sql3 += f" SET cname = '{self.cname_edit}'"

        if self.chours_edit != '':
            if self.tno_edit != '' or self.cname_edit != '':
                sql3 += f", chours = {self.chours_edit}"
            else:
                sql3 += f" SET chours = {self.chours_edit}"

        if self.credit_edit != '':
            if self.tno_edit != '' or self.cname_edit != '' or self.chours_edit != '':
                sql3 += f", ccredit = {self.credit_edit}"
            else:
                sql3 += f" SET ccredit = {self.credit_edit}"

        sql3 += f" WHERE cno = '{self.cno_edit}'"


        print(sql3)

        try:
            db_update(sql3)
            AdminCou.infoBar_success('修改成功！')

        except:
            AdminCou.infoBar_error('修改失败！')

    def listCreate(self, input_list, index):
        output_list = []
        for i in input_list:
            output_list.append(str(i[index]))
        return output_list



class AddCourseFrame(Frame):
    def __init__(self, parent=None):
        super().__init__(parent)


        self.LineEdit_cname = LineEdit(self)
        self.LineEdit_cname.setPlaceholderText('请输入课程名')
        self.LineEdit_cname.setClearButtonEnabled(True)
        self.LineEdit_cname.setFixedWidth(250)
        self.addWidget(self.LineEdit_cname, 0, 0, 1, 1)

        self.LineEdit_ctno = LineEdit(self)
        self.LineEdit_ctno.setPlaceholderText('请输入该课教师号')
        self.LineEdit_ctno.setClearButtonEnabled(True)
        self.LineEdit_ctno.setFixedWidth(250)
        self.addWidget(self.LineEdit_ctno, 0, 1, 1, 1)

        self.LineEdit_chours = LineEdit(self)
        self.LineEdit_chours.setPlaceholderText('请输入该课学时')
        self.LineEdit_chours.setClearButtonEnabled(True)
        self.LineEdit_chours.setFixedWidth(250)
        self.addWidget(self.LineEdit_chours, 1, 0, 1, 1)

        self.LineEdit_credit = LineEdit(self)
        self.LineEdit_credit.setPlaceholderText('请输入该课学分')
        self.LineEdit_credit.setClearButtonEnabled(True)
        self.LineEdit_credit.setFixedWidth(250)
        self.addWidget(self.LineEdit_credit, 1, 1, 1, 1)

        self.AddButton = PrimaryPushButton(self)
        self.AddButton.setText('添加')
        self.addWidget(self.AddButton, 2, 0, 1, 2)

        self.AddButton.clicked.connect(self.AddTea)

    def AddTea(self):
        self.cname = self.LineEdit_cname.text()
        self.ctno = self.LineEdit_ctno.text()
        self.chours = self.LineEdit_chours.text()
        self.credit = self.LineEdit_credit.text()

        sql4 = "SELECT DISTINCT cname FROM tea_course_info WHERE tno = '%s'" % self.ctno

        tea_course_list = db_select(sql4)
        for i in tea_course_list:
            if self.cname in i:
                AdminCou.infoBar_error('该教师已教授该课程！')
                return

        if self.cname == '' or self.ctno == '' or self.chours == '' or self.credit == '':
            AdminCou.infoBar_error('请输入完整信息！')
            return

        sql5 = "INSERT INTO courses(cname, ctno, chours, ccredit) VALUES('%s', '%s', %s, %s)" % (self.cname, self.ctno, self.chours, self.credit)

        try:
            db_insert(sql5)
            AdminCou.infoBar_success('添加成功！')
        except:
            AdminCou.infoBar_error('添加失败！')

    def listCreate(self, input_list, index):
        output_list = []
        for i in input_list:
            output_list.append(str(i[index]))
        return output_list


class DelTeaFrame(Frame):
    def __init__(self, parent=None):
        super().__init__(parent)

        sql6 = "SELECT cno FROM courses ORDER BY cno ASC"
        self.all_course_info = db_select(sql6)
        self.course_list = self.listCreate(self.all_course_info, 0)

        self.cno = None
        self.SearchLineEdit_cno = SearchLineEdit(self)
        self.SearchLineEdit_cno.setPlaceholderText('请选择删除的课程号')
        self.SearchLineEdit_cno.setClearButtonEnabled(True)
        self.SearchLineEdit_cno.setFixedWidth(250)
        self.completer_cno = QCompleter(self.course_list, self.SearchLineEdit_cno)
        self.completer_cno.setCaseSensitivity(Qt.CaseInsensitive)
        self.SearchLineEdit_cno.setCompleter(self.completer_cno)
        self.addWidget(self.SearchLineEdit_cno, 0, 0, 1, 1)

        self.DelButton = PrimaryPushButton(self)
        self.DelButton.setText('删除')
        self.addWidget(self.DelButton, 0, 1, 1, 1)

        self.DelButton.clicked.connect(self.DelCourse)
        self.DelButton.clicked.connect(self.update)

    def update(self):
        sql6 = "SELECT cno FROM courses ORDER BY cno ASC"
        self.all_course_info = db_select(sql6)
        self.course_list = self.listCreate(self.all_course_info, 0)

        self.completer_cno = QCompleter(self.course_list, self.SearchLineEdit_cno)
        self.completer_cno.setCaseSensitivity(Qt.CaseInsensitive)
        self.SearchLineEdit_cno.setCompleter(self.completer_cno)

    def listCreate(self, input_list, index):
        output_list = []
        for i in input_list:
            output_list.append(str(i[index]))
        return output_list

    def DelCourse(self):
        title = self.tr('注意')
        content = self.tr(
            "你确定要删除此课程吗?")
        w = MessageBox(title, content, self.window())

        if w.exec_():
            try:
                self.cno = self.SearchLineEdit_cno.text()
                if self.cno == '':
                    AdminCou.infoBar_error('请输入课程号！')
                    return

                sql7 = f"DELETE FROM courses WHERE cno = '{self.cno}'"
                db_delete(sql7)
                AdminCou.infoBar_success('删除成功！')
            except:
                AdminCou.infoBar_error('删除失败！')

        else:
            pass

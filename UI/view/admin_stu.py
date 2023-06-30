# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QCompleter, QTableWidgetItem
from PyQt5.QtWidgets import QWidget, QFrame, QGridLayout
from qfluentwidgets import ComboBox, InfoBar, InfoBarPosition, SearchLineEdit, TableWidget, PrimaryPushButton, LineEdit, \
    MessageBox

from UI.connectDataBase import db_select, db_update, db_insert, db_delete
from .gallery_interface import GalleryInterface
from ..common.style_sheet import StyleSheet


class AdminStu(GalleryInterface):
    current_instance = None

    def __init__(self, parent=None):
        super().__init__(
            title='学生信息操作',
            subtitle='',
            parent=parent
        )
        AdminStu.current_instance = self

        self.addExampleCard(
            title=self.tr('学生信息查询'),
            widget=SearchStuFrame(self)
        )

        self.addExampleCard(
            title=self.tr('学生信息修改'),
            widget=EditStuFrame(self)
        )

        self.addExampleCard(
            title=self.tr('学生信息添加'),
            widget=AddStuFrame(self)
        )

        self.addExampleCard(
            title=self.tr('学生信息删除'),
            widget=DelStuFrame(self)
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


class SearchStuFrame(Frame):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.dname = None
        self.class_ = None
        self.ssex = None
        self.sage = None
        self.sname = None
        self.sno = None
        sql1 = f"SELECT students.sno, students.sname, students.sage, students.ssex, students.class, department.dname FROM students INNER JOIN department ON students.sdno = department.dno"
        self.all_stu_info = db_select(sql1)

        self.sno_list = self.listCreate(self.all_stu_info, 0)
        self.sname_list = self.listCreate(self.all_stu_info, 1)
        self.sage_list = set(self.listCreate(self.all_stu_info, 2))
        self.ssex_list = set(self.listCreate(self.all_stu_info, 3))
        self.class_list = set(self.listCreate(self.all_stu_info, 4))
        self.dname_list = set(self.listCreate(self.all_stu_info, 5))

        # self.spacer_widget = QWidget(self)
        # self.spacer_widget.setFixedSize(10, 20)
        # self.addWidget(self.spacer_widget, 0, 0, 1, 1)

        self.SearchLineEdit_sno = SearchLineEdit(self)
        self.SearchLineEdit_sno.setPlaceholderText('请输入学号')
        self.SearchLineEdit_sno.setClearButtonEnabled(True)
        self.SearchLineEdit_sno.setFixedWidth(200)
        self.completer_sno = QCompleter(self.sno_list, self.SearchLineEdit_sno)
        self.completer_sno.setCaseSensitivity(Qt.CaseInsensitive)
        self.SearchLineEdit_sno.setCompleter(self.completer_sno)
        self.addWidget(self.SearchLineEdit_sno, 0, 0, 1, 1)

        self.SearchLineEdit_sname = SearchLineEdit(self)
        self.SearchLineEdit_sname.setPlaceholderText('请输入姓名')
        self.SearchLineEdit_sname.setClearButtonEnabled(True)
        self.SearchLineEdit_sname.setFixedWidth(160)
        self.completer_sname = QCompleter(self.sname_list, self.SearchLineEdit_sname)
        self.completer_sname.setCaseSensitivity(Qt.CaseInsensitive)
        self.SearchLineEdit_sname.setCompleter(self.completer_sname)
        self.addWidget(self.SearchLineEdit_sname, 0, 1, 1, 2)

        self.SearchLineEdit_class = SearchLineEdit(self)
        self.SearchLineEdit_class.setPlaceholderText('请输入班级')
        self.SearchLineEdit_class.setClearButtonEnabled(True)
        self.SearchLineEdit_class.setFixedWidth(160)
        self.completer_class = QCompleter(self.class_list, self.SearchLineEdit_class)
        self.completer_class.setCaseSensitivity(Qt.CaseInsensitive)
        self.SearchLineEdit_class.setCompleter(self.completer_class)
        self.addWidget(self.SearchLineEdit_class, 0, 3, 1, 1)

        self.comboBox_dname = ComboBox(self)
        self.comboBox_dname.addItems(self.dname_list)
        self.comboBox_dname.addItems(["全部"])
        self.comboBox_dname.setCurrentIndex(0)
        self.comboBox_dname.setMaximumWidth(200)
        self.addWidget(self.comboBox_dname, 1, 0, 1, 1)

        self.comboBox_sage = ComboBox(self)
        self.comboBox_sage.addItems(self.sage_list)
        self.comboBox_sage.addItems(["全部"])
        self.comboBox_sage.setCurrentIndex(0)
        self.comboBox_sage.setMaximumWidth(80)
        self.addWidget(self.comboBox_sage, 1, 1, 1, 1)

        self.comboBox_ssex = ComboBox(self)
        self.comboBox_ssex.addItems(self.ssex_list)
        self.comboBox_ssex.addItems(["全部"])
        self.comboBox_ssex.setCurrentIndex(0)
        self.comboBox_ssex.setMaximumWidth(80)
        self.addWidget(self.comboBox_ssex, 1, 2, 1, 1)

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

        self.table.setRowCount(len(self.all_stu_info))
        self.table.setHorizontalHeaderLabels([
            self.tr('学号'), self.tr('姓名'), self.tr('年龄'),
            self.tr('性别'), self.tr('班级'), self.tr('学院'),
        ])

        for i, every_stu in enumerate(self.all_stu_info):
            for j in range(6):
                self.table.setItem(i, j, QTableWidgetItem(str(every_stu[j])))

        self.SearchButton.clicked.connect(self.stu_search)

        self.setFixedSize(860, 400)
        self.table.resizeColumnsToContents()
        self.table.setColumnWidth(0, 150)
        self.table.setColumnWidth(1, 150)
        self.table.setColumnWidth(2, 80)
        self.table.setColumnWidth(3, 80)
        self.table.setColumnWidth(4, 80)
        self.table.setColumnWidth(5, 300)

    def stu_search(self):
        try:
            self.sno = self.SearchLineEdit_sno.text()
            self.sname = self.SearchLineEdit_sname.text()
            self.sage = self.comboBox_sage.currentText()
            self.ssex = self.comboBox_ssex.currentText()
            self.class_ = self.SearchLineEdit_class.text()
            self.dname = self.comboBox_dname.currentText()

            sql2 = "SELECT students.sno, students.sname, students.sage, students.ssex, students.class, department.dname FROM students INNER JOIN department ON students.sdno = department.dno"

            if self.sno != '':
                sql2 += " WHERE students.sno = '%s'" % self.sno

            if self.sname != '':
                if self.sno != '':
                    sql2 += " AND students.sname = '%s'" % self.sname
                else:
                    sql2 += " WHERE students.sname = '%s'" % self.sname

            if self.sage != '全部':
                if self.sno != '' or self.sname != '':
                    sql2 += " AND students.sage = '%s'" % self.sage
                else:
                    sql2 += " WHERE students.sage = '%s'" % self.sage

            if self.ssex != '全部':
                if self.sno != '' or self.sname != '' or self.sage != '全部':
                    sql2 += " AND students.ssex = '%s'" % self.ssex
                else:
                    sql2 += " WHERE students.ssex = '%s'" % self.ssex

            if self.class_ != '':
                if self.sno != '' or self.sname != '' or self.sage != '全部' or self.ssex != '全部':
                    sql2 += " AND students.class = '%s'" % self.class_
                else:
                    sql2 += " WHERE students.class = '%s'" % self.class_

            if self.dname != '全部':
                if self.sno != '' or self.sname != '' or self.sage != '全部' or self.ssex != '全部' or self.class_ != '':
                    sql2 += " AND department.dname = '%s'" % self.dname
                else:
                    sql2 += " WHERE department.dname = '%s'" % self.dname

            sql2 += " ORDER BY students.sno"

            print(sql2)

            classInfos_query = db_select(sql2)

            if len(classInfos_query) == 0:
                raise Exception

            self.table.clearContents()
            for i, classInfo in enumerate(classInfos_query):
                for j in range(6):
                    self.table.setItem(i, j, QTableWidgetItem(str(classInfo[j])))

            self.setFixedSize(860, 400)
            self.table.resizeColumnsToContents()
            self.table.setColumnWidth(0, 150)
            self.table.setColumnWidth(1, 150)
            self.table.setColumnWidth(2, 80)
            self.table.setColumnWidth(3, 80)
            self.table.setColumnWidth(4, 80)
            self.table.setColumnWidth(5, 300)
            AdminStu.infoBar_success('查询成功！')

        except:
            AdminStu.infoBar_error('查询失败！')

    def listCreate(self, input_list, index):
        output_list = []
        for i in input_list:
            output_list.append(str(i[index]))
        return output_list


class EditStuFrame(Frame):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.dname_edit = None
        self.class_edit = None
        self.sage_edit = None
        self.sname_edit = None

        sql1 = f"SELECT students.sno, students.sname, students.sage, students.ssex, students.class, department.dname " \
               f"FROM students INNER JOIN department ON students.sdno = department.dno"

        sql2 = "SELECT dname FROM department"

        self.all_stu_info = db_select(sql1)
        self.all_dname = db_select(sql2)
        self.sno_list = self.listCreate(self.all_stu_info, 0)
        self.dname_list = self.listCreate(self.all_dname, 0)

        self.SearchLineEdit_sno = SearchLineEdit(self)
        self.SearchLineEdit_sno.setPlaceholderText('请选择修改的学生学号')
        self.SearchLineEdit_sno.setClearButtonEnabled(True)
        self.SearchLineEdit_sno.setFixedWidth(250)
        self.completer_sno = QCompleter(self.sno_list, self.SearchLineEdit_sno)
        self.completer_sno.setCaseSensitivity(Qt.CaseInsensitive)
        self.SearchLineEdit_sno.setCompleter(self.completer_sno)
        self.addWidget(self.SearchLineEdit_sno, 0, 0, 1, 1)

        self.LineEdit_sname = LineEdit(self)
        self.LineEdit_sname.setPlaceholderText('请输入修改后的学生姓名')
        self.LineEdit_sname.setClearButtonEnabled(True)
        self.LineEdit_sname.setFixedWidth(250)
        self.addWidget(self.LineEdit_sname, 1, 0, 1, 1)

        self.LineEdit_sage = LineEdit(self)
        self.LineEdit_sage.setPlaceholderText('请输入修改后的学生年龄')
        self.LineEdit_sage.setClearButtonEnabled(True)
        self.LineEdit_sage.setFixedWidth(250)
        self.addWidget(self.LineEdit_sage, 1, 1, 1, 1)

        self.LineEdit_class = LineEdit(self)
        self.LineEdit_class.setPlaceholderText('请输入修改后的学生班级')
        self.LineEdit_class.setClearButtonEnabled(True)
        self.LineEdit_class.setFixedWidth(250)
        self.addWidget(self.LineEdit_class, 2, 0, 1, 1)

        self.comboBox_dname = ComboBox(self)
        self.comboBox_dname.addItems(self.dname_list)
        self.comboBox_dname.setFixedWidth(250)
        self.addWidget(self.comboBox_dname, 2, 1, 1, 1)

        self.EditButton = PrimaryPushButton(self)
        self.EditButton.setText('修改')
        self.addWidget(self.EditButton, 0, 1, 1, 1)

        self.EditButton.clicked.connect(self.EditStu)

    def EditStu(self):
        self.sname_edit = self.LineEdit_sname.text()
        self.sage_edit = self.LineEdit_sage.text()
        self.class_edit = self.LineEdit_class.text()
        self.dname_edit = self.comboBox_dname.currentText()

        sql3 = "UPDATE students"

        if self.sname_edit == '' and self.sage_edit == '' and self.class_edit == '' and self.dname_edit == '':
            AdminStu.infoBar_error('请输入修改后的信息！')
            return

        if self.sname_edit != '':
            sql3 += f" SET sname = '{self.sname_edit}'"

        if self.sage_edit != '':
            if self.sname_edit != '':
                sql3 += f", sage = '{self.sage_edit}'"
            else:
                sql3 += f" SET sage = '{self.sage_edit}'"

        if self.class_edit != '':
            if self.sname_edit != '' or self.sage_edit != '':
                sql3 += f", class = '{self.class_edit}'"
            else:
                sql3 += f" SET class = '{self.class_edit}'"

        if self.dname_edit != '':
            if self.sname_edit != '' or self.sage_edit != '' or self.class_edit != '':
                sql3 += f", sdno = (SELECT dno FROM department WHERE dname = '{self.dname_edit}')"
            else:
                sql3 += f" SET sdno = (SELECT dno FROM department WHERE dname = '{self.dname_edit}')"

        sql3 += f" WHERE sno = '{self.SearchLineEdit_sno.text()}'"

        try:
            db_update(sql3)
            AdminStu.infoBar_success('修改成功！')

        except:
            AdminStu.infoBar_error('修改失败！')

    def listCreate(self, input_list, index):
        output_list = []
        for i in input_list:
            output_list.append(str(i[index]))
        return output_list


class AddStuFrame(Frame):
    def __init__(self, parent=None):
        super().__init__(parent)

        sql1 = "SELECT dname FROM department"
        self.all_dname = db_select(sql1)
        self.dname_list = self.listCreate(self.all_dname, 0)

        self.LineEdit_sname = LineEdit(self)
        self.LineEdit_sname.setPlaceholderText('请输入学生姓名')
        self.LineEdit_sname.setClearButtonEnabled(True)
        self.LineEdit_sname.setFixedWidth(250)
        self.addWidget(self.LineEdit_sname, 0, 0, 1, 1)

        self.LineEdit_sage = LineEdit(self)
        self.LineEdit_sage.setPlaceholderText('请输入学生年龄')
        self.LineEdit_sage.setClearButtonEnabled(True)
        self.LineEdit_sage.setFixedWidth(250)
        self.addWidget(self.LineEdit_sage, 0, 1, 1, 1)

        self.comboBox_ssex = ComboBox(self)
        self.comboBox_ssex.addItems(['男', '女'])
        self.comboBox_ssex.setFixedWidth(250)
        self.addWidget(self.comboBox_ssex, 1, 0, 1, 1)

        self.LineEdit_class = LineEdit(self)
        self.LineEdit_class.setPlaceholderText('请输入学生班级')
        self.LineEdit_class.setClearButtonEnabled(True)
        self.LineEdit_class.setFixedWidth(250)
        self.addWidget(self.LineEdit_class, 1, 1, 1, 1)

        self.comboBox_dname = ComboBox(self)
        self.comboBox_dname.addItems(self.dname_list)
        self.comboBox_dname.setFixedWidth(250)
        self.addWidget(self.comboBox_dname, 2, 0, 1, 1)

        self.AddButton = PrimaryPushButton(self)
        self.AddButton.setText('添加')
        self.addWidget(self.AddButton, 2, 1, 1, 1)

        self.AddButton.clicked.connect(self.AddStu)

    def AddStu(self):
        self.sname = self.LineEdit_sname.text().split()
        self.sage = self.LineEdit_sage.text().split()
        self.ssex = self.comboBox_ssex.currentText().split()
        self.class_ = self.LineEdit_class.text().split()
        self.dname = self.comboBox_dname.currentText().split()

        if self.sname == '' or self.sage == '' or self.class_ == '' or self.dname == '':
            AdminStu.infoBar_error('请输入完整的学生信息！')
            return

        sql4 = f"INSERT INTO students(sname, sage, ssex, class, sdno) VALUES('{self.sname}', '{self.sage}', '{self.ssex}', '{self.class_}', (SELECT dno FROM department WHERE dname = '{self.dname}'))"

        try:
            db_insert(sql4)
            AdminStu.infoBar_success('添加成功！')
        except:
            AdminStu.infoBar_error('添加失败！')

    def listCreate(self, input_list, index):
        output_list = []
        for i in input_list:
            output_list.append(str(i[index]))
        return output_list


class DelStuFrame(Frame):
    def __init__(self, parent=None):
        super().__init__(parent)

        sql6 = "SELECT sno FROM students ORDER BY sno ASC"
        self.all_sno_info = db_select(sql6)
        self.sno_list = self.listCreate(self.all_sno_info, 0)

        self.sno = None
        self.SearchLineEdit_sno = SearchLineEdit(self)
        self.SearchLineEdit_sno.setPlaceholderText('请选择删除的学生学号')
        self.SearchLineEdit_sno.setClearButtonEnabled(True)
        self.SearchLineEdit_sno.setFixedWidth(250)
        self.completer_sno = QCompleter(self.sno_list, self.SearchLineEdit_sno)
        self.completer_sno.setCaseSensitivity(Qt.CaseInsensitive)
        self.SearchLineEdit_sno.setCompleter(self.completer_sno)
        self.addWidget(self.SearchLineEdit_sno, 0, 0, 1, 1)

        self.DelButton = PrimaryPushButton(self)
        self.DelButton.setText('删除')
        self.addWidget(self.DelButton, 0, 1, 1, 1)

        self.DelButton.clicked.connect(self.DelStu)
        self.DelButton.clicked.connect(self.update)

    def update(self):
        sql6 = "SELECT sno FROM students ORDER BY sno ASC"
        self.all_sno_info = db_select(sql6)
        self.sno_list = self.listCreate(self.all_sno_info, 0)

        self.completer_sno = QCompleter(self.sno_list, self.SearchLineEdit_sno)
        self.completer_sno.setCaseSensitivity(Qt.CaseInsensitive)
        self.SearchLineEdit_sno.setCompleter(self.completer_sno)


    def listCreate(self, input_list, index):
        output_list = []
        for i in input_list:
            output_list.append(str(i[index]))
        return output_list

    def DelStu(self):
        title = self.tr('注意')
        content = self.tr(
            "你确定要删除此学生吗?")
        w = MessageBox(title, content, self.window())

        if w.exec_():
            try:
                self.sno = self.SearchLineEdit_sno.text()
                if self.sno == '':
                    AdminStu.infoBar_error('请输入学生学号！')
                    return

                sql5 = f"DELETE FROM students WHERE sno = '{self.sno}'"
                db_delete(sql5)
                AdminStu.infoBar_success('删除成功！')
            except:
                AdminStu.infoBar_error('删除失败！')

        else:
            pass

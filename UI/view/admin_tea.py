# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QCompleter, QTableWidgetItem
from PyQt5.QtWidgets import QWidget, QFrame, QGridLayout
from qfluentwidgets import ComboBox, InfoBar, InfoBarPosition, SearchLineEdit, PrimaryPushButton, TableWidget, LineEdit, \
    MessageBox

from UI.connectDataBase import db_select, db_update, db_insert, db_delete
from .gallery_interface import GalleryInterface
from ..common.style_sheet import StyleSheet


class AdminTea(GalleryInterface):
    current_instance = None

    def __init__(self, parent=None):
        super().__init__(
            title='教师信息操作',
            subtitle='',
            parent=parent
        )
        AdminTea.current_instance = self

        self.addExampleCard(
            title=self.tr('教师信息查询'),
            widget=SearchTeaFrame(self)
        )

        self.addExampleCard(
            title=self.tr('教师信息修改'),
            widget=EditTeaFrame(self)
        )

        self.addExampleCard(
            title=self.tr('教师信息添加'),
            widget=AddTeaFrame(self)
        )

        self.addExampleCard(
            title=self.tr('教师信息删除'),
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


class SearchTeaFrame(Frame):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.tno = None
        self.tname = None
        self.tage = None
        self.tsex = None
        self.dname = None
        sql1 = "SELECT teachers.tno, teachers.tname, teachers.tage, teachers.tsex, department.dname FROM teachers " \
               "INNER JOIN department ON teachers.tdno = department.dno"
        self.all_tea_info = db_select(sql1)

        self.tno_list = self.listCreate(self.all_tea_info, 0)
        self.tname_list = self.listCreate(self.all_tea_info, 1)
        self.tage_list = sorted(set(self.listCreate(self.all_tea_info, 2)))
        self.tsex_list = set(self.listCreate(self.all_tea_info, 3))
        self.dname_list = set(self.listCreate(self.all_tea_info, 4))

        # self.spacer_widget = QWidget(self)
        # self.spacer_widget.setFixedSize(10, 20)
        # self.addWidget(self.spacer_widget, 0, 0, 1, 1)

        self.SearchLineEdit_tno = SearchLineEdit(self)
        self.SearchLineEdit_tno.setPlaceholderText('请输入教师工号')
        self.SearchLineEdit_tno.setClearButtonEnabled(True)
        self.SearchLineEdit_tno.setFixedWidth(200)
        self.completer_tno = QCompleter(self.tno_list, self.SearchLineEdit_tno)
        self.completer_tno.setCaseSensitivity(Qt.CaseInsensitive)
        self.SearchLineEdit_tno.setCompleter(self.completer_tno)
        self.addWidget(self.SearchLineEdit_tno, 0, 0, 1, 1)

        self.SearchLineEdit_tname = SearchLineEdit(self)
        self.SearchLineEdit_tname.setPlaceholderText('请输入姓名')
        self.SearchLineEdit_tname.setClearButtonEnabled(True)
        self.SearchLineEdit_tname.setFixedWidth(160)
        self.completer_tname = QCompleter(self.tname_list, self.SearchLineEdit_tname)
        self.completer_tname.setCaseSensitivity(Qt.CaseInsensitive)
        self.SearchLineEdit_tname.setCompleter(self.completer_tname)
        self.addWidget(self.SearchLineEdit_tname, 0, 1, 1, 2)

        self.comboBox_dname = ComboBox(self)
        self.comboBox_dname.addItems(self.dname_list)
        self.comboBox_dname.addItems(["全部"])
        self.comboBox_dname.setCurrentIndex(0)
        self.comboBox_dname.setMaximumWidth(200)
        self.addWidget(self.comboBox_dname, 1, 0, 1, 1)

        self.comboBox_tage = ComboBox(self)
        self.comboBox_tage.addItems(self.tage_list)
        self.comboBox_tage.addItems(["全部"])
        self.comboBox_tage.setCurrentIndex(0)
        self.comboBox_tage.setMaximumWidth(80)
        self.addWidget(self.comboBox_tage, 1, 1, 1, 1)

        self.comboBox_tsex = ComboBox(self)
        self.comboBox_tsex.addItems(self.tsex_list)
        self.comboBox_tsex.addItems(["全部"])
        self.comboBox_tsex.setCurrentIndex(0)
        self.comboBox_tsex.setMaximumWidth(80)
        self.addWidget(self.comboBox_tsex, 1, 2, 1, 1)

        self.SearchButton = PrimaryPushButton(self)
        self.SearchButton.setText('查询')
        self.SearchButton.setFixedSize(80, 30)
        self.addWidget(self.SearchButton, 1, 6, 1, 1)

        self.table = TableWidget(self)
        self.addWidget(self.table, 2, 0, 1, 8)

        self.table.verticalHeader().hide()
        self.table.setColumnCount(5)
        self.table.setEditTriggers(self.table.NoEditTriggers)
        self.table.setSortingEnabled(True)

        self.table.setRowCount(len(self.all_tea_info))
        self.table.setHorizontalHeaderLabels([
            self.tr('工号'), self.tr('姓名'), self.tr('年龄'),
            self.tr('性别'), self.tr('学院'),
        ])

        for i, every_tea in enumerate(self.all_tea_info):
            for j in range(5):
                self.table.setItem(i, j, QTableWidgetItem(str(every_tea[j])))

        self.SearchButton.clicked.connect(self.tea_search)

        self.setFixedSize(860, 400)
        self.table.resizeColumnsToContents()
        self.table.setColumnWidth(0, 150)
        self.table.setColumnWidth(1, 150)
        self.table.setColumnWidth(2, 80)
        self.table.setColumnWidth(3, 80)
        self.table.setColumnWidth(4, 400)


    def tea_search(self):
        try:
            self.tno = self.SearchLineEdit_tno.text()
            self.tname = self.SearchLineEdit_tname.text()
            self.tage = self.comboBox_tage.currentText()
            self.tsex = self.comboBox_tsex.currentText()
            self.dname = self.comboBox_dname.currentText()

            sql2 = "SELECT teachers.tno, teachers.tname, teachers.tage, teachers.tsex, department.dname FROM teachers " \
                   "INNER JOIN department ON teachers.tdno = department.dno"

            if self.tno != "":
                sql2 += " WHERE teachers.tno = '%s'" % self.tno

            if self.tname != "":
                if self.tno != "":
                    sql2 += " AND teachers.tname = '%s'" % self.tname
                else:
                    sql2 += " WHERE teachers.tname = '%s'" % self.tname

            if self.tage != "全部":
                if self.tno != "" or self.tname != "":
                    sql2 += " AND teachers.tage = '%s'" % self.tage
                else:
                    sql2 += " WHERE teachers.tage = '%s'" % self.tage

            if self.tsex != "全部":
                if self.tno != "" or self.tname != "" or self.tage != "全部":
                    sql2 += " AND teachers.tsex = '%s'" % self.tsex
                else:
                    sql2 += " WHERE teachers.tsex = '%s'" % self.tsex

            if self.dname != "全部":
                if self.tno != "" or self.tname != "" or self.tage != "全部" or self.tsex != "全部":
                    sql2 += " AND department.dname = '%s'" % self.dname
                else:
                    sql2 += " WHERE department.dname = '%s'" % self.dname

            sql2 += " ORDER BY teachers.tno"

            print(sql2)

            teaInfos_query = db_select(sql2)

            if len(teaInfos_query) == 0:
                raise Exception

            self.table.clearContents()
            for i, teaInfo in enumerate(teaInfos_query):
                for j in range(5):
                    self.table.setItem(i, j, QTableWidgetItem(str(teaInfo[j])))

            self.setFixedSize(860, 400)
            self.table.resizeColumnsToContents()
            self.table.setColumnWidth(0, 150)
            self.table.setColumnWidth(1, 150)
            self.table.setColumnWidth(2, 80)
            self.table.setColumnWidth(3, 80)
            self.table.setColumnWidth(4, 400)
            AdminTea.infoBar_success('查询成功！')

        except:
            AdminTea.infoBar_error('查询失败！')

    def listCreate(self, input_list, index):
        output_list = []
        for i in input_list:
            output_list.append(str(i[index]))
        return output_list


class EditTeaFrame(Frame):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.dname_edit = None
        self.class_edit = None
        self.tage_edit = None
        self.tname_edit = None

        sql1 = "SELECT teachers.tno, teachers.tname, teachers.tage, teachers.tsex, department.dname FROM teachers " \
               "INNER JOIN department ON teachers.tdno = department.dno"

        sql2 = "SELECT dname FROM department"

        self.all_tea_info = db_select(sql1)
        self.all_dname = db_select(sql2)
        self.tno_list = self.listCreate(self.all_tea_info, 0)
        self.dname_list = self.listCreate(self.all_dname, 0)

        self.SearchLineEdit_tno = SearchLineEdit(self)
        self.SearchLineEdit_tno.setPlaceholderText('请选择修改的教师工号')
        self.SearchLineEdit_tno.setClearButtonEnabled(True)
        self.SearchLineEdit_tno.setFixedWidth(250)
        self.completer_tno = QCompleter(self.tno_list, self.SearchLineEdit_tno)
        self.completer_tno.setCaseSensitivity(Qt.CaseInsensitive)
        self.SearchLineEdit_tno.setCompleter(self.completer_tno)
        self.addWidget(self.SearchLineEdit_tno, 0, 0, 1, 1)

        self.LineEdit_sname = LineEdit(self)
        self.LineEdit_sname.setPlaceholderText('请输入修改后的教师姓名')
        self.LineEdit_sname.setClearButtonEnabled(True)
        self.LineEdit_sname.setFixedWidth(250)
        self.addWidget(self.LineEdit_sname, 1, 0, 1, 1)

        self.LineEdit_sage = LineEdit(self)
        self.LineEdit_sage.setPlaceholderText('请输入修改后的教师年龄')
        self.LineEdit_sage.setClearButtonEnabled(True)
        self.LineEdit_sage.setFixedWidth(250)
        self.addWidget(self.LineEdit_sage, 1, 1, 1, 1)

        self.comboBox_dname = ComboBox(self)
        self.comboBox_dname.addItems(self.dname_list)
        self.comboBox_dname.setFixedWidth(250)
        self.addWidget(self.comboBox_dname, 2, 0, 1, 1)

        self.EditButton = PrimaryPushButton(self)
        self.EditButton.setText('修改')
        self.addWidget(self.EditButton, 2, 1, 1, 1)

        self.EditButton.clicked.connect(self.EditTea)

    def EditTea(self):
        self.tname_edit = self.LineEdit_sname.text()
        self.tage_edit = self.LineEdit_sage.text()
        self.dname_edit = self.comboBox_dname.currentText()

        sql3 = "UPDATE teachers"

        if self.tname_edit == '' and self.tage_edit == '' and self.dname_edit == '':
            AdminTea.infoBar_error('请输入修改后的信息！')
            return

        if self.tname_edit != '':
            sql3 += f" SET tname = '{self.tname_edit}'"

        if self.tage_edit != '':
            if self.tname_edit != '':
                sql3 += f", tage = '{self.tage_edit}'"
            else:
                sql3 += f" SET tage = '{self.tage_edit}'"

        if self.dname_edit != '':
            if self.tname_edit != '' or self.tage_edit != '':
                sql3 += f", tdno = (SELECT dno FROM department WHERE dname = '{self.dname_edit}')"
            else:
                sql3 += f" SET tdno = (SELECT dno FROM department WHERE dname = '{self.dname_edit}')"

        sql3 += " WHERE tno = '%s'" % self.SearchLineEdit_tno.text()


        print(sql3)

        try:
            db_update(sql3)
            AdminTea.infoBar_success('修改成功！')

        except:
            AdminTea.infoBar_error('修改失败！')

    def listCreate(self, input_list, index):
        output_list = []
        for i in input_list:
            output_list.append(str(i[index]))
        return output_list


class AddTeaFrame(Frame):
    def __init__(self, parent=None):
        super().__init__(parent)

        sql1 = "SELECT dname FROM department"
        self.all_dname = db_select(sql1)
        self.dname_list = self.listCreate(self.all_dname, 0)

        self.LineEdit_tname = LineEdit(self)
        self.LineEdit_tname.setPlaceholderText('请输入教师姓名')
        self.LineEdit_tname.setClearButtonEnabled(True)
        self.LineEdit_tname.setFixedWidth(250)
        self.addWidget(self.LineEdit_tname, 0, 0, 1, 1)

        self.LineEdit_tage = LineEdit(self)
        self.LineEdit_tage.setPlaceholderText('请输入教师年龄')
        self.LineEdit_tage.setClearButtonEnabled(True)
        self.LineEdit_tage.setFixedWidth(250)
        self.addWidget(self.LineEdit_tage, 0, 1, 1, 1)

        self.comboBox_tsex = ComboBox(self)
        self.comboBox_tsex.addItems(['男', '女'])
        self.comboBox_tsex.setFixedWidth(250)
        self.addWidget(self.comboBox_tsex, 1, 0, 1, 1)

        self.comboBox_dname = ComboBox(self)
        self.comboBox_dname.addItems(self.dname_list)
        self.comboBox_dname.setFixedWidth(250)
        self.addWidget(self.comboBox_dname, 1, 1, 1, 1)

        self.AddButton = PrimaryPushButton(self)
        self.AddButton.setText('添加')
        self.addWidget(self.AddButton, 2, 0, 1, 2)

        self.AddButton.clicked.connect(self.AddTea)

    def AddTea(self):
        self.tname = self.LineEdit_tname.text()
        self.tage = self.LineEdit_tage.text()
        self.tsex = self.comboBox_tsex.currentText()
        self.dname = self.comboBox_dname.currentText()

        if self.tname == '' or self.tage == '' or self.dname == '':
            AdminTea.infoBar_error('请输入完整的教师信息！')
            return

        sql4 = "INSERT INTO teachers (tname, tage, tsex, tdno) VALUES ('%s', '%s', '%s', (SELECT dno FROM department WHERE dname = '%s'))" % (self.tname, self.tage, self.tsex, self.dname)

        try:
            db_insert(sql4)
            AdminTea.infoBar_success('添加成功！')
        except:
            AdminTea.infoBar_error('添加失败！')

    def listCreate(self, input_list, index):
        output_list = []
        for i in input_list:
            output_list.append(str(i[index]))
        return output_list


class DelTeaFrame(Frame):
    def __init__(self, parent=None):
        super().__init__(parent)

        sql6 = "SELECT tno FROM teachers ORDER BY tno ASC"
        self.all_tno_info = db_select(sql6)
        self.tno_list = self.listCreate(self.all_tno_info, 0)

        self.tno = None
        self.SearchLineEdit_tno = SearchLineEdit(self)
        self.SearchLineEdit_tno.setPlaceholderText('请选择删除的教师工号')
        self.SearchLineEdit_tno.setClearButtonEnabled(True)
        self.SearchLineEdit_tno.setFixedWidth(250)
        self.completer_tno = QCompleter(self.tno_list, self.SearchLineEdit_tno)
        self.completer_tno.setCaseSensitivity(Qt.CaseInsensitive)
        self.SearchLineEdit_tno.setCompleter(self.completer_tno)
        self.addWidget(self.SearchLineEdit_tno, 0, 0, 1, 1)

        self.DelButton = PrimaryPushButton(self)
        self.DelButton.setText('删除')
        self.addWidget(self.DelButton, 0, 1, 1, 1)

        self.DelButton.clicked.connect(self.DelTea)
        self.DelButton.clicked.connect(self.update)

    def update(self):
        sql6 = "SELECT tno FROM teachers ORDER BY tno ASC"
        self.all_tno_info = db_select(sql6)
        self.tno_list = self.listCreate(self.all_tno_info, 0)

        self.completer_tno = QCompleter(self.tno_list, self.SearchLineEdit_tno)
        self.completer_tno.setCaseSensitivity(Qt.CaseInsensitive)
        self.SearchLineEdit_tno.setCompleter(self.completer_tno)

    def listCreate(self, input_list, index):
        output_list = []
        for i in input_list:
            output_list.append(str(i[index]))
        return output_list

    def DelTea(self):
        title = self.tr('注意')
        content = self.tr(
            "你确定要删除此教师吗?")
        w = MessageBox(title, content, self.window())

        if w.exec_():
            try:
                self.tno = self.SearchLineEdit_tno.text()
                if self.tno == '':
                    AdminTea.infoBar_error('请输入教师工号！')
                    return

                sql5 = f"DELETE FROM teachers WHERE tno = '{self.tno}'"
                db_delete(sql5)
                AdminTea.infoBar_success('删除成功！')
            except:
                AdminTea.infoBar_error('删除失败！')

        else:
            pass

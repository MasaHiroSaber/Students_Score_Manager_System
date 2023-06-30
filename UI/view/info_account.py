from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QFrame, QGridLayout, QPushButton
from qfluentwidgets import LineEdit, PrimaryPushButton, InfoBarPosition, InfoBar
from qfluentwidgets import PushButton, Dialog, MessageBox, ColorDialog
from .gallery_interface import GalleryInterface
from ..common.style_sheet import StyleSheet
import pymysql
from UI.connectDataBase import db_update
from UI.global_var import globalVal


class InfoAccount(GalleryInterface):
    current_instance = None

    def __init__(self, parent=None):
        super().__init__(
            title='个人账号',
            subtitle='',
            parent=parent
        )
        InfoAccount.current_instance = self

        self.addExampleCard(
            self.tr('修改密码'),
            widget=TextFrame(self)
        )

    @classmethod
    def infoBar_success(cls, content):
        InfoBar.success(
            title='成功',
            content=content,
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP_RIGHT,
            duration=2000,
            parent=cls.current_instance
        )

    @classmethod
    def infoBar_error(cls, content):
        InfoBar.error(
            title='错误',
            content=content,
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
        self.gBoxLayout.setContentsMargins(20, 20, 20, 20)

        self.setObjectName('frame')
        StyleSheet.VIEW_INTERFACE.apply(self)

    def addWidget(self, widget, row, column, rowSpan=1, columnSpan=1):
        self.gBoxLayout.addWidget(widget, row, column, rowSpan, columnSpan)


class TextFrame(Frame):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.label_1 = QtWidgets.QLabel(self)
        self.label_1.setText('    旧密码    ')
        self.addWidget(self.label_1, 0, 0, 1, 1)

        self.lineEdit_1 = LineEdit(self)
        self.lineEdit_1.setPlaceholderText("请输入旧密码")
        self.lineEdit_1.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_1.setClearButtonEnabled(True)
        self.lineEdit_1.setMinimumWidth(300)
        self.addWidget(self.lineEdit_1, 0, 1, 1, 2)

        self.spacer_widget_1 = QWidget(self)
        self.spacer_widget_1.setFixedSize(10, 20)
        self.addWidget(self.spacer_widget_1, 1, 0, 1, 1)

        self.label_2 = QtWidgets.QLabel(self)
        self.label_2.setText('    新密码    ')
        self.addWidget(self.label_2, 2, 0, 1, 1)

        self.lineEdit_2 = LineEdit(self)
        self.lineEdit_2.setPlaceholderText("请输入新密码")
        self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_2.setClearButtonEnabled(True)
        self.addWidget(self.lineEdit_2, 2, 1, 1, 2)

        self.spacer_widget_2 = QWidget(self)
        self.spacer_widget_2.setFixedSize(10, 20)
        self.addWidget(self.spacer_widget_2, 3, 0, 1, 1)

        self.button_1 = PrimaryPushButton(self.tr('修改密码'), self)
        self.button_1.setMaximumWidth(100)
        self.addWidget(self.button_1, 4, 2, 1, 1)
        self.button_1.clicked.connect(self.change_password_info)

    def change_password_info(self):
        title = self.tr('注意')
        content = self.tr(
            "你确定要修改密码吗?")
        w = MessageBox(title, content, self.window())
        if w.exec():
            try:
                account_type = None
                account_id = None
                gl_username = globalVal.global_list[0]
                gl_password = globalVal.global_list[1]
                old_password = self.lineEdit_1.text().split()[0]
                new_password = self.lineEdit_2.text().split()[0]

                if str(gl_username[0]) == '1':
                    account_type = 'stu_ac'
                    account_id = 'sno'
                elif str(gl_username[0]) == '2':
                    account_type = 'tea_ac'
                    account_id = 'tno'
                elif str(gl_username) == 'admin':
                    account_type = 'admin_ac'
                    account_id = 'admin_id'

                if new_password == '' or ' ' in new_password:
                    InfoAccount.infoBar_error('密码不能为空或包含空格')

                elif new_password == old_password[0]:
                    InfoAccount.infoBar_error('新密码不能与旧密码相同')

                elif old_password == gl_password[0]:
                    sql = f"update {account_type} set password ='{new_password}' where {account_id} ='{gl_username}'"
                    status = db_update(sql)

                    if status:
                        InfoAccount.infoBar_success('修改成功')
                        globalVal.global_list[1] = new_password
                    else:
                        InfoAccount.infoBar_error('修改失败')

                else:
                    InfoAccount.infoBar_error('旧密码错误')
            except:
                InfoAccount.infoBar_error('修改失败')
        else:
            pass

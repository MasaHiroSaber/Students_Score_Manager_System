# -*- coding: utf-8 -*-
import sys
import UI.login
from PyQt5.QtCore import Qt, QLocale
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QApplication
from qframelesswindow import StandardTitleBar, AcrylicWindow
from qfluentwidgets import setThemeColor, FluentTranslator, InfoBarPosition, InfoBar
from UI.LoginWindow import Ui_Form
from UI.MainWindow import MainWindow
from UI.global_var import globalVal
import UI.resources_rc


class LoginWindow(AcrylicWindow, Ui_Form):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        setThemeColor('#28afe9')

        self.setTitleBar(StandardTitleBar(self))
        self.titleBar.raise_()

        self.label.setScaledContents(False)
        self.setWindowTitle('Students Score Management System')
        self.setWindowIcon(QIcon(":/images/login.png"))
        self.resize(1100, 500)

        self.pushButton.clicked.connect(self.db_login)

        self.windowEffect.setMicaEffect(self.winId())
        self.setStyleSheet("LoginWindow{background: rgba(242, 242, 242, 0.8)}")
        self.titleBar.titleLabel.setStyleSheet("""
            QLabel{
                background: transparent;
                font: 13px 'Segoe UI';
                padding: 0 4px;
                color: white
            }
        """)

        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)

    def resizeEvent(self, e):
        super().resizeEvent(e)
        pixmap = QPixmap(":/images/background.png").scaled(
            self.label.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        self.label.setPixmap(pixmap)

    # 按下登录按钮后的操作
    def db_login(self):
        global app_start
        # 获取用户名和密码
        db_username = self.lineEdit_3.text()
        db_password = self.lineEdit_4.text()
        db_connect = UI.login.db_login(db_username, db_password)

        globalVal.global_list.append(db_username)
        globalVal.global_list.append(db_password)

        if db_connect == -1:
            # 用户名或密码错误，弹出提示框
            InfoBar.warning(
                title="警告",
                content="用户名或密码错误",
                orient=Qt.Horizontal,
                isClosable=False,
                position=InfoBarPosition.TOP_RIGHT,
                duration=3000,
                parent=self
            )
            app_start = -1
        elif db_connect == -2:
            # 无法连接到数据库，弹出提示框
            InfoBar.error(
                title='错误',
                content="连接至数据库失败",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP_RIGHT,
                duration=-1,
                parent=self
            )
            app_start = -1

        elif db_connect == 1:
            self.close()
            app_start = 1

        elif db_connect == 2:
            self.close()
            app_start = 2

        elif db_connect == 3:
            self.close()
            app_start = 3


if __name__ == '__main__':
    global app_start
    app_start = None

    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)

    translator = FluentTranslator(QLocale())
    app.installTranslator(translator)

    w = LoginWindow()
    w.show()
    app.exec_()

    if app_start == 1:
        MainWindow(1)

    elif app_start == 2:
        MainWindow(2)

    elif app_start == 3:
        MainWindow(3)

    else:
        pass


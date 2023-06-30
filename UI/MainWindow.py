# coding:utf-8
import os
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from UI.common.config import cfg
from UI.view.admin_page import AMainWindow
from UI.view.main_window import MainWindow
from UI.view.stu_page import SMainWindow
from UI.view.tea_page import TMainWindow


class MainWindow:
    if cfg.get(cfg.dpiScale) == "Auto":
        QApplication.setHighDpiScaleFactorRoundingPolicy(
            Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    else:
        os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "0"
        os.environ["QT_SCALE_FACTOR"] = str(cfg.get(cfg.dpiScale))

    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)
    app.setAttribute(Qt.AA_DontCreateNativeWidgetSiblings)

    def __init__(self, status):
        self.run(status)
        self.app.exec_()

    def run(self, status):
        if status == 1:
            # create main window
            print('已启动学生端')
            w = SMainWindow()
            w.show()

        elif status == 2:
            # create main window
            print('已启动教师端')
            w = TMainWindow()
            w.show()

        elif status == 3:
            # create main window
            print('已启动管理员端')
            w = AMainWindow()
            w.show()


# coding: utf-8
from PyQt5.QtCore import Qt, pyqtSignal, QEasingCurve, QUrl
from PyQt5.QtGui import QIcon, QDesktopServices
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QFrame, QWidget
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import (NavigationInterface, NavigationItemPosition, PopUpAniStackedWidget, qrouter)

from .gallery_interface import GalleryInterface
from .admin_stu import AdminStu
from .admin_tea import AdminTea
from .admin_cou import AdminCou
from .admin_account import AdminAccount
from .setting_interface import SettingInterface
from .title_bar import CustomTitleBar
from ..common.signal_bus import signalBus
from ..common.style_sheet import StyleSheet
from ..components.frameless_window import FramelessWindow


class StackedWidget(QFrame):

    currentWidgetChanged = pyqtSignal(QWidget)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.hBoxLayout = QHBoxLayout(self)
        self.view = PopUpAniStackedWidget(self)

        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.hBoxLayout.addWidget(self.view)

        self.view.currentChanged.connect(
            lambda i: self.currentWidgetChanged.emit(self.view.widget(i)))

    def addWidget(self, widget):
        self.view.addWidget(widget)

    def setCurrentWidget(self, widget, popOut=True):
        widget.verticalScrollBar().setValue(0)
        if not popOut:
            self.view.setCurrentWidget(widget, duration=300)
        else:
            self.view.setCurrentWidget(
                widget, True, False, 200, QEasingCurve.InQuad)

    def setCurrentIndex(self, index, popOut=False):
        self.setCurrentWidget(self.view.widget(index), popOut)


class AMainWindow(FramelessWindow):

    def __init__(self):
        super().__init__()
        self.setTitleBar(CustomTitleBar(self))
        self.hBoxLayout = QHBoxLayout(self)
        self.widgetLayout = QHBoxLayout()

        self.stackWidget = StackedWidget(self)
        self.navigationInterface = NavigationInterface(self, True, True)

        self.adminStu = AdminStu(self)
        self.adminTea = AdminTea(self)
        self.adminCou = AdminCou(self)
        self.adminAccount = AdminAccount(self)
        self.settingInterface = SettingInterface(self)

        self.initLayout()

        self.initNavigation()
        self.initWindow()

    def initLayout(self):
        self.hBoxLayout.setSpacing(0)
        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.hBoxLayout.addWidget(self.navigationInterface)
        self.hBoxLayout.addLayout(self.widgetLayout)
        self.hBoxLayout.setStretchFactor(self.widgetLayout, 1)

        self.widgetLayout.addWidget(self.stackWidget)
        self.widgetLayout.setContentsMargins(0, 48, 0, 0)

        signalBus.switchToSampleCard.connect(self.switchToSample)

        self.navigationInterface.displayModeChanged.connect(
            self.titleBar.raise_)
        self.titleBar.raise_()

    def initNavigation(self):
        self.navigationInterface.addSeparator()

        self.addSubInterface(
            self.adminStu, 'adminStu', FIF.EDIT, self.tr('学生管理'))
        self.addSubInterface(
            self.adminTea, 'adminTea', FIF.INFO, self.tr('教师管理'))
        self.addSubInterface(
            self.adminCou, 'adminCou', FIF.DOCUMENT, self.tr('课程管理'))
        self.addSubInterface(
            self.adminAccount, 'adminAccount', FIF.FEEDBACK, self.tr('账户管理'))

        self.addSubInterface(
            self.settingInterface, 'settingInterface', FIF.SETTING, self.tr('设置'), NavigationItemPosition.BOTTOM)

        self.stackWidget.currentWidgetChanged.connect(self.onCurrentWidgetChanged)

        self.stackWidget.setCurrentIndex(0)

    def addSubInterface(self, interface: QWidget, objectName: str, icon, text: str,
                        position=NavigationItemPosition.SCROLL):
        interface.setObjectName(objectName)
        self.stackWidget.addWidget(interface)
        self.navigationInterface.addItem(
            routeKey=objectName,
            icon=icon,
            text=text,
            onClick=lambda t: self.switchTo(interface, t),
            position=position,
            tooltip=text
        )

    def initWindow(self):
        self.resize(1000, 780)
        self.setMinimumWidth(760)
        self.setWindowIcon(QIcon('UI/resource/login.png'))
        self.setWindowTitle("Welcome to Student Management System,Admin!")

        self.titleBar.setAttribute(Qt.WA_StyledBackground)

        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)

        StyleSheet.MAIN_WINDOW.apply(self)

    def switchTo(self, widget, triggerByUser=True):
        self.stackWidget.setCurrentWidget(widget, not triggerByUser)

    def onCurrentWidgetChanged(self, widget: QWidget):
        self.navigationInterface.setCurrentItem(widget.objectName())
        qrouter.push(self.stackWidget, widget.objectName())

    def resizeEvent(self, e):
        self.titleBar.move(46, 0)
        self.titleBar.resize(self.width() - 46, self.titleBar.height())



    def switchToSample(self, routeKey, index):
        interfaces = self.findChildren(GalleryInterface)
        for w in interfaces:
            if w.objectName() == routeKey:
                self.stackWidget.setCurrentWidget(w, False)
                w.scrollToCard(index)

# coding: utf-8
from PyQt5.QtCore import Qt, pyqtSignal, QEasingCurve, QUrl
from PyQt5.QtGui import QIcon, QDesktopServices
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QFrame, QWidget
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import (NavigationInterface, NavigationItemPosition, PopUpAniStackedWidget, qrouter)
from UI.global_var import globalVal
from .gallery_interface import GalleryInterface
from .info_score import InfoScore
from .info_students import InfoStudents
from .info_account import InfoAccount
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


class SMainWindow(FramelessWindow):

    def __init__(self):
        super().__init__()
        self.setTitleBar(CustomTitleBar(self))
        self.hBoxLayout = QHBoxLayout(self)
        self.widgetLayout = QHBoxLayout()

        self.stackWidget = StackedWidget(self)
        self.navigationInterface = NavigationInterface(self, True, True)

        self.infoStudents = InfoStudents(self)
        self.infoScore = InfoScore(self)
        self.infoAccount = InfoAccount(self)

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
        signalBus.supportSignal.connect(self.onSupport)

        self.navigationInterface.displayModeChanged.connect(
            self.titleBar.raise_)
        self.titleBar.raise_()

    def initNavigation(self):
        self.navigationInterface.addSeparator()

        self.addSubInterface(
            self.infoStudents, 'infoStudents', FIF.INFO, self.tr('学生数据'))
        self.addSubInterface(
            self.infoScore, 'infoScore', FIF.VIEW, self.tr('成绩查询'))
        self.addSubInterface(
            self.infoAccount, 'infoAccount', FIF.MORE, self.tr('账户信息'))

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
        self.setWindowTitle(f"Welcome to Student Management System,{globalVal.global_list[0]}!")

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

    def onSupport(self):
        QDesktopServices.openUrl(QUrl(SUPPORT_URL))

    def switchToSample(self, routeKey, index):

        interfaces = self.findChildren(GalleryInterface)
        for w in interfaces:
            if w.objectName() == routeKey:
                self.stackWidget.setCurrentWidget(w, False)
                w.scrollToCard(index)

# coding:utf-8
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QWidget, QLabel
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import InfoBar
from qfluentwidgets import (SettingCardGroup, OptionsSettingCard, ScrollArea,
                            ExpandLayout, CustomColorSettingCard,
                            setTheme, setThemeColor)

from ..common.config import cfg
from ..common.style_sheet import StyleSheet


class SettingInterface(ScrollArea):


    checkUpdateSig = pyqtSignal()
    musicFoldersChanged = pyqtSignal(list)
    acrylicEnableChanged = pyqtSignal(bool)
    downloadFolderChanged = pyqtSignal(str)
    minimizeToTrayChanged = pyqtSignal(bool)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.scrollWidget = QWidget()
        self.expandLayout = ExpandLayout(self.scrollWidget)

        self.settingLabel = QLabel(self.tr("设置"), self)
        self.personalGroup = SettingCardGroup(
            self.tr('个性化'), self.scrollWidget)
        self.themeCard = OptionsSettingCard(
            cfg.themeMode,
            FIF.BRUSH,
            self.tr('主题'),
            self.tr("改变主题色"),
            texts=[
                self.tr('明亮'), self.tr('黑暗'),
                self.tr('跟随系统')
            ],
            parent=self.personalGroup
        )
        self.themeColorCard = CustomColorSettingCard(
            cfg.themeColor,
            FIF.PALETTE,
            self.tr('主题色'),
            self.tr('改变应用主题色'),
            self.personalGroup
        )
        self.zoomCard = OptionsSettingCard(
            cfg.dpiScale,
            FIF.ZOOM,
            self.tr("控件缩放"),
            self.tr("改变控件及字体的显示大小"),
            texts=[
                "100%", "125%", "150%", "175%", "200%",
                self.tr("跟随系统")
            ],
            parent=self.personalGroup
        )
        self.__initWidget()

    def __initWidget(self):
        self.resize(1000, 800)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setViewportMargins(0, 80, 0, 20)
        self.setWidget(self.scrollWidget)
        self.setWidgetResizable(True)

        self.scrollWidget.setObjectName('scrollWidget')
        self.settingLabel.setObjectName('settingLabel')
        StyleSheet.SETTING_INTERFACE.apply(self)

        self.__initLayout()
        self.__connectSignalToSlot()

    def __initLayout(self):
        self.settingLabel.move(36, 30)
        self.personalGroup.addSettingCard(self.themeCard)
        self.personalGroup.addSettingCard(self.themeColorCard)
        self.personalGroup.addSettingCard(self.zoomCard)
        self.expandLayout.setSpacing(28)
        self.expandLayout.setContentsMargins(36, 10, 36, 0)
        self.expandLayout.addWidget(self.personalGroup)


    def __showRestartTooltip(self):
        InfoBar.success(
            self.tr('Updated successfully'),
            self.tr('Configuration takes effect after restart'),
            duration=1500,
            parent=self
        )

    # def __onDownloadFolderCardClicked(self):
    #
    #     folder = QFileDialog.getExistingDirectory(
    #         self, self.tr("Choose folder"), "./")
    #     if not folder or cfg.get(cfg.downloadFolder) == folder:
    #         return
    #
    #     cfg.set(cfg.downloadFolder, folder)
    #     self.downloadFolderCard.setContent(folder)

    def __connectSignalToSlot(self):
        cfg.appRestartSig.connect(self.__showRestartTooltip)
        cfg.themeChanged.connect(setTheme)
        self.themeColorCard.colorChanged.connect(setThemeColor)


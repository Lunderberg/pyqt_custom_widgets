from PyQt4 import QtGui, QtCore

class BetterTabBar(QtGui.QTabBar):
    tabClicked = QtCore.pyqtSignal(int)

    def mousePressEvent(self, mouseEvent):
        tab_index = self.tabAt(mouseEvent.pos())
        self.tabClicked.emit(tab_index)
        super(BetterTabBar, self).mousePressEvent(mouseEvent)

class CollapsibleTabWidget(QtGui.QTabWidget):
    tabClicked = QtCore.pyqtSignal(int)
    collapsedChanged = QtCore.pyqtSignal(bool)

    def __init__(self, *args, **kwargs):
        super(CollapsibleTabWidget, self).__init__(*args, **kwargs)

        self.setTabBar(BetterTabBar(self))
        self.tabBar().tabClicked.connect(self._tabClicked)

    def _tabClicked(self, index):
        self.tabClicked.emit(index)
        if index == self.currentIndex() or self.collapsed:
            self.collapsed = not self.collapsed

    def getCollapsed(self):
        max_size = (self.maximumSize().width(),
                    self.maximumSize().height())
        return max_size == self._collapsed_size()

    def setCollapsed(self, val):
        if val:
            self.setMaximumSize(*self._collapsed_size())
        else:
            self.setMaximumSize(16777215, 16777215)
        self.collapsedChanged.emit(val)

    collapsed = QtCore.pyqtProperty(bool, getCollapsed, setCollapsed)

    def _collapsed_size(self):
        tabs_on_side = self.tabPosition() in [QtGui.QTabWidget.West,
                                              QtGui.QTabWidget.East]
        if self.tabBar().count() == 0:
            self.tabBar().addTab('dummy')
            tab_bar_size = self.tabBar().sizeHint()
            self.tabBar().removeTab(0)
        else:
            tab_bar_size = self.tabBar().sizeHint()

        if tabs_on_side:
            return (tab_bar_size.width() + 4, 16777215)
        else:
            return (16777215, tab_bar_size.height() + 4)

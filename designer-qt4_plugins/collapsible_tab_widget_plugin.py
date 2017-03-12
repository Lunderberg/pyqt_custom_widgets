#============================================================================#
# PyQt4 port of the designer/containerextension example from Qt v4.x         #
#----------------------------------------------------------------------------#
from PyQt4 import QtGui, QtDesigner
import sip

from custom_widgets.collapsible_tab_widget import CollapsibleTabWidget

Q_TYPEID = {'QPyDesignerContainerExtension':     'com.trolltech.Qt.Designer.Container',
            'QPyDesignerPropertySheetExtension': 'com.trolltech.Qt.Designer.PropertySheet',
            'QPyDesignerTaskMenuExtension':      'com.trolltech.Qt.Designer.TaskMenu',
            'QPyDesignerMemberSheetExtension':   'com.trolltech.Qt.Designer.MemberSheet'}


#============================================================================#
# ContainerExtension                                                         #
#----------------------------------------------------------------------------#
class CTabWidgetContainerExtension(QtDesigner.QPyDesignerContainerExtension):
    def __init__(self, widget, parent=None):
        super(CTabWidgetContainerExtension, self).__init__(parent)

        self._widget = widget

    def addWidget(self, widget):
        self._widget.addPage(widget)

    def count(self):
        return self._widget.count()

    def currentIndex(self):
        return self._widget.currentIndex()

    def insertWidget(self, index, widget):
        self._widget.insertPage(index, widget)

    def remove(self, index):
        self._widget.removePage(index)

    def setCurrentIndex(self, index):
        self._widget.setCurrentIndex(index)

    def widget(self, index):
        return self._widget.widget(index)


#============================================================================#
# ExtensionFactory                                                           #
#----------------------------------------------------------------------------#
class CTabWidgetExtensionFactory(QtDesigner.QExtensionFactory):
    def __init__(self, parent=None):
        super(CTabWidgetExtensionFactory, self).__init__(parent)

    def createExtension(self, obj, iid, parent):
        if iid != Q_TYPEID['QPyDesignerContainerExtension']:
            return None
        if isinstance(obj, CollapsibleTabWidget):
            return CTabWidgetContainerExtension(obj, parent)
        return None


#============================================================================#
# CustomWidgetPlugin                                                         #
#----------------------------------------------------------------------------#
class CTabWidgetPlugin(QtDesigner.QPyDesignerCustomWidgetPlugin):

    def __init__(self, parent=None):
        super(CTabWidgetPlugin, self).__init__(parent)

        self.initialized = False

    def initialize(self, formEditor):
        if self.initialized:
            return
        manager = formEditor.extensionManager()
        if manager:
            self.factory = CTabWidgetExtensionFactory(manager)
            manager.registerExtensions(self.factory, Q_TYPEID['QPyDesignerContainerExtension'])
        self.initialized = True

    def isInitialized(self):
        return self.initialized

    def createWidget(self, parent):
        widget = CollapsibleTabWidget(parent)
        widget.currentChanged.connect(self.currentChanged)
        widget.collapsedChanged.connect(self.collapsedChanged)
        # widget.currentIndexChanged.connect(self.currentIndexChanged)
        # widget.pageTitleChanged.connect(self.pageTitleChanged)
        return widget

    def name(self):
        return "CollapsibleTabWidget"

    def group(self):
        return "PyQt Examples"

    def icon(self):
        return QtGui.QIcon()

    def toolTip(self):
        return ""

    def whatsThis(self):
        return ""

    def isContainer(self):
        return True

    def domXml(self):
        return ('<widget class="CollapsibleTabWidget" name="coltabwidget">'
                '  <widget class="QWidget" name="page" />'
                '</widget>')

    def includeFile(self):
        return "custom_widgets.collapsible_tab_widget"

    def currentChanged(self, index):
        widget = self.sender()
        if widget and isinstance(widget, CollapsibleTabWidget):
            form = QtDesigner.QDesignerFormWindowInterface.findFormWindow(widget)
            if form:
                form.setDirty(True)

    def collapsedChanged(self, state):
        widget = self.sender()
        if widget and isinstance(widget, CollapsibleTabWidget):
            form = QtDesigner.QDesignerFormWindowInterface.findFormWindow(widget)
            if form:
                form.setDirty(True)


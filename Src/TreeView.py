from PySide2 import QtCore
from PySide2 import QtWidgets
from shiboken2 import wrapInstance

import maya.OpenMaya as om
import maya.cmds as cmds
import maya.OpenMayaUI as omui
'''
如何在第二次开启窗口时，在上一次的关闭的位置
'''

def maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)


class TreeViewDialog(QtWidgets.QDialog):
    def __init__(self, parent=maya_main_window()):
        super(TreeViewDialog, self).__init__(parent)

        self.setWindowTitle("TreeViewDialog")
        self.setMinimumSize(500,400)

        self.create_widgets()
        self.create_layout()
        self.create_connection()


    def create_widgets(self):
        root_path = "{0}scripts".format(cmds.internalVar(userAppDir=True))
        self.model =QtWidgets.QFileSystemModel()
        self.model.setRootPath(root_path)

        self.tree_view = QtWidgets.QTreeView()
        self.tree_view.setModel(self.model)
        self.tree_view.setRootIndex(self.model.index(root_path))
        self.tree_view.hideColumn(1)
        self.tree_view.setColumnWidth(0,240)

        # self.model.setFilter(QtCore.QDir.Dirs | QtCore.QDir.NoDotAndDotDot)

        # self.model.setNaneFilters(["*.py"])
        # self.model.setNameFilterDisables(False)
    def create_layout(self):
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(2,2,2,2)
        main_layout.addWidget(self.tree_view)


    def create_connection(self):
        self.tree_view.doubleClicked.connect(self.on_double_clicked)
    def on_double_clicked(self, index):
        path = self.model.filePath(index)
        if self.model.isDir(index):
            print("Directory selected: {0}".format(path))
        else:
            print("Directory selected:  {0}".format(path))




if __name__ == "__main__":

    try:
        d.close()
        d.deleterLater()
    except:
        pass
    d = TreeViewDialog()
    d.show()
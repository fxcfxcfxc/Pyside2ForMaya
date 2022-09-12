from PySide2 import QtCore
from PySide2 import QtWidgets
from shiboken2 import wrapInstance

import maya.OpenMaya as om
import maya.cmds as cmds
import maya.OpenMayaUI as omui

#得到maya窗口
def maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)


class TestDialog(QtWidgets.QDialog):

    ATTR_ROLE = QtCore.Qt.UserRole
    VALUE_ROLE = QtCore.Qt.UserRole+1

    def __init__(self, parent=maya_main_window()):
        super(TestDialog, self).__init__(parent)

        self.setWindowTitle("Test Dialog")
        self.setMinimumWidth(600)

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

    #----------------------创建组件-----------#
    def create_widgets(self):

        # 创建table
        self.table_wdg =QtWidgets.QTableWidget()
        # 设置table属性
        self.table_wdg.setColumnCount(5)
        self.table_wdg.setColumnWidth(0, 22)
        self.table_wdg.setColumnWidth(2, 70)
        self.table_wdg.setColumnWidth(3, 70)
        self.table_wdg.setColumnWidth(4, 70)
        self.table_wdg.setHorizontalHeaderLabels( ["", "Name", "TransX", "TransY", "TransZ"] )
        header_view = self.table_wdg.horizontalHeader()
        header_view.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)


        # 按钮
        self.button_Refresh = QtWidgets.QPushButton("Refresh")
        self.button_Close = QtWidgets.QPushButton("Close")

    #-----------------------设置布局----------------#
    def create_layouts(self):


        #----------------------------------------按钮布局
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.button_Refresh)
        button_layout.addWidget(self.button_Close)


        # ---------------------------------------最上层 布局
        main_layout = QtWidgets.QVBoxLayout(self)
        # 设置布局边界
        main_layout.setContentsMargins(2,2,2,2)
        main_layout.setSpacing(2)
        #  添加table控件对象
        main_layout.addWidget(self.table_wdg)
        main_layout.addStretch()
        main_layout.addLayout(button_layout)

    #-------------------------链接信号与槽-----------#
    def create_connections(self):
        self.button_Refresh.clicked.connect(self.refresh)
        self.button_Close.clicked.connect(self.close)
        pass
    # ---------------------重写showevent事件--------------#
    def showEvent(self, e):
        super(TestDialog, self).showEvent(e)
        self.refresh()

    def refresh(self):
        # 初始化QTableWidget 行数为0
        self.table_wdg.setRowCount(0)

        # 返回场景中类型为mesh node的列表
        meshes = cmds.ls(type="mesh")

        # 遍历meshes对象
        for i in range(len(meshes)):

            # 有可能有子节点，返回第一个node父级节点
            transform_name = cmds.listRelatives( meshes[i], parent=True )[0]

            # 获得node 的 translate属性
            translation = cmds.getAttr("{0}.translate".format(transform_name))[0]

            # 获得node 的 visibility属性
            visible = cmds.getAttr( "{0}.visibility".format(transform_name) )
            # 插入QTableWidget 一行
            self.table_wdg.insertRow(i)

            # 插入名字信息到行列的位置
            self.insert_item(i, 1, transform_name)

    def insert_item(self, row, column, text):
        item = QtWidgets.QTableWidgetItem(text)
        self.table_wdg.setItem(row, column, item)


    def set_item_text(self, item, text):
        return item.text();

    def set_item_checked(self, item, checked):
        if checked:
            item.setCheckState(QtCore.Qt.Checked)
        else:
            item.setCheckState(QtCore.Qt.Unchecked)

    def is_item_checked(self, item):
        return item.checkState() == QtCore.Qt.Checked


if __name__ == "__main__":
    try:
        d.close()
        d.deleteLater()

    except:
        pass

    d = TestDialog()
    d.show()
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
        self.setMinimumWidth(500)

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

    #----------------------创建组件-----------#
    def create_widgets(self):

        # 创建table
        self.table_wdg =QtWidgets.QTableWidget()
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
        self.table_wdg.cellChanged.connect(self.on_cell_changed)


    def set_cell_changed_connection_enabled(self, enabled):
        if enabled:
            self.table_wdg.cellChanged.connect(self.on_cell_changed)
        else:
            self.table_wdg.cellChanged.disconnect(self.on_cell_changed)

    # ---------------------重写showevent事件--------------#
    def showEvent(self, e):
        super(TestDialog, self).showEvent(e)
        self.refresh()

    #--------------------重写事件 前界面 按键失效-------------------#
    def keyPressEvent(self, e):
        super(TestDialog,self).showEvent(e)
        e.accept()

    #---------------------------槽函数：当界面发生改变，更新场景数据-------------------------------#
    def on_cell_changed(self,row, column):
        self.set_cell_changed_connection_enabled(False)
        print("TODO: on_cell_changed")
        item = self.table_wdg.item(row, column)
        # 判断用户修改的是否是第一列的项
        if column ==1:
            self.rename(item)

        else:
            is_boolean = column ==0
            self.update_attr(self.get_full_attr_name(row, item), item, is_boolean)
        self.set_cell_changed_connection_enabled(True)


    # ---------------------槽函数：刷新场景-------------------------------#
    def refresh(self):
        self.set_cell_changed_connection_enabled(False)
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
            # 插入元素到行列的位置
            self.insert_item(i, 0, "", "visibility", visible, True)
            self.insert_item(i, 1, transform_name, None, transform_name, False)
            self.insert_item(i, 2, self.float_to_string( translation[0] ), "tx", translation[0], False)
            self.insert_item(i, 3, self.float_to_string( translation[1] ), "ty", translation[1], False)
            self.insert_item(i, 4, self.float_to_string( translation[2] ) , "tz", translation[2], False)

        self.set_cell_changed_connection_enabled(True)




    #----------------------添加项------------------------------#
    def insert_item(self, row, column, text, attr, value, is_boolean):
        item = QtWidgets.QTableWidgetItem(text)
        self.set_item_attr(item, attr)
        self.set_item_value(item, value)
        if is_boolean:
            item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            self.set_item_checked(item, value)

        self.table_wdg.setItem(row, column, item)

    #-----------------------修改名字-------------------------------#
    def rename(self, item):

        old_name = self.get_item_value(item)
        new_name = self.get_item_text(item)
        if old_name != new_name:
            actual_new_name = cmds.rename(old_name, new_name)
            if actual_new_name != new_name:
                self.set_item_text(item, actual_new_name)

            self.set_item_value(item, actual_new_name)

    # ----------------------更新值-------------------------------#
    def update_attr(self, attr_name, item, is_boolean):
        if is_boolean:
            value = self.is_item_checked(item)
            self.set_item_text(item,"")
        else:
            text = self.get_item_text(item)
            try:
                value = float(text)
            except ValueError:
                self.revert_original_value(item, is_boolean)
                return

        try:
            cmds.setAttr(attr_name, value)
        except:
            self.revert_original_value(item, is_boolean)
            return
        new_value = cmds.getAttr(attr_name)
        if is_boolean:
            self.set_item_text(item, self.float_to_string(new_value))
        else:
            self.set_item_text(item, self.float_to_string(new_value))
        self.set_item_value(item, new_value)


    def get_full_attr_name(self, row, item):
        node_name = self.table_wdg.item(row, 1).data(self.VALUE_ROLE)
        attr_name = self.get_item_attr(item)
        return "{0}.{1}".format(node_name, attr_name)

    def revert_original_value(self, item , is_boolean):
        original_value = self.get_item_value(item)
        if is_boolean:
            self.set_item_checked(item, original_value)
        else:
            self.set_item_text(item, self.float_to_string(original_value))

    # ---------------------------item设置Text-------------------------#
    def set_item_text(self, item, text):
        item.setText(text)
    def get_item_text(self, item):
        return item.text()

    # ---------------------------item设置Check-------------------------#
    def set_item_checked(self, item, checked):
        if checked:
            item.setCheckState(QtCore.Qt.Checked)
        else:
            item.setCheckState(QtCore.Qt.Unchecked)

    def is_item_checked(self, item):
        return item.checkState() == QtCore.Qt.Checked

    # ---------------------------item设置Attribute-------------------------#
    def set_item_attr(self, item, attr):
        item.setData(self.ATTR_ROLE, attr)
    def get_item_attr(self, item):
        return item.data(self.ATTR_ROLE)

    # ----------------------get Set Item Value----------#
    def set_item_value(self, item, value):
        item.setData(self.VALUE_ROLE, value)
    def get_item_value(self, item):
        return item.data(self.VALUE_ROLE)
    # -------------------------float 转 string--------------#
    def float_to_string(self, value):
        return "{0:.4f}".format(value)

if __name__ == "__main__":
    try:
        d.close()
        d.deleteLater()

    except:
        pass

    d = TestDialog()
    d.show()
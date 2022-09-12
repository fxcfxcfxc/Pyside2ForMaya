from PySide2 import QtCore
from PySide2 import QtWidgets
from shiboken2 import wrapInstance

import maya.OpenMaya as om
import maya.cmds as cmds
import maya.OpenMayaUI as omui

#�õ�maya����
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

    #----------------------�������-----------#
    def create_widgets(self):

        # ����table
        self.table_wdg =QtWidgets.QTableWidget()
        # ����table����
        self.table_wdg.setColumnCount(5)
        self.table_wdg.setColumnWidth(0, 22)
        self.table_wdg.setColumnWidth(2, 70)
        self.table_wdg.setColumnWidth(3, 70)
        self.table_wdg.setColumnWidth(4, 70)
        self.table_wdg.setHorizontalHeaderLabels( ["", "Name", "TransX", "TransY", "TransZ"] )
        header_view = self.table_wdg.horizontalHeader()
        header_view.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)


        # ��ť
        self.button_Refresh = QtWidgets.QPushButton("Refresh")
        self.button_Close = QtWidgets.QPushButton("Close")

    #-----------------------���ò���----------------#
    def create_layouts(self):


        #----------------------------------------��ť����
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.button_Refresh)
        button_layout.addWidget(self.button_Close)


        # ---------------------------------------���ϲ� ����
        main_layout = QtWidgets.QVBoxLayout(self)
        # ���ò��ֱ߽�
        main_layout.setContentsMargins(2,2,2,2)
        main_layout.setSpacing(2)
        #  ���table�ؼ�����
        main_layout.addWidget(self.table_wdg)
        main_layout.addStretch()
        main_layout.addLayout(button_layout)

    #-------------------------�����ź����-----------#
    def create_connections(self):
        self.button_Refresh.clicked.connect(self.refresh)
        self.button_Close.clicked.connect(self.close)
        pass
    # ---------------------��дshowevent�¼�--------------#
    def showEvent(self, e):
        super(TestDialog, self).showEvent(e)
        self.refresh()

    def refresh(self):
        # ��ʼ��QTableWidget ����Ϊ0
        self.table_wdg.setRowCount(0)

        # ���س���������Ϊmesh node���б�
        meshes = cmds.ls(type="mesh")

        # ����meshes����
        for i in range(len(meshes)):

            # �п������ӽڵ㣬���ص�һ��node�����ڵ�
            transform_name = cmds.listRelatives( meshes[i], parent=True )[0]

            # ���node �� translate����
            translation = cmds.getAttr("{0}.translate".format(transform_name))[0]

            # ���node �� visibility����
            visible = cmds.getAttr( "{0}.visibility".format(transform_name) )
            # ����QTableWidget һ��
            self.table_wdg.insertRow(i)

            # ����������Ϣ�����е�λ��
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
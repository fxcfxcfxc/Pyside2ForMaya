from PySide2 import QtCore
from PySide2 import QtWidgets
from shiboken2 import wrapInstance

import maya.OpenMayaUI as omui


def maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)


class TestDialog(QtWidgets.QDialog):
    def __init__(self, parent=maya_main_window()):
        super(TestDialog, self).__init__(parent)

        self.setWindowTitle("Test Dialog")
        self.setMinimumWidth(200)
        self.create_widgets()
        self.create_layouts()

    # 创建组件
    def create_widgets(self):
        self.lineedit = QtWidgets.QLineEdit()
        self.checkbox_00 = QtWidgets.QCheckBox("CheckBox1")
        self.checkbox_01 = QtWidgets.QCheckBox("CheckBox2")
        self.button_00 = QtWidgets.QPushButton("Button1")
        self.button_01 = QtWidgets.QPushButton("Button2")

    # 设置布局
    def create_layouts(self):
        # 设置form 布局
        form_layout = QtWidgets.QFormLayout()
        form_layout.addRow("Name:", self.lineedit)
        form_layout.addRow("Hidden:", self.checkbox_00)
        form_layout.addRow("Hidden:", self.checkbox_01)

        # 设置按钮 的布局
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.button_00)
        button_layout.addWidget(self.button_01)

        # 总布局 添加其他布局
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)


if __name__ == "__main__":
    d = TestDialog()
    d.show()
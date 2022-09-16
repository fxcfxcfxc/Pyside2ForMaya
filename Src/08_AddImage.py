from PySide2 import QtCore
from PySide2 import QtWidgets,QtGui
from shiboken2 import wrapInstance

import maya.OpenMaya as om
import maya.cmds as cmds
import maya.OpenMayaUI as omui


def maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)


class ImageDialog(QtWidgets.QDialog):
    def __init__(self, parent=maya_main_window()):
        super(ImageDialog, self).__init__(parent)

        self.setWindowTitle("ImageDialog")
        self.setMinimumSize(300,80)

        self.create_widgets()
        self.create_layout()
        self.create_connection()


    def create_widgets(self):
        self.create_title_label()
        self.spin_box = QtWidgets.QSpinBox()
        self.spin_box.setFixedWidth(80)
        self.spin_box.setMinimum(-100)
        self.spin_box.setMaximum(100)
        self.spin_box.setSingleStep(5)
        self.spin_box.setPrefix("&")
        self.spin_box.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)

        self.double_spin_box = QtWidgets.QDoubleSpinBox()
        self.double_spin_box.setFixedWidth(80)
        self.double_spin_box.setRange(-50.0,50.0)
        self.double_spin_box.setSuffix(" m")


    def create_title_label(self):
        image_path = "../icon/Snipaste.png"


        # image = QtGui.QImage(image_path)
        # image = image.scaled(280,60,QtCore.Qt.IgnoreAspectRatio, QtCore.Qt.SmoothTransformation)

        # pixmap = QtGui.QPixmap()
        # pixmap.convertFromImage(image)

        self.title_label = QtWidgets.QLabel("My Awesome Utility")
        self.title_label.setPixmap(image_path)


    def create_layout(self):
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addWidget(self.title_label)
        # main_layout.addRow("Spin Box: ", self.spin_box)
        # main_layout.addRow("Double Spin Box: ", self.double_spin_box)

    def create_connection(self):
        self.spin_box.valueChanged.connect(self.print_value)
        self.double_spin_box.valueChanged.connect(self.print_value)


    def print_value(self,value):
        print("value: {0}".format(value))

if __name__ == "__main__":
    d = ImageDialog()
    d.show()
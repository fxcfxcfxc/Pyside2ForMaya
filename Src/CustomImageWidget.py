from PySide2 import QtCore
from PySide2 import QtWidgets,QtGui
from shiboken2 import wrapInstance

import maya.OpenMaya as om
import maya.cmds as cmds
import maya.OpenMayaUI as omui


def maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)


# -------------------------------CustomImageWidget类---------------------------------------#
class CustomImageWidget(QtWidgets.QWidget):
    def __init__(self, width, height, image_path, parent=None):
        super(CustomImageWidget, self).__init__(parent)
        self.set_size(width,height)
        self.set_image(image_path)
        self.set_background_color(QtCore.Qt.black)

    def set_size(self, width, height):
        self.setFixedSize(width, height)

    def set_image(self, image_path):
        image = QtGui.QImage(image_path)
        image = image.scaled(self.width(),self.height(), QtCore.Qt.IgnoreAspectRatio, QtCore.Qt.SmoothTransformation)

        self.pixmap = QtGui.QPixmap()
        self.pixmap.convertFromImage(image)

    def set_background_color(self, color):
        self.background_color = color


    # --------------------------重写事件--------------------------#
    def paintEvent(self, event):
        painter = QtGui.QPainter(self)

        painter.fillRect(0,0, self.width(), self.height(),self.background_color)
        painter.drawPixmap(self.rect(), self.pixmap)


# -------------------------------ImageDialog类---------------------------------------#
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
        image_path = "../icon/icon.png"

        self.title_label = CustomImageWidget(280, 60, image_path)
        self.title_label.set_background_color(QtCore.Qt.red)

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
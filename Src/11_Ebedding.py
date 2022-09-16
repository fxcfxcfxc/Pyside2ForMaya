from PySide2 import QtCore
from PySide2 import QtWidgets,QtGui
from shiboken2 import wrapInstance

import maya.OpenMaya as om
import maya.cmds as cmds
import maya.OpenMayaUI as omui
'''
可视化颜色控件  maya选色窗口

'''

def maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)


# ---------------------------------------------------------------------#
class CustomColorButton(QtWidgets.QLabel):

    # ------------------------------自定义信号------------------#
    color_changed = QtCore.Signal()

    def __init__(self, color = QtCore.Qt.white, parent=None):
        super(CustomColorButton, self).__init__(parent)
        self._color = QtGui.QColor()
        self.set_size(50,14)
        self.set_color(color)

    def set_size(self, width, height):
        self.setFixedSize(width, height)

    def set_color(self, color):
        color = QtGui.QColor(color)

        if self._color !=color:
            self._color = color
            pixmap = QtGui.QPixmap(self.size())
            pixmap.fill(self._color)
            self.setPixmap(pixmap)

            self.color_changed.emit()

    def get_color(self):
        return self._color

    def select_color(self):
        color = QtWidgets.QColorDialog.getColor(self.get_color(), self, options = QtWidgets.QColorDialog.DontUseNativeDialog)
        if color.isValid():
            self.set_color(color)


    def mouseReleaseEvent(self, ev):
        if ev.button() == QtCore.Qt.LeftButton:
            self.select_color()



# -------------------------------ImageDialog类---------------------------------------#
class ColorDialog(QtWidgets.QDialog):
    def __init__(self, parent=maya_main_window()):
        super(ColorDialog, self).__init__(parent)

        self.setWindowTitle("ImageDialog")
        self.setMinimumSize(300,80)

        self.create_widgets()
        self.create_layout()
        self.create_connection()


    def create_widgets(self):
        self.c1= CustomColorButton(QtCore.Qt.white)
        self.c2 = CustomColorButton(QtCore.Qt.black)



    def create_layout(self):
        main_layout = QtWidgets.QFormLayout(self)
        main_layout.addRow("foreground", self.c1)
        main_layout.addRow("background", self.c2)


    def create_connection(self):
        self.c1.color_changed.connect(self.print)
        pass


    def print(self):
        color= self.c1.get_color()
        print("{0}".format(color.red()))


if __name__ == "__main__":
    d = ColorDialog()
    d.show()
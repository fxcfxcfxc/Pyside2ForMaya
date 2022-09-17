from functools import partial
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
class CustomColorButton(QtWidgets.QWidget):

    # ------------------------------自定义信号------------------#
    color_changed = QtCore.Signal(QtGui.QColor)

    def __init__(self, color = QtCore.Qt.white, parent=None):
        super(CustomColorButton, self).__init__(parent)

        self.setObjectName("CustomColorButton")
        # self._color = QtGui.QColor()
        self.create_control()
        self.set_size(50,14)
        self.set_color(color)


    def create_control(self):
        #---
        window = cmds.window()
        color_slider_name = cmds.colorSliderGrp()
        #-----
        self.color_slider_obj = omui.MQtUtil.findControl(color_slider_name)
        if self.color_slider_obj:
            self._color_slider_widget = wrapInstance(int(self.color_slider_obj), QtWidgets.QWidget)

            #-----
            main_layout = QtWidgets.QVBoxLayout(self)
            main_layout.setObjectName("main_layout")
            main_layout.setContentsMargins(0,0,0,0)
            main_layout.addWidget(self._color_slider_widget)


            # self._name = omui.MQtUtil.fullName(int(color_slider_obj))
            # children = self._color_slider_widget.children()
            self._slider_widget = self._color_slider_widget.findChild(QtWidgets.QWidget, "slider")
            if self._slider_widget:
                self._slider_widget.hide()
            self._color_widget = self._color_slider_widget.findChild(QtWidgets.QWidget, "port")

            cmds.colorSliderGrp( self.get_full_name(), e =True, changeCommand = partial(self.on_color_changed) )

        #-----
        cmds.deleteUI(window,window = True)

    def get_full_name(self):
        return omui.MQtUtil.fullName( int(self.color_slider_obj) )

    def set_size(self, width, height):
        self._color_slider_widget.setFixedWidth(width)
        self._color_widget.setFixedHeight(height)

    def set_color(self, color):
        color = QtGui.QColor(color)
        cmds.colorSliderGrp(self.get_full_name(), e =True, rgbValue = ( color.redF(), color.greenF(), color.blueF() ) )
        self.on_color_changed()

    def get_color(self):
        color = cmds.colorSliderGrp(self.get_full_name(), q = True, rgbValue = True)
        color =QtGui.QColor(color[0] * 255, color[1] * 255, color[2] * 255)

        return color

    def on_color_changed(self, *args):
        self.color_changed.emit(self.get_color())





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


    def print(self):
        color= self.c1.get_color()
        print("{0}".format(color.red()))


if __name__ == "__main__":
    d = ColorDialog()
    d.show()
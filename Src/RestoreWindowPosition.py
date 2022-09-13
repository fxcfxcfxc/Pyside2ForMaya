from PySide2 import QtCore
from PySide2 import QtWidgets
from shiboken2 import wrapInstance

import maya.OpenMayaUI as omui
'''
如何在第二次开启窗口时，在上一次的关闭的位置
'''

def maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)


class SpinBoxDialog(QtWidgets.QDialog):
    def __init__(self, parent=maya_main_window()):
        super(SpinBoxDialog, self).__init__(parent)

        self.setWindowTitle("Spin Box Dialog")
        # self.setMinimumWidth(200)

        self.create_widgets()
        self.create_layout()
        self.create_connection()
        self.geometry = None

    def create_widgets(self):
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


    def create_layout(self):
        main_layout = QtWidgets.QFormLayout(self)
        main_layout.addRow("Spin Box: ", self.spin_box)
        main_layout.addRow("Double Spin Box: ", self.double_spin_box)

    def create_connection(self):
        self.spin_box.valueChanged.connect(self.print_value)
        self.double_spin_box.valueChanged.connect(self.print_value)


    def showEvent(self,e):
        super(SpinBoxDialog,self).showEvent(e)
        if self.geometry:
            self.restorGeometry(self.geometry)

    def closeEvent(self,e):
        if isinstance(self,SpinBoxDialog):
            super(SpinBoxDialog, self).closeEvent(e)
            self.geometry = self.saveGeometry()

    def print_value(self,value):
        print("value: {0}".format(value))

if __name__ == "__main__":

    try:
        d.close()
        d.deleterLater()
    except:
        pass
    d = SpinBoxDialog()
    d.show()
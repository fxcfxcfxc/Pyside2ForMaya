from PySide2 import QtWidgets, QtGui, QtCore
from shiboken2 import wrapInstance

import maya.OpenMaya as om
import maya.cmds as cmds
import maya.OpenMayaUI as omui

def maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)


# ------------------------------------#
class LightItem(QtWidgets.QWidget):
    SUPPORTED_TYPES = ["ambientLight","directionalLight","pointLight", "spotLight"]
    EMIT_TYPES = ["directionalLight","pointLight", "spotLight"]

    def __init__(self, shape_name, parent = None):
        super(LightItem,self).__init__(parent)

        self.setFixedHeight(26)
        self.create_widgets()
        self.create_layout()
        self.create_connections()


    def create_widgets(self):
        self.light_type_btn = QtWidgets.QPushButton()
        self.light_type_btn.setFixedSize(20,20)
        self.visiblity_cb = QtWidgets.QCheckBox()

        self.transform_name_label = QtWidgets.QLabel("placeholder")
        self.transform_name_label.setFixedWidth(120)
        self.transform_name_label.setAlignment(QtCore.Qt.AlignCenter)

    def create_layout(self):
        main_layout = QtWidgets.QHBoxLayout(self)
        main_layout.setContentsMargins(0,0,0,0)
        main_layout.addWidget(self.light_type_btn)
        main_layout.addWidget(self.visiblity_cb)
        main_layout.addWidget(self.transform_name_label)

        main_layout.addStretch()


    def create_connections(self):
        pass
# ------------------------------------#
class LightPanel(QtWidgets.QDialog):
    WINDOW_TITLE = "Light Panel"

    def __init__(self, parent = maya_main_window()):
        super(LightPanel, self).__init__(parent)

        self.setWindowTitle(self.WINDOW_TITLE)
        if cmds.about(ntOS = True):
            self.setWindowFlags(self.windowFlags())
        elif cmds.about(macOS  = True):
            self.setWindowFlags(QtCore.Qt.Tool)
        self.light_items = []
        self.resize(700,560)

        self.create_widgets()
        self.create_layout()
        self.create_connections()

    # ---------------------------创建控件-----------------#
    def create_widgets(self):
        self.refreshButton = QtWidgets.QPushButton("Refresh")

    # ---------------------------设置布局-----------------#
    def create_layout(self):
        header_layout = QtWidgets.QHBoxLayout()
        header_layout.addSpacing(20)
        header_layout.addWidget(QtWidgets.QLabel("Light"))
        header_layout.addSpacing(100)
        header_layout.addWidget(QtWidgets.QLabel("Intensity"))
        header_layout.addSpacing(100)
        header_layout.addWidget(QtWidgets.QLabel("Color"))
        header_layout.addSpacing(100)
        header_layout.addWidget(QtWidgets.QLabel("Emit Diffuse"))
        header_layout.addSpacing(100)
        header_layout.addWidget(QtWidgets.QLabel("Emit Spec"))
        header_layout.addStretch()

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.refreshButton)

        light_list_wdg = QtWidgets.QWidget()

        self.light_layout = QtWidgets.QVBoxLayout(light_list_wdg)
        self.light_layout.setContentsMargins(2, 2, 2, 2)
        self.light_layout.setSpacing(3)
        self.light_layout.setAlignment(QtCore.Qt.AlignTop)

        light_list_scroll_area  = QtWidgets.QScrollArea()
        light_list_scroll_area.setWidgetResizable(True)
        light_list_scroll_area.setWidget(light_list_wdg)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(2,2,2,2)
        main_layout.addLayout(header_layout)
        main_layout.addWidget(light_list_scroll_area)
        # main_layout.addStretch()
        main_layout.addLayout(button_layout)

    # ---------------------------链接槽函数-----------------#
    def create_connections(self):
        self.refreshButton.clicked.connect(self.refresh_lights)

    # ---------------------------返回场景灯光数组-----------------#
    def get_lights_in_scene(self):
        return cmds.ls(type = "light")

    #----------------------------刷新数据---------------------#
    def refresh_lights(self):
        self.clear_lights()
        print("TODO: re")
        scene_lights = self.get_lights_in_scene()
        for light in scene_lights:
            light_item = LightItem(light)
            self.light_layout.addWidget(light_item)
            self.light_items.append(light_item)

    # ----------------------------清除灯光数据---------------------#
    def clear_lights(self):
        self.light_items = []
        print("TODO: cl")
        #如果layout中控件 大于0就删除 直到等于0
        while self.light_layout.count()>0:
            light_item = self.light_layout.takeAt(0)
            if light_item.widget():
                light_item.widget().deleteLater()


    def showEvent(self, event):
        self.refresh_lights()
    def closeEvent(self, event):
        self.clear_lights()

if __name__ == "__main__":
    try:
        Light_Dialog.close()
        Light_Dialog.deleteLater()
    except:
        pass
    Light_Dialog = LightPanel()
    Light_Dialog.show()
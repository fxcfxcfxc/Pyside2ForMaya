from PySide2 import QtCore
from PySide2 import QtWidgets
from shiboken2 import wrapInstance

import maya.OpenMayaUI as omui

#------------------------------------得到maya窗口-------------------#
def maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)


class TestDialog(QtWidgets.QDialog):

    RESOLUTION_ITEMS = [
                        ["1920x1080(1080P)", 1920.0, 1080.0],
                        ["1280x720(720P)", 1280.0, 720.0],
                        ["960x540(540p)", 960.0, 540.0],
                        ["640x480", 640.0, 480.0],
                        ["960x540", 320.0, 240.0]
                       ]


    def __init__(self, parent=maya_main_window()):
        super(TestDialog, self).__init__(parent)

        self.setWindowTitle("Test Dialog")
        self.setMinimumWidth(200)
        self.create_widgets()
        self.create_layouts()
        self.create_connections()
    # --------------------------------创建组件----------------------#
    def create_widgets(self):

        self.resoution_list_wdg = QtWidgets.QListWidget()
        # 添加元素
        # self.resoution_list_wdg.addItems(["1920x1080(1080P)","1280x720(720P)","960x540(540p)"])

        # 遍历list每一个元素
        for resolution_item in self.RESOLUTION_ITEMS:
            # 创建list对象
            list_wdg_item = QtWidgets.QListWidgetItem(resolution_item[0])
            # 设置list属性
            list_wdg_item.setData(QtCore.Qt.UserRole, [resolution_item[1], resolution_item[2]])

            self.resoution_list_wdg.addItem(list_wdg_item)

        self.button_01 = QtWidgets.QPushButton("Button2")

    # ----------------------------------设置布局---------------------------#
    def create_layouts(self):


        # 设置按钮的布局
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.button_01)


        # 总布局 添加其他布局
        main_layout = QtWidgets.QVBoxLayout(self)

        # 设置布局边界
        main_layout.setContentsMargins(2,2,2,2)
        main_layout.setSpacing(2)
        main_layout.addWidget(self.resoution_list_wdg)
        main_layout.addStretch()
        main_layout.addLayout(button_layout)

    # ----------------------------------设置信号与槽---------------------------#
    def create_connections(self):
        self.resoution_list_wdg.itemClicked.connect(self.set_output_resolution)

    #-------------------传入的item 代表触发信号时选择的元素对象---------------#
    def set_output_resolution(self,item):
        resloution = item.data(QtCore.Qt.UserRole)
        print(resloution[0])
        print(resloution[1])
        print( "resloution: {0}",format( resloution ) )




if __name__ == "__main__":
    try:
        d.close()
        d.deleteLater()

    except:
        pass

    d = TestDialog()
    d.show()
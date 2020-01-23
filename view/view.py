# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'view/view.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.video = QtWidgets.QFrame(self.centralwidget)
        self.video.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.video.setFrameShadow(QtWidgets.QFrame.Raised)
        self.video.setObjectName("video")
        self.gridLayout.addWidget(self.video, 0, 0, 1, 1)
        self.name_list = QtWidgets.QFrame(self.centralwidget)
        self.name_list.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.name_list.setFrameShadow(QtWidgets.QFrame.Raised)
        self.name_list.setObjectName("name_list")
        self.gridLayout.addWidget(self.name_list, 0, 1, 2, 1)
        self.button = QtWidgets.QFrame(self.centralwidget)
        self.button.setMaximumSize(QtCore.QSize(16777215, 200))
        self.button.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.button.setFrameShadow(QtWidgets.QFrame.Raised)
        self.button.setObjectName("button")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.button)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.clear_information_button = QtWidgets.QPushButton(self.button)
        self.clear_information_button.setMinimumSize(QtCore.QSize(0, 85))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.clear_information_button.setFont(font)
        self.clear_information_button.setObjectName("clear_information_button")
        self.gridLayout_2.addWidget(self.clear_information_button, 1, 1, 1, 1)
        self.import_information_button = QtWidgets.QPushButton(self.button)
        self.import_information_button.setMinimumSize(QtCore.QSize(0, 85))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.import_information_button.setFont(font)
        self.import_information_button.setObjectName("import_information_button")
        self.gridLayout_2.addWidget(self.import_information_button, 1, 2, 1, 1)
        self.check_in_button = QtWidgets.QPushButton(self.button)
        self.check_in_button.setMinimumSize(QtCore.QSize(0, 85))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.check_in_button.setFont(font)
        self.check_in_button.setObjectName("check_in_button")
        self.gridLayout_2.addWidget(self.check_in_button, 0, 1, 1, 2)
        self.export_information_button = QtWidgets.QPushButton(self.button)
        self.export_information_button.setMinimumSize(QtCore.QSize(0, 85))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.export_information_button.setFont(font)
        self.export_information_button.setObjectName("export_information_button")
        self.gridLayout_2.addWidget(self.export_information_button, 1, 3, 1, 1)
        self.choose_class_button = QtWidgets.QPushButton(self.button)
        self.choose_class_button.setMinimumSize(QtCore.QSize(0, 85))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.choose_class_button.setFont(font)
        self.choose_class_button.setObjectName("choose_class_button")
        self.gridLayout_2.addWidget(self.choose_class_button, 0, 3, 1, 1)
        self.gridLayout.addWidget(self.button, 1, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "去上课"))
        self.clear_information_button.setText(_translate("MainWindow", "清除数据"))
        self.import_information_button.setText(_translate("MainWindow", "导入信息"))
        self.check_in_button.setText(_translate("MainWindow", "签到"))
        self.export_information_button.setText(_translate("MainWindow", "导出数据"))
        self.choose_class_button.setText(_translate("MainWindow", "选择班级"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

import os
import sqlite3

from view.view import Ui_MainWindow
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox
import sys
import cv2

class ui_main(QMainWindow, Ui_MainWindow):
    # def __init__(self, parent=None):
    #     super(ui_main, self).__init__(parent)
    #     # self.setupUi(self)

    def setupUi(self, MainWindow):
        self.timer_camera = QtCore.QTimer() #定义定时器，用于控制显示视频的帧率
        self.cap = cv2.VideoCapture()       #视频流
        self.CAM_NUM = 0                    #为0时表示视频流来自笔记本内置摄像头

        Ui_MainWindow.setupUi(self, MainWindow)
        super().setupUi(MainWindow)
        self.import_information_button.clicked.connect(self.choose_dir)
        self.clear_information_button.clicked.connect(self.delete_data)
        self.comboBox.addItem('')
        if os.path.exists('data.db'):
            self.add_comboBox()

        self.timer_camera.timeout.connect(self.show_camera) #若定时器结束，则调用show_camera()
        flag = self.cap.open(self.CAM_NUM)
        self.timer_camera.start(10)  #定时器开始计时30ms，结果是每过30ms从摄像头中取一帧显示

    def show_camera(self):
        flag,self.image = self.cap.read()  #从视频流中读取
 
        show = cv2.resize(self.image,(960,720))     #把读到的帧的大小重新设置为 640x480
        show = cv2.cvtColor(show,cv2.COLOR_BGR2RGB) #视频色彩转换回RGB，这样才是现实的颜色
        showImage = QtGui.QImage(show.data,show.shape[1],show.shape[0],QtGui.QImage.Format_RGB888) #把读取到的视频数据变成QImage形式
        self.video_label.setPixmap(QtGui.QPixmap.fromImage(showImage))  #往显示视频的Label里 显示QImage

    def add_comboBox(self):
        class_data = self.get_class()
        self.comboBox.addItems(class_data)
        self.comboBox.currentTextChanged.connect(self.choose_class)

    def get_class(self):
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        cursor = c.execute("SELECT DISTINCT class FROM information")
        class_data = []
        for row in cursor:
            class_data.append(row[0])
        conn.close()
        return class_data

    def choose_class(self):
        choosed_class = self.comboBox.currentText()
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        cursor = c.execute("SELECT id,name FROM information WHERE class=?",(choosed_class,))
        for row in cursor:
            student = row[1]+row[0]
            self.checkBox = QtWidgets.QCheckBox(self.name_list)
            self.checkBox.setObjectName("checkBox")
            self.checkBox.setText(student)
            self.verticalLayout.addWidget(self.checkBox)
            self.checkBox = QtWidgets.QCheckBox(self.name_list)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)

    def choose_dir(self):
        directory = QFileDialog.getExistingDirectory(self, "选取文件夹", "./")
        if directory != '':
            data = []
            files_name = os.listdir(directory)
            for file_name in files_name:
                file_name_split = file_name.split(',')
                file_name_split.append('')
                data.append(file_name_split)
            conn = sqlite3.connect('data.db')
            c = conn.cursor()
            c.execute('''CREATE TABLE information
                    (
                        id text,
                        name text,
                        class text,
                        check_in text
                    );''')
            c.executemany("INSERT INTO information VALUES (?,?,?,?)", data)
            conn.commit()
            conn.close()
            self.add_comboBox()

    def delete_data(self):
        reply = QMessageBox.question(self, '确认', '确定要清除数据吗?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            os.system('rm data.db')

def view_show():
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = ui_main()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    view_show()

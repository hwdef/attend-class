import os
import sqlite3

from view.view import Ui_MainWindow
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox
import sys
import cv2
import face_recognition
import numpy as np
from time import strftime,gmtime

class ui_main(QMainWindow, Ui_MainWindow):

    def setupUi(self, MainWindow):
        self.timer_camera = QtCore.QTimer() #定义定时器，用于控制显示视频的帧率
        self.cap = cv2.VideoCapture()       #视频流
        self.CAM_NUM = 0                    #为0时表示视频流来自笔记本内置摄像头
        self.face_locations = []
        self.face_encodings = []
        self.face_names = []
        self.process_this_frame = True
        self.directory = 'images'
        self.known_face_names = []
        self.known_face_encodings = []
        id = []
        data = self.choose_dir()
        for i in data:
            self.known_face_names.append(i[0])
            filename = i[0] + ',' + i[1] + ',' + i[2] + '.jpg'
            exec('face_{} = face_recognition.face_encodings(face_recognition.load_image_file("images/{}"))[0]'.format(i[0],filename))
            exec('self.known_face_encodings.append(face_{})'.format(i[0]))
        
        Ui_MainWindow.setupUi(self, MainWindow)
        super().setupUi(MainWindow)
        self.import_information_button.clicked.connect(self.save_information)
        self.clear_information_button.clicked.connect(self.delete_data)
        self.check_in_button.clicked.connect(self.check_in)
        self.export_information_button.clicked.connect(self.export_information)
        self.comboBox.addItem('')
        if os.path.exists('data.db'):
            self.add_comboBox()

    def show_camera(self):
        flag,self.image = self.cap.read()  #从视频流中读取
        show = cv2.resize(self.image,(960,720))     #把读到的帧的大小重新设置为 960*720
        show = cv2.cvtColor(show,cv2.COLOR_BGR2RGB) #视频色彩转换回RGB，这样才是现实的颜色
        showImage = QtGui.QImage(show.data,show.shape[1],show.shape[0],QtGui.QImage.Format_RGB888) #把读取到的视频数据变成QImage形式
        self.video_label.setPixmap(QtGui.QPixmap.fromImage(showImage))  #往显示视频的Label里 显示QImage
        self.face()
        
    def face(self):
        frame = self.image
        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Only process every other frame of video to save time
        if self.process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            self.face_locations = face_recognition.face_locations(rgb_small_frame)
            self.face_encodings = face_recognition.face_encodings(rgb_small_frame, self.face_locations)

            for face_encoding in self.face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
                id = "Unknown"
                face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    id = self.known_face_names[best_match_index]
                    if id != 'Unknown':
                        for i in range(self.count):
                            cb = getattr(self,"checkBox%d"%i)
                            if id in cb.text():
                                cb.setChecked(True)

        self.process_this_frame = not self.process_this_frame

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
        self.count = 0
        choosed_class = self.comboBox.currentText()
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        cursor = c.execute("SELECT id,name FROM information WHERE class=?",(choosed_class,))
        for row in cursor:
            student = row[1]+' '+row[0]
            exec('self.checkBox{} = QtWidgets.QCheckBox(self.name_list)'.format(self.count))
            font = QtGui.QFont()
            font.setPointSize(20)
            exec('self.checkBox{}.setFont(font)'.format(self.count))
            exec('self.checkBox{}.setText(student)'.format(self.count))
            exec('self.verticalLayout.addWidget(self.checkBox{})'.format(self.count))
            self.count = self.count + 1
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        self.timer_camera.timeout.connect(self.show_camera) #若定时器结束，则调用show_camera()
        self.cap.open(self.CAM_NUM)
        self.timer_camera.start(30)  #定时器开始计时30ms，结果是每过30ms从摄像头中取一帧显示

    def choose_dir(self):
        data = []
        files_name = os.listdir(self.directory)
        for file_name in files_name:
            file_name_split = file_name.split(',')
            file_name_split.append('')
            file_name_split[-2]=file_name_split[-2][:-4] #去掉.jpg后缀
            data.append(file_name_split)
        return data

    def save_information(self):
        data = self.choose_dir()
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
        QMessageBox.information(self,"","导入成功",QMessageBox.Yes,QMessageBox.Yes)


    def delete_data(self):
        reply = QMessageBox.question(self, '确认', '确定要清除数据吗?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            os.remove('data.db')

    def check_in(self):
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        for i in range(self.count):
            cb = getattr(self,"checkBox%d"%i)
            if cb.isChecked():
                id = cb.text().split(' ')[1]
                cursor = c.execute('SELECT check_in FROM information WHERE id = ?',(id,))
                for y in cursor:
                    now_time = y[0] + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ','
                    c.execute('UPDATE information SET check_in = ? WHERE id = ?',(now_time,id))
                conn.commit()
        conn.close()
        QMessageBox.information(self,"","签到成功",QMessageBox.Yes,QMessageBox.Yes)

    def export_information(self):
        res = ''
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        cursor = c.execute("SELECT * FROM information")
        for row in cursor:
            res = res + row[0] +','+ row[1] +','+ row[2] +','+ row[3] + '\n'
        conn.close()
        file_path =  QFileDialog.getSaveFileName(self,'save file',"考勤信息.csv" ,"csv files (*.csv);;all files(*.*)") 
        file = open(file_path[0],'w')
        file.write(res)
        file.close()
        
def view_show():
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = ui_main()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    view_show()

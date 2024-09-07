import sys
import os
import traceback
import logging
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QFileDialog, QVBoxLayout, QLabel,
                             QStackedWidget, QHBoxLayout, QRadioButton, QButtonGroup)
from PyQt5.QtCore import QSettings
from moviepy.editor import VideoFileClip

# 设置日志
log_path = os.path.expanduser('~/audio_extractor_app.log')
logging.basicConfig(filename=log_path, level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

logging.info("Starting application...")
logging.info(f"Python version: {sys.version}")
logging.info(f"Executable: {sys.executable}")
logging.info(f"Current working directory: {os.getcwd()}")
logging.info(f"sys.path: {sys.path}")

# 尝试导入所需的模块
try:
    from PyQt5.QtWidgets import QApplication
    print("Successfully imported PyQt5")
except ImportError as e:
    print("Failed to import PyQt5:", str(e))

try:
    from moviepy.editor import VideoFileClip
    print("Successfully imported moviepy")
except ImportError as e:
    print("Failed to import moviepy:", str(e))

try:
    # 设置 ffmpeg 路径
    if getattr(sys, 'frozen', False):
        # 如果是打包后的应用
        ffmpeg_path = os.path.join(os.path.dirname(sys.executable), 'ffmpeg')
        if not os.path.exists(ffmpeg_path):
            # 如果 ffmpeg 不在预期位置，尝试在资源目录中查找
            ffmpeg_path = os.path.join(os.path.dirname(os.path.dirname(sys.executable)), 'Resources', 'ffmpeg')
    else:
        # 如果是开发环境
        ffmpeg_path = os.popen('which ffmpeg').read().strip()

    # 设置 ffmpeg 环境变量
    os.environ['IMAGEIO_FFMPEG_EXE'] = ffmpeg_path
    logging.info(f"FFMPEG path: {ffmpeg_path}")
    logging.info(f"FFMPEG path exists: {os.path.exists(ffmpeg_path)}")
    logging.info(f"FFMPEG path is executable: {os.access(ffmpeg_path, os.X_OK)}")

except Exception as e:
    logging.error(f"Error during ffmpeg setup: {str(e)}")
    logging.error(traceback.format_exc())
    sys.exit(1)

class AudioExtractor(QWidget):
    def __init__(self):
        super().__init__()
        self.settings = QSettings('YourCompany', 'AudioExtractor')
        self.initUI()

    def initUI(self):
        # 创建堆叠小部件来管理两层结构
        self.stacked_widget = QStackedWidget()
        
        # 创建第一层和第二层
        self.create_first_layer()
        self.create_second_layer()
        
        # 将两层添加到堆叠小部件中
        self.stacked_widget.addWidget(self.first_layer)
        self.stacked_widget.addWidget(self.second_layer)
        
        # 设置主布局
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.stacked_widget)
        self.setLayout(main_layout)
        
        # 设置窗口
        self.setGeometry(300, 300, 400, 300)
        self.setWindowTitle('音频提取器')
        self.show()
        
        # 加载保存的设置
        self.load_settings()

    def create_first_layer(self):
        self.first_layer = QWidget()
        layout = QVBoxLayout()
        
        # 创建单选按钮组
        self.radio_group = QButtonGroup()
        self.radio_file = QRadioButton('选择指定视频文件')
        self.radio_folder = QRadioButton('选择指定文件夹')
        self.radio_group.addButton(self.radio_file)
        self.radio_group.addButton(self.radio_folder)
        
        layout.addWidget(self.radio_file)
        layout.addWidget(self.radio_folder)
        
        # 创建选择按钮
        self.btn_select = QPushButton('选择')
        self.btn_select.clicked.connect(self.select_input)
        layout.addWidget(self.btn_select)
        
        # 创建选择输出路径按钮
        self.btn_output = QPushButton('选择输出路径')
        self.btn_output.clicked.connect(self.select_output)
        layout.addWidget(self.btn_output)
        
        # 创建下一步按钮
        self.btn_next = QPushButton('下一步')
        self.btn_next.clicked.connect(self.go_to_second_layer)
        layout.addWidget(self.btn_next)
        
        # 创建标签显示选择的路径
        self.label_path = QLabel('未选择路径')
        self.label_output = QLabel('未选择输出路径')
        layout.addWidget(self.label_path)
        layout.addWidget(self.label_output)
        
        self.first_layer.setLayout(layout)

    def create_second_layer(self):
        self.second_layer = QWidget()
        layout = QVBoxLayout()
        
        self.btn_extract = QPushButton('提取音频')
        self.btn_extract.clicked.connect(self.extract_audio)
        layout.addWidget(self.btn_extract)
        
        self.label_status = QLabel('准备提取')
        layout.addWidget(self.label_status)
        
        self.btn_back = QPushButton('返回')
        self.btn_back.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        layout.addWidget(self.btn_back)
        
        self.second_layer.setLayout(layout)

    def select_input(self):
        if self.radio_file.isChecked():
            path, _ = QFileDialog.getOpenFileName(self, '选择视频文件', '', 'Video Files (*.mp4 *.avi *.mov)')
            if path:
                self.input_path = path
                self.label_path.setText(f'选择的文件: {path}')
        elif self.radio_folder.isChecked():
            path = QFileDialog.getExistingDirectory(self, '选择文件夹')
            if path:
                self.input_path = path
                self.label_path.setText(f'选择的文件夹: {path}')
        self.save_settings()

    def select_output(self):
        path = QFileDialog.getExistingDirectory(self, '选择输出目录')
        if path:
            self.output_path = path
            self.label_output.setText(f'输出目录: {path}')
        self.save_settings()

    def go_to_second_layer(self):
        if hasattr(self, 'input_path') and hasattr(self, 'output_path'):
            self.stacked_widget.setCurrentIndex(1)
        else:
            self.label_status.setText('请先选择输入和输出路径')

    def extract_audio(self):
        try:
            if os.path.isfile(self.input_path):
                self.extract_single_file(self.input_path)
            elif os.path.isdir(self.input_path):
                self.extract_from_folder(self.input_path)
            self.label_status.setText('提取完成')
        except Exception as e:
            self.label_status.setText(f'提取失败: {str(e)}')
            logging.error(f"Error in extracting audio: {str(e)}")
            logging.error(traceback.format_exc())

    def extract_single_file(self, video_path):
        video = VideoFileClip(video_path)
        audio = video.audio
        output_filename = os.path.splitext(os.path.basename(video_path))[0] + '.mp3'
        output_path = os.path.join(self.output_path, output_filename)
        audio.write_audiofile(output_path)
        video.close()
        audio.close()

    def extract_from_folder(self, folder_path):
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.endswith(('.mp4', '.avi', '.mov')):
                    video_path = os.path.join(root, file)
                    self.extract_single_file(video_path)

    def save_settings(self):
        if hasattr(self, 'input_path'):
            self.settings.setValue('input_path', self.input_path)
        if hasattr(self, 'output_path'):
            self.settings.setValue('output_path', self.output_path)
        self.settings.setValue('is_file', self.radio_file.isChecked())

    def load_settings(self):
        input_path = self.settings.value('input_path')
        output_path = self.settings.value('output_path')
        is_file = self.settings.value('is_file', type=bool)
        
        if input_path:
            self.input_path = input_path
            if is_file:
                self.radio_file.setChecked(True)
                self.label_path.setText(f'选择的文件: {input_path}')
            else:
                self.radio_folder.setChecked(True)
                self.label_path.setText(f'选择的文件夹: {input_path}')
        
        if output_path:
            self.output_path = output_path
            self.label_output.setText(f'输出目录: {output_path}')

if __name__ == '__main__':
    try:
        logging.info("Entering main")
        app = QApplication(sys.argv)
        logging.info("QApplication created")
        ex = AudioExtractor()
        logging.info("AudioExtractor instance created")
        result = app.exec_()
        logging.info(f"Application exited with code {result}")
        sys.exit(result)
    except Exception as e:
        logging.error(f"Error in main: {str(e)}")
        logging.error(traceback.format_exc())
        sys.exit(1)
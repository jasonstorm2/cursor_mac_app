import sys
import os
import traceback
import logging

# 设置日志
logging.basicConfig(filename=os.path.expanduser('~/audio_extractor_app.log'), level=logging.DEBUG)

try:
    # 添加调试信息
    logging.info(f"Python version: {sys.version}")
    logging.info(f"Executable: {sys.executable}")
    logging.info(f"Current working directory: {os.getcwd()}")
    logging.info(f"sys.path: {sys.path}")

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

    os.environ['IMAGEIO_FFMPEG_EXE'] = ffmpeg_path
    logging.info(f"FFMPEG path: {ffmpeg_path}")
    logging.info(f"FFMPEG path exists: {os.path.exists(ffmpeg_path)}")
    logging.info(f"FFMPEG path is executable: {os.access(ffmpeg_path, os.X_OK)}")

    from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog, QVBoxLayout, QLabel
    from moviepy.editor import VideoFileClip
except Exception as e:
    logging.error(f"Error during import: {str(e)}")
    logging.error(traceback.format_exc())
    sys.exit(1)

# 原有的导入语句
import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog, QVBoxLayout, QLabel
from moviepy.editor import VideoFileClip

class AudioExtractor(QWidget):
    def __init__(self):
        super().__init__()
        try:
            self.initUI()
        except Exception as e:
            logging.error(f"Error in initializing UI: {str(e)}")
            logging.error(traceback.format_exc())

    def initUI(self):
        layout = QVBoxLayout()

        self.label = QLabel('选择视频文件和输出目录')
        layout.addWidget(self.label)

        btn_select_video = QPushButton('选择视频文件', self)
        btn_select_video.clicked.connect(self.select_video)
        layout.addWidget(btn_select_video)

        btn_select_output = QPushButton('选择输出目录', self)
        btn_select_output.clicked.connect(self.select_output)
        layout.addWidget(btn_select_output)

        btn_extract = QPushButton('提取音频', self)
        btn_extract.clicked.connect(self.extract_audio)
        layout.addWidget(btn_extract)

        self.setLayout(layout)
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('音频提取器')
        self.show()

        self.video_path = ''
        self.output_dir = ''

    def select_video(self):
        self.video_path, _ = QFileDialog.getOpenFileName(self, '选择视频文件', '', 'Video Files (*.mp4 *.avi *.mov)')
        self.update_label()

    def select_output(self):
        self.output_dir = QFileDialog.getExistingDirectory(self, '选择输出目录')
        self.update_label()

    def update_label(self):
        self.label.setText(f'视频: {self.video_path}\n输出: {self.output_dir}')

    def extract_audio(self):
        if not self.video_path or not self.output_dir:
            self.label.setText('请先选择视频文件和输出目录')
            return

        try:
            video = VideoFileClip(self.video_path)
            audio = video.audio
            
            output_filename = os.path.splitext(os.path.basename(self.video_path))[0] + '.mp3'
            output_path = os.path.join(self.output_dir, output_filename)
            
            audio.write_audiofile(output_path)
            video.close()
            audio.close()

            self.label.setText(f'音频已提取到: {output_path}')
        except Exception as e:
            error_msg = f"Error in extracting audio: {str(e)}"
            logging.error(error_msg)
            logging.error(traceback.format_exc())
            self.label.setText(error_msg)

if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        ex = AudioExtractor()
        sys.exit(app.exec_())
    except Exception as e:
        logging.error(f"Error in main: {str(e)}")
        logging.error(traceback.format_exc())
        sys.exit(1)
import os
import shutil
import sys
from setuptools import setup

# 获取 ffmpeg 的路径
ffmpeg_path = os.popen('which ffmpeg').read().strip()

# 确保 ffmpeg 存在
if not os.path.exists(ffmpeg_path):
    raise FileNotFoundError(f"ffmpeg not found at {ffmpeg_path}")

APP = ['audio_extractor.py']
DATA_FILES = [('', [ffmpeg_path])]

OPTIONS = {
    'argv_emulation': False,
    'packages': ['PyQt5', 'moviepy', 'numpy', 'decorator', 'imageio', 'tqdm', 'proglog', 'chardet', 'requests'],
    'includes': ['sip', 'PyQt5.QtCore', 'PyQt5.QtGui', 'PyQt5.QtWidgets'],
    'excludes': ['tkinter'],
    'plist': {
        'CFBundleName': 'Audio Extractor',
        'CFBundleDisplayName': 'Audio Extractor',
        'CFBundleGetInfoString': "Extract audio from video files",
        'CFBundleIdentifier': "com.yourcompany.AudioExtractor",
        'CFBundleVersion': "0.1.0",
        'CFBundleShortVersionString': "0.1.0",
        'NSHumanReadableCopyright': u"Copyright © 2023, Your Company, All Rights Reserved"
    }
}

def post_process(target_dir):
    # 复制 ffmpeg 到应用程序包中
    dest = os.path.join(target_dir, 'Contents', 'MacOS', 'ffmpeg')
    shutil.copy2(ffmpeg_path, dest)
    print(f"Copied ffmpeg to {dest}")
    # 确保 ffmpeg 有执行权限
    os.chmod(dest, 0o755)
    print(f"Set execute permissions for {dest}")

setup(
    app=APP,
    name='Audio Extractor',
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
    install_requires=['PyQt5', 'moviepy', 'numpy', 'decorator', 'imageio', 'tqdm', 'proglog', 'chardet', 'requests'],
)

# 在 setup 完成后执行后处理
if 'py2app' in sys.argv:
    post_process('dist/Audio Extractor.app')
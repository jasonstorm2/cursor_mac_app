# Audio Extractor

   这是一个简单的 Mac 应用程序，用于从视频文件中提取音频。

   ## 前置要求

   - macOS 操作系统
   - Python 3.9 或更高版本
   - Homebrew（用于安装 ffmpeg）

   ## 安装步骤

   1. 确保你的系统安装了 Python 3.9 或更高版本。
   2. 克隆此仓库：
      ```
      git clone https://github.com/jasonstorm2/audio-extractor.git
      cd audio-extractor
      ```
   3. 创建并激活虚拟环境：
      ```
      python3 -m venv myenv
      source myenv/bin/activate
          ```
   4. 安装依赖：
      ```
      pip install -r requirements.txt
      ```
   5. 安装 ffmpeg（如果尚未安装）：
      ```
      brew install ffmpeg
      ```

   ## 构建应用

   运行以下命令构建应用：
   ```
   python setup.py py2app
   
构建完成后，你可以在 `dist` 目录中找到 `Audio Extractor.app`。

   ## 运行应用

   双击 `dist/Audio Extractor.app` 运行应用。

   ## 使用方法

   1. 点击 "选择视频文件" 选择要提取音频的视频文件。
   2. 点击 "选择输出目录" 选择音频文件的保存位置。
   3. 点击 "提取音频" 开始提取过程。
   4. 提取完成后，应用会显示输出文件的路径。

## 注意事项

   - 确保你的系统中安装了 ffmpeg。
   - 如果遇到权限问题，可能需要在系统偏好设置中允许运行来自未知开发者的应用。

## 贡献

欢迎提交 Pull Requests 来改进这个项目。

## 许可证

[MIT License](LICENSE)

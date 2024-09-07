#!/bin/bash
APP_PATH="/Users/jasonli/cursor_mac_app/dist/Audio Extractor.app/Contents/MacOS/Audio Extractor"
LOG_PATH="$HOME/audio_extractor_run.log"

echo "Starting application at $(date)" > "$LOG_PATH"
echo "App path: $APP_PATH" >> "$LOG_PATH"
echo "Python version:" >> "$LOG_PATH"
/usr/bin/python3 --version >> "$LOG_PATH" 2>&1

"$APP_PATH" >> "$LOG_PATH" 2>&1

echo "Application exited with code $?" >> "$LOG_PATH"

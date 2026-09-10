import re

with open('.github/workflows/flutter-build.yml', 'r') as f:
    text = f.read()

old_apt = """          sudo apt-get install -y build-essential libx11-dev libxdo-dev libwayland-dev libxkbcommon-dev libdrm-dev libgbm-dev libpam0g-dev libxtst-dev libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev clang cmake ninja-build pkg-config libgtk-3-dev liblzma-dev nasm libva-dev"""
new_apt = """          sudo apt-get install -y build-essential libx11-dev libxdo-dev libwayland-dev libxkbcommon-dev libdrm-dev libgbm-dev libpam0g-dev libxtst-dev libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev clang cmake ninja-build pkg-config libgtk-3-dev liblzma-dev nasm libva-dev libasound2-dev libpulse-dev libayatana-appindicator3-dev libegl1-mesa-dev"""

text = text.replace(old_apt, new_apt)

with open('.github/workflows/flutter-build.yml', 'w') as f:
    f.write(text)

print("Fixed apt-get even more!")


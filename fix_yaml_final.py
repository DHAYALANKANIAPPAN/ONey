with open('.github/workflows/flutter-build.yml', 'r') as f:
    text = f.read()

# I will just write a python script that replaces the 'run' line with a proper multiline block.
import re

old_text = r"""      - name: Install dependencies
        run: 'sudo apt-get install ca-certificates -y

          sudo apt-get update -y

          sudo apt-get install -y clang cmake gcc git g++ libclang-dev libgtk-3-dev
          llvm-dev nasm ninja-build pkg-config wget libxdo-dev libx11-dev libxext-dev
          libxfixes-dev libxi-dev libxrandr-dev libxtst-dev libxcb1-dev libx11-xcb-dev
          libxcb-damage0-dev libxcb-xfixes0-dev libxcb-shape0-dev libxcb-render-util0-dev
          libxcb-render0-dev libxcb-randr0-dev libxcb-composite0-dev libxcb-image0-dev
          libxcb-present-dev libxcb-xinerama0-dev libxcb-glx0-dev libpixman-1-dev
          libdbus-1-dev libgbm-dev libusb-1.0-0-dev libwayland-dev libxkbcommon-dev
          libdrm-dev libpam0g-dev libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev
          libappindicator3-dev

          '"""

new_text = """      - name: Install dependencies
        run: |
          sudo apt-get install ca-certificates -y
          sudo apt-get update -y
          sudo apt-get install -y clang cmake gcc git g++ libclang-dev libgtk-3-dev llvm-dev nasm ninja-build pkg-config wget libxdo-dev libx11-dev libxext-dev libxfixes-dev libxi-dev libxrandr-dev libxtst-dev libxcb1-dev libx11-xcb-dev libxcb-damage0-dev libxcb-xfixes0-dev libxcb-shape0-dev libxcb-render-util0-dev libxcb-render0-dev libxcb-randr0-dev libxcb-composite0-dev libxcb-image0-dev libxcb-present-dev libxcb-xinerama0-dev libxcb-glx0-dev libpixman-1-dev libdbus-1-dev libgbm-dev libusb-1.0-0-dev libwayland-dev libxkbcommon-dev libdrm-dev libpam0g-dev libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev libappindicator3-dev"""

text = text.replace(old_text, new_text)

# Also fix the build step which also has the same problem!
old_build = r"""      - name: Build
        run: 'python3 ./build.py --flutter

          '"""
new_build = """      - name: Build
        run: python3 ./build.py --flutter"""

text = text.replace(old_build, new_build)

with open('.github/workflows/flutter-build.yml', 'w') as f:
    f.write(text)


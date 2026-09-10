with open('.github/workflows/flutter-build.yml', 'r') as f:
    text = f.read()

# Replace the entire apt-get install block
import re

new_text = re.sub(
    r'sudo apt-get install -y clang.*',
    r'sudo apt-get install -y g++-11 libx11-dev libxdo-dev libwayland-dev libxkbcommon-dev libdrm-dev libgbm-dev libpam0g-dev libxtst-dev libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev clang cmake ninja-build pkg-config libgtk-3-dev liblzma-dev libstdc++-12-dev',
    text
)

with open('.github/workflows/flutter-build.yml', 'w') as f:
    f.write(new_text)

print("Fixed apt-get dependencies to official list!")


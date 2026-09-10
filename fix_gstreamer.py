with open('.github/workflows/flutter-build.yml', 'r') as f:
    text = f.read()

# Replace the apt-get line to remove gstreamer
old_line = "libdrm-dev libpam0g-dev libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev libappindicator3-dev"
new_line = "libdrm-dev libpam0g-dev libappindicator3-dev"

if old_line in text:
    text = text.replace(old_line, new_line)
    with open('.github/workflows/flutter-build.yml', 'w') as f:
        f.write(text)
    print("Replaced!")
else:
    print("Not found!")

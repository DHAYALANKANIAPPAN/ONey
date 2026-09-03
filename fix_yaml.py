import urllib.request

# 1. Download the pristine, perfectly formatted file directly from RustDesk to fix the spaces
url = "https://raw.githubusercontent.com/rustdesk/rustdesk/master/.github/workflows/flutter-build.yml"
urllib.request.urlretrieve(url, ".github/workflows/flutter-build.yml")

# 2. Open it and apply ONLY the Windows compiler fix
with open(".github/workflows/flutter-build.yml", "r") as f:
    text = f.read()

# Change to the stable windows-2019 compiler to bypass the vcpkg C++ crash
text = text.replace("windows-2022", "windows-2019")

with open(".github/workflows/flutter-build.yml", "w") as f:
    f.write(text)

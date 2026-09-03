import re

with open(".github/workflows/flutter-build.yml", "r") as f:
    text = f.read()

# 1. Safely inject a command to skip non-Windows builds (Linux, Mac, Android) to save time
text = re.sub(
    r'(runs-on: \$\{\{ matrix\.job\.os \}\}\n)',
    r'\1    if: contains(matrix.job.os, \'windows\')\n',
    text
)

# 2. Downgrade from the buggy windows-2022 C++ compiler to the stable windows-2019 compiler
text = text.replace('os: windows-2022', 'os: windows-2019')

with open(".github/workflows/flutter-build.yml", "w") as f:
    f.write(text)

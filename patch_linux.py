with open('.github/workflows/flutter-build.yml', 'r') as f:
    text = f.read()

import re
old_bridge = """      - name: Download bridge artifact
        uses: actions/download-artifact@v3
        with:
          name: bridge-artifact-flutter-${{ env.FLUTTER_VERSION }}
          path: flutter/lib/generated_bridge.dart"""

new_bridge = """      - name: Restore bridge files
        uses: actions/download-artifact@3e5f45b2cfb9172054b4087a40e8e0b5a5461e7c
        with:
          name: bridge-artifact"""

text = text.replace(old_bridge, new_bridge)

with open('.github/workflows/flutter-build.yml', 'w') as f:
    f.write(text)

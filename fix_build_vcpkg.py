import re

with open('.github/workflows/flutter-build.yml', 'r') as f:
    text = f.read()

# Fix Setup VCPKG to write to GITHUB_ENV
old_setup = """      - name: Setup VCPKG
        run: |
          export VCPKG_ROOT=/opt/artifacts/vcpkg"""

new_setup = """      - name: Setup VCPKG
        run: |
          echo "VCPKG_ROOT=/opt/artifacts/vcpkg" >> $GITHUB_ENV
          export VCPKG_ROOT=/opt/artifacts/vcpkg"""

text = text.replace(old_setup, new_setup)

# Fix Build step to run cargo manually
old_build = """      - name: Build
        run: |
          export VCPKG_ROOT=/opt/artifacts/vcpkg
          python3 ./build.py --flutter"""

new_build = """      - name: Build
        run: |
          cargo build --locked --lib --features flutter,hwcodec --release
          python3 ./build.py --flutter --hwcodec --skip-cargo"""

text = text.replace(old_build, new_build)

with open('.github/workflows/flutter-build.yml', 'w') as f:
    f.write(text)

print("Fixed Build and GITHUB_ENV!")


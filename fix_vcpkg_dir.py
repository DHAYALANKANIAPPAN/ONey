import re

with open('.github/workflows/flutter-build.yml', 'r') as f:
    text = f.read()

old_vcpkg = """          ./bootstrap-vcpkg.sh -disableMetrics
          ./vcpkg install --triplet x64-linux --x-install-root="$VCPKG_ROOT/installed"
          popd
          popd"""

new_vcpkg = """          ./bootstrap-vcpkg.sh -disableMetrics
          popd
          popd
          $VCPKG_ROOT/vcpkg install --triplet x64-linux --x-install-root="$VCPKG_ROOT/installed\""""

if old_vcpkg in text:
    text = text.replace(old_vcpkg, new_vcpkg)
    with open('.github/workflows/flutter-build.yml', 'w') as f:
        f.write(text)
    print("Fixed VCPKG directory!")
else:
    print("String not found!")


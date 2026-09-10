import re

with open('.github/workflows/flutter-build.yml', 'r') as f:
    text = f.read()

vcpkg_step = """
      - name: Export GitHub Actions cache environment variables
        uses: actions/github-script@v6
        with:
          script: |
            core.exportVariable('ACTIONS_CACHE_URL', process.env.ACTIONS_CACHE_URL || '');
            core.exportVariable('ACTIONS_RUNTIME_TOKEN', process.env.ACTIONS_RUNTIME_TOKEN || '');

      - name: Setup VCPKG
        run: |
          export VCPKG_ROOT=/opt/artifacts/vcpkg
          sudo mkdir -p /opt/artifacts
          sudo chown -R $USER:$USER /opt/artifacts
          pushd /opt/artifacts
          git clone https://github.com/microsoft/vcpkg
          pushd vcpkg
          git reset --hard ${{ env.VCPKG_COMMIT_ID }}
          ./bootstrap-vcpkg.sh -disableMetrics
          ./vcpkg install --triplet x64-linux --x-install-root="$VCPKG_ROOT/installed"
          popd
          popd

      - name: Build
        run: |
          export VCPKG_ROOT=/opt/artifacts/vcpkg
          python3 ./build.py --flutter
"""

# Replace the old Build step
new_text = re.sub(r'      - name: Build\n        run: python3 ./build.py --flutter\n?', vcpkg_step, text)

with open('.github/workflows/flutter-build.yml', 'w') as f:
    f.write(new_text)

print("Added vcpkg setup step!")


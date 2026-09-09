import yaml

with open('.github/workflows/flutter-build.yml', 'r') as f:
    data = yaml.safe_load(f)

# Remove Windows jobs
if 'build-for-windows-flutter' in data['jobs']:
    del data['jobs']['build-for-windows-flutter']
if 'build-for-windows-sciter' in data['jobs']:
    del data['jobs']['build-for-windows-sciter']
if 'build-RustDeskTempTopMostWindow' in data['jobs']:
    del data['jobs']['build-RustDeskTempTopMostWindow']

# Add Linux job
data['jobs']['build-for-linux-flutter'] = {
    'runs-on': 'ubuntu-22.04',
    'needs': ['generate-bridge'],
    'steps': [
        {
            'name': 'Checkout',
            'uses': 'actions/checkout@v3',
        },
        {
            'name': 'Download bridge artifact',
            'uses': 'actions/download-artifact@v3',
            'with': {
                'name': 'bridge-artifact-flutter-${{ env.FLUTTER_VERSION }}',
                'path': 'flutter/lib/generated_bridge.dart'
            }
        },
        {
            'name': 'Install Dependencies',
            'run': 'sudo apt-get update\nsudo apt-get install -y g++-11 libx11-dev libxdo-dev libwayland-dev libxkbcommon-dev libdrm-dev libgbm-dev libpam0g-dev libxtst-dev libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev zip g++ gcc git curl wget nasm yasm libgtk-3-dev clang libxcb-randr0-dev libxfixes-dev libxcb-shape0-dev libxcb-xfixes0-dev libasound2-dev libpulse-dev cmake make libclang-dev ninja-build\n'
        },
        {
            'name': 'Install Rust',
            'uses': 'dtolnay/rust-toolchain@stable',
            'with': {
                'toolchain': '${{ env.RUST_VERSION }}',
                'targets': 'x86_64-unknown-linux-gnu'
            }
        },
        {
            'name': 'Install Flutter',
            'uses': 'subosito/flutter-action@v2',
            'with': {
                'channel': 'stable',
                'flutter-version': '${{ env.FLUTTER_VERSION }}'
            }
        },
        {
            'name': 'Build Linux deb',
            'run': 'python3 ./build.py --flutter\n'
        },
        {
            'name': 'Upload Artifact',
            'uses': 'actions/upload-artifact@v3',
            'with': {
                'name': 'rustdesk-linux-deb',
                'path': 'rustdesk-*.deb'
            }
        }
    ]
}

class Dumper(yaml.Dumper):
    def increase_indent(self, flow=False, indentless=False):
        return super(Dumper, self).increase_indent(flow, False)

with open('.github/workflows/flutter-build.yml', 'w') as f:
    yaml.dump(data, f, Dumper=Dumper, default_flow_style=False, sort_keys=False)

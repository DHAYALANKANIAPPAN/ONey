import yaml

with open('.github/workflows/flutter-build.yml', 'r') as f:
    data = yaml.safe_load(f)

# Delete windows jobs
jobs_to_delete = [
    'build-RustDeskTempTopMostWindow',
    'build-for-windows-flutter',
    'build-for-windows-sciter'
]

for job in jobs_to_delete:
    if job in data.get('jobs', {}):
        del data['jobs'][job]

# Add linux job
data['jobs']['build-for-linux-flutter'] = {
    'runs-on': 'ubuntu-22.04',
    'needs': ['generate-bridge'],
    'steps': [
        {
            'name': 'Checkout',
            'uses': 'actions/checkout@v3'
        },
        {
            'name': 'Restore bridge files',
            'uses': 'actions/download-artifact@3e5f45b2cfb9172054b4087a40e8e0b5a5461e7c',
            'with': {
                'name': 'bridge-artifact'
            }
        },
        {
            'name': 'Install dependencies',
            'run': 'sudo apt update\nsudo apt install -y g++-11 libx11-dev libxdo-dev libwayland-dev libxkbcommon-dev libdrm-dev libgbm-dev libpam0g-dev libxtst-dev libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev zip g++ gcc git curl wget nasm yasm libgtk-3-dev clang libxcb-randr0-dev libxfixes-dev libxcb-shape0-dev libxcb-xfixes0-dev libasound2-dev libpulse-dev cmake make libclang-dev ninja-build\n'
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
            'name': 'Enable Desktop',
            'run': 'flutter config --enable-linux-desktop\n'
        },
        {
            'name': 'Build',
            'run': 'python3 ./build.py --flutter\n'
        },
        {
            'name': 'Upload Artifact',
            'if': "env.UPLOAD_ARTIFACT == 'true'",
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

yaml_output = yaml.dump(data, Dumper=Dumper, default_flow_style=False, sort_keys=False)
yaml_output = yaml_output.replace('\ntrue:', '\non:')

with open('.github/workflows/flutter-build.yml', 'w') as f:
    f.write(yaml_output)


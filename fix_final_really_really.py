import yaml

with open('.github/workflows/flutter-build.yml', 'r') as f:
    data = yaml.safe_load(f)

linux_job = data['jobs']['build-for-linux-flutter']

new_steps = []
for step in linux_job['steps']:
    if step.get('name') == 'Install dependencies':
        continue # Remove existing
    new_steps.append(step)
    
    if step.get('name') == 'Restore bridge files':
        # Insert Install dependencies right after restore bridge
        new_steps.append({
            'name': 'Install dependencies',
            'run': 'sudo apt-get install ca-certificates -y\nsudo apt-get update -y\nsudo apt-get install -y clang cmake gcc git g++ libclang-dev libgtk-3-dev llvm-dev nasm ninja-build pkg-config wget libxdo-dev libx11-dev libxext-dev libxfixes-dev libxi-dev libxrandr-dev libxtst-dev libxcb1-dev libx11-xcb-dev libxcb-damage0-dev libxcb-xfixes0-dev libxcb-shape0-dev libxcb-render-util0-dev libxcb-render0-dev libxcb-randr0-dev libxcb-composite0-dev libxcb-image0-dev libxcb-present-dev libxcb-xinerama0-dev libxcb-glx0-dev libpixman-1-dev libdbus-1-dev libgbm-dev libusb-1.0-0-dev libwayland-dev libxkbcommon-dev libdrm-dev libpam0g-dev libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev libappindicator3-dev\n'
        })

linux_job['steps'] = new_steps

class Dumper(yaml.Dumper):
    def increase_indent(self, flow=False, indentless=False):
        return super(Dumper, self).increase_indent(flow, False)

yaml_output = yaml.dump(data, Dumper=Dumper, default_flow_style=False, sort_keys=False)
yaml_output = yaml_output.replace('\ntrue:', '\non:')

with open('.github/workflows/flutter-build.yml', 'w') as f:
    f.write(yaml_output)


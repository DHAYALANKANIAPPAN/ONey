import yaml

with open('.github/workflows/flutter-build.yml', 'r') as f:
    data = yaml.safe_load(f)

linux_job = data['jobs']['build-for-linux-flutter']

# Find where to insert Install dependencies
steps = linux_job['steps']
new_steps = []
for step in steps:
    new_steps.append(step)
    if step.get('name') == 'Restore bridge files':
        new_steps.append({
            'name': 'Install dependencies',
            'run': 'sudo apt-get update -qq || true\nsudo apt-get install -yqq clang cmake ninja-build pkg-config libgtk-3-dev liblzma-dev libxdo-dev libx11-dev libwayland-dev libxkbcommon-dev libdrm-dev libgbm-dev libpam0g-dev libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev libappindicator3-dev\n'
        })

linux_job['steps'] = new_steps

class Dumper(yaml.Dumper):
    def increase_indent(self, flow=False, indentless=False):
        return super(Dumper, self).increase_indent(flow, False)

yaml_output = yaml.dump(data, Dumper=Dumper, default_flow_style=False, sort_keys=False)
yaml_output = yaml_output.replace('\ntrue:', '\non:')

with open('.github/workflows/flutter-build.yml', 'w') as f:
    f.write(yaml_output)


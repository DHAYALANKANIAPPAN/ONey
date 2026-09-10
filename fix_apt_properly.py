import yaml

with open('.github/workflows/flutter-build.yml', 'r') as f:
    data = yaml.safe_load(f)

# Find build-for-linux-flutter job
linux_job = data['jobs']['build-for-linux-flutter']
for step in linux_job['steps']:
    if step.get('name') == 'Install dependencies':
        step['run'] = "sudo apt-get update -qq || true\nsudo apt-get install -yqq libx11-dev libxdo-dev libwayland-dev libxkbcommon-dev libdrm-dev libgbm-dev libpam0g-dev libxtst-dev libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev libgtk-3-dev libxcb-randr0-dev libxfixes-dev libxcb-shape0-dev libxcb-xfixes0-dev libasound2-dev libpulse-dev\n"

class Dumper(yaml.Dumper):
    def increase_indent(self, flow=False, indentless=False):
        return super(Dumper, self).increase_indent(flow, False)

yaml_output = yaml.dump(data, Dumper=Dumper, default_flow_style=False, sort_keys=False)
yaml_output = yaml_output.replace('\ntrue:', '\non:')

with open('.github/workflows/flutter-build.yml', 'w') as f:
    f.write(yaml_output)


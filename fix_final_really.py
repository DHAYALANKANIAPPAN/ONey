import yaml

with open('.github/workflows/flutter-build.yml', 'r') as f:
    data = yaml.safe_load(f)

linux_job = data['jobs']['build-for-linux-flutter']

# Rebuild the steps list
new_steps = []
for step in linux_job['steps']:
    if step.get('name') == 'Install dependencies':
        continue # Remove existing
    if step.get('name') == 'Build':
        step['run'] = "python3 ./build.py --flutter\n" # Remove --skip-cargo
    
    new_steps.append(step)
    
    if step.get('name') == 'Restore bridge files':
        # Insert Install dependencies right after restore bridge
        new_steps.append({
            'name': 'Install dependencies',
            'run': 'sudo apt-get update -y\nsudo apt-get install -y libx11-dev libxdo-dev libwayland-dev libxkbcommon-dev libdrm-dev libgbm-dev libpam0g-dev libxtst-dev libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev clang cmake ninja-build pkg-config libgtk-3-dev liblzma-dev\n'
        })

linux_job['steps'] = new_steps

class Dumper(yaml.Dumper):
    def increase_indent(self, flow=False, indentless=False):
        return super(Dumper, self).increase_indent(flow, False)

yaml_output = yaml.dump(data, Dumper=Dumper, default_flow_style=False, sort_keys=False)
yaml_output = yaml_output.replace('\ntrue:', '\non:')

with open('.github/workflows/flutter-build.yml', 'w') as f:
    f.write(yaml_output)


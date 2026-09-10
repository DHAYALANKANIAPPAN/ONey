import yaml

with open('.github/workflows/flutter-build.yml', 'r') as f:
    data = yaml.safe_load(f)

linux_job = data['jobs']['build-for-linux-flutter']

# Remove the 'Install dependencies' step
linux_job['steps'] = [step for step in linux_job['steps'] if step.get('name') != 'Install dependencies']

# Add --skip-cargo to the Build step
for step in linux_job['steps']:
    if step.get('name') == 'Build':
        step['run'] = "python3 ./build.py --flutter --skip-cargo"

class Dumper(yaml.Dumper):
    def increase_indent(self, flow=False, indentless=False):
        return super(Dumper, self).increase_indent(flow, False)

yaml_output = yaml.dump(data, Dumper=Dumper, default_flow_style=False, sort_keys=False)
yaml_output = yaml_output.replace('\ntrue:', '\non:')

with open('.github/workflows/flutter-build.yml', 'w') as f:
    f.write(yaml_output)


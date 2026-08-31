import yaml
with open('.github/workflows/flutter-build.yml', 'r') as f: data = yaml.safe_load(f)
keep = ['generate-bridge', 'build-rustdesk-linux', 'build-for-windows-flutter']
if 'jobs' in data:
    jobs = data['jobs']
    for k in list(jobs.keys()):
        if k not in keep: del jobs[k]
    if 'build-rustdesk-linux' in jobs:
        matrix_jobs = jobs['build-rustdesk-linux'].get('strategy', {}).get('matrix', {}).get('job', [])
        jobs['build-rustdesk-linux']['strategy']['matrix']['job'] = [m for m in matrix_jobs if m.get('arch') == 'x86_64']
with open('.github/workflows/flutter-build.yml', 'w') as f: yaml.dump(data, f, sort_keys=False, width=1000)

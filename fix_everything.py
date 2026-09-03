import os, glob

# 1. Fix ALL workflows to only run manually (removes 'on: push' and 'on: pull_request')
for filepath in glob.glob('.github/workflows/*.yml'):
    with open(filepath, 'r') as f:
        lines = f.readlines()
    
    new_lines = []
    in_on_block = False
    for line in lines:
        # Find the trigger block
        if line.startswith('on:'):
            in_on_block = True
            new_lines.append('on: workflow_dispatch\n')
            continue
        
        # Skip everything inside the old trigger block
        if in_on_block:
            if line.strip() == '' or line.startswith(' ') or line.startswith('\t'):
                continue
            else:
                in_on_block = False
        
        if not in_on_block:
            new_lines.append(line)
            
    with open(filepath, 'w') as f:
        f.writelines(new_lines)
        
# 2. Fix the 4-hour queue freeze by removing 'windows-11-arm' ghost servers
flutter_build = ".github/workflows/flutter-build.yml"
if os.path.exists(flutter_build):
    with open(flutter_build, 'r') as f:
        lines = f.readlines()
        
    new_lines = []
    skip_mode = False
    for line in lines:
        if "target: windows-11-arm" in line or "target: aarch64-pc-windows-msvc" in line:
            skip_mode = True
            # Remove the previous line that starts the array item
            if len(new_lines) > 0 and "- {" in new_lines[-1]:
                new_lines.pop()
            continue
            
        if skip_mode:
            if "}" in line:
                skip_mode = False
            continue
            
        new_lines.append(line)
        
    with open(flutter_build, 'w') as f:
        f.writelines(new_lines)

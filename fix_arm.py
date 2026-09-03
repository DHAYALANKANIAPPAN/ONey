import os

def remove_arm_safely(filepath):
    if not os.path.exists(filepath): return
    with open(filepath, 'r') as f:
        lines = f.readlines()
    
    new_lines = []
    skip = False
    for line in lines:
        # If we find the ARM64 targets that cause the 4-hour freeze, activate skip mode
        if "target: windows-11-arm" in line or "target: aarch64-pc-windows-msvc" in line:
            skip = True
            # Remove the preceding '- {' line so the YAML array stays perfectly valid
            if len(new_lines) > 0 and "- {" in new_lines[-1]:
                new_lines.pop()
            continue
        
        if skip:
            if "}" in line:
                skip = False # End of the block, turn off skip mode
            continue
            
        new_lines.append(line)
        
    with open(filepath, 'w') as f:
        f.writelines(new_lines)

remove_arm_safely(".github/workflows/third-party-RustDeskTempTopMostWindow.yml")
remove_arm_safely(".github/workflows/flutter-build.yml")

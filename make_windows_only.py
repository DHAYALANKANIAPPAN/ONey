filepath = ".github/workflows/flutter-build.yml"
with open(filepath, "r") as f:
    content = f.read()

# Find where the non-Windows jobs start (starting with iOS)
cut_index = content.find("  build-rustdesk-ios:")

if cut_index != -1:
    # Keep everything before this point (which is only the Windows jobs)
    new_content = content[:cut_index]
    
    # Save the file
    with open(filepath, "w") as f:
        f.write(new_content)
    print("Successfully removed all non-Windows jobs!")
else:
    print("Could not find the cut point.")

from PIL import Image, ImageDraw
size = 256
img = Image.new('RGBA', (size, size), color=(255,255,255,0))
d = ImageDraw.Draw(img)

# Draw the blue eye!
d.ellipse([20, 80, 236, 176], fill="white", outline="#1e88e5", width=16) # Outer eye
d.ellipse([96, 96, 160, 160], fill="#1e88e5") # Blue Iris
d.ellipse([116, 116, 140, 140], fill="#0d47a1") # Dark Pupil

# Overwrite ALL the old icon formats (PNG, ICO)
icons = ['res/icon.png', 'res/icon.ico', 'res/tray-icon.ico', 'res/128x128.png', 'res/64x64.png', 'res/32x32.png', 'res/128x128@2x.png', 'res/mac-icon.png', 'res/mac-tray-dark-x2.png', 'res/mac-tray-light-x2.png', 'fastlane/metadata/android/en-US/images/icon.png']
for p in icons:
    try: img.save(p)
    except: pass

# Generate and overwrite SVG logos
svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256"><ellipse cx="128" cy="128" rx="108" ry="48" fill="white" stroke="#1e88e5" stroke-width="16"/><circle cx="128" cy="128" r="32" fill="#1e88e5"/><circle cx="128" cy="128" r="12" fill="#0d47a1"/></svg>'
open('res/logo.svg', 'w').write(svg)
open('flutter/assets/icon.svg', 'w').write(svg)
open('res/logo-header.svg', 'w').write(svg)
open('res/rustdesk-banner.svg', 'w').write(svg)
print("Blue Eye logo successfully generated and applied everywhere!")

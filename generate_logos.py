from PIL import Image, ImageDraw, ImageFont
size = 256
img = Image.new('RGBA', (size, size), color='#1e88e5')
d = ImageDraw.Draw(img)
try: 
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 80)
except: 
    font = ImageFont.load_default()
d.text(((size - d.textbbox((0,0),"ONey",font=font)[2])/2, (size - d.textbbox((0,0),"ONey",font=font)[3])/2 - 10), "ONey", fill="white", font=font)
img.save('res/icon.png')
img.save('res/icon.ico')
img.save('fastlane/metadata/android/en-US/images/icon.png')
svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256"><rect width="256" height="256" rx="64" fill="#1e88e5"/><text x="128" y="148" font-family="Arial" font-size="72" font-weight="bold" fill="white" text-anchor="middle">ONey</text></svg>'
open('res/logo.svg', 'w').write(svg)
open('flutter/assets/icon.svg', 'w').write(svg)
print("Logos successfully created and replaced!")

with open('.github/workflows/flutter-build.yml', 'r') as f:
    text = f.read()

old_checkout = """      - name: Checkout
        uses: actions/checkout@v4
      - name: Restore bridge files"""

new_checkout = """      - name: Checkout
        uses: actions/checkout@v4
        with:
          submodules: recursive
      - name: Restore bridge files"""

if old_checkout in text:
    text = text.replace(old_checkout, new_checkout)
    with open('.github/workflows/flutter-build.yml', 'w') as f:
        f.write(text)
    print("Fixed checkout!")
else:
    print("Checkout not found or already fixed.")

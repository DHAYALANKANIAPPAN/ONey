import re
with open("flutter/lib/common.dart", "r") as f: text = f.read()
replacement = '''Widget loadLogo() {
  return Container(
    padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
    child: Row(
      mainAxisSize: MainAxisSize.min,
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        SvgPicture.asset("assets/icon.svg", width: 32, height: 32),
        const SizedBox(width: 10),
        const Text("ONey", style: TextStyle(fontSize: 20, fontWeight: FontWeight.w700, letterSpacing: 1.2)),
      ],
    ),
  );
}
Widget loadIcon(double size) {
  return SvgPicture.asset("assets/icon.svg", width: size, height: size);
}'''
text = re.sub(r'Widget loadLogo\(\) \{.*?Widget loadIcon\(double size\) \{.*?\}\n', replacement + '\n', text, flags=re.DOTALL)
with open("flutter/lib/common.dart", "w") as f: f.write(text)

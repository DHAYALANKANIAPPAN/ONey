import re
with open("flutter/lib/models/terminal_model.dart", "r") as f: text = f.read()

if 'static final List<TerminalModel> allTerminals = [];' not in text:
    text = re.sub(r'class TerminalModel with ChangeNotifier \{', 'class TerminalModel with ChangeNotifier {\n  static final List<TerminalModel> allTerminals = [];\n  static bool broadcastMode = true;', text)
if 'allTerminals.add(this);' not in text:
    text = re.sub(r'TerminalModel\(this\.parent, this\.terminalId, \{this\.onClosed\}\) \{', 'TerminalModel(this.parent, this.terminalId, {this.onClosed}) {\n    allTerminals.add(this);', text)
if 'allTerminals.remove(this);' not in text:
    text = re.sub(r'void dispose\(\) \{', 'void dispose() {\n    allTerminals.remove(this);', text)

text = re.sub(r'Future<void> _handleInput\(String data\) async \{', 'Future<void> _handleInput(String data, {bool skipBroadcast = false}) async {\n    if (broadcastMode && !skipBroadcast) {\n      for (var t in allTerminals) {\n        if (t != this) {\n          t._handleInput(data, skipBroadcast: true);\n        }\n      }\n    }\n', text)
text = re.sub(r'terminal\.onOutput = \(data\) \{(\s*)if \(_suppressTerminalOutput\) return;(\s*)_handleInput\(data\);', r'terminal.onOutput = (data) {\1if (_suppressTerminalOutput) return;\2_handleInput(data, skipBroadcast: false);', text)

with open("flutter/lib/models/terminal_model.dart", "w") as f: f.write(text)

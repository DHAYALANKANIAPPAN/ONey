import urllib.request
import re

base_url = "https://raw.githubusercontent.com/rustdesk/rustdesk/master/"

# 1. Force-Download Pristine Files (Guarantees no old corrupted code!)
print("Downloading fresh files...")
files = [
    "flutter/lib/utils/multi_window_manager.dart",
    "flutter/lib/common/widgets/peer_tab_page.dart",
    "flutter/lib/models/terminal_model.dart"
]
for f in files:
    urllib.request.urlretrieve(base_url + f, f)

# 2. Patch multi_window_manager.dart (Force Terminals to open in Tabs)
print("Patching Window Manager...")
with open("flutter/lib/utils/multi_window_manager.dart", "r") as f: text = f.read()
text = re.sub(
    r'// Always create a new window for terminal[\s\S]*?return MultiWindowCallResult\(windowId, null\);',
    r'return _newSession(true, WindowType.Terminal, kWindowEventNewTerminal, remoteId, _terminalWindows, msg);',
    text
)
with open("flutter/lib/utils/multi_window_manager.dart", "w") as f: f.write(text)

# 3. Patch peer_tab_page.dart (Add the Green Terminal Button)
print("Patching Multi-Select UI...")
with open("flutter/lib/common/widgets/peer_tab_page.dart", "r") as f: text = f.read()
text = re.sub(
    r'deleteSelection\(\),',
    r'massTerminalSelection(),\n              deleteSelection(),',
    text
)
text = re.sub(
    r'Widget deleteSelection\(\) \{',
    '''Widget massTerminalSelection() {
    final model = Provider.of<PeerTabModel>(context, listen: false);
    return _hoverAction(
      toolTip: 'Mass Terminal (Broadcast to all selected)',
      onTap: () async {
        final peers = model.selectedPeers;
        for (var p in peers) {
            connect(context, p.id, isTerminal: true);
        }
        model.setMultiSelectionMode(false);
      },
      child: const Icon(Icons.terminal, color: Colors.green),
    );
  }

  Widget deleteSelection() {''',
    text
)
with open("flutter/lib/common/widgets/peer_tab_page.dart", "w") as f: f.write(text)

# 4. Patch terminal_model.dart (Broadcast typing to all tabs)
print("Patching Terminal Broadcast logic...")
with open("flutter/lib/models/terminal_model.dart", "r") as f: text = f.read()
text = re.sub(
    r'class TerminalModel with ChangeNotifier \{',
    'class TerminalModel with ChangeNotifier {\n  static final List<TerminalModel> allTerminals = [];\n  static bool broadcastMode = true;',
    text
)
text = re.sub(
    r'TerminalModel\(this\.parent, \[this\.terminalId = 0\]\) : id = parent\.id \{',
    'TerminalModel(this.parent, [this.terminalId = 0]) : id = parent.id {\n    allTerminals.add(this);',
    text
)
text = re.sub(
    r'void dispose\(\) \{',
    'void dispose() {\n    allTerminals.remove(this);',
    text
)
text = re.sub(
    r'Future<void> _handleInput\(String data\) async \{',
    'Future<void> _handleInput(String data, {bool skipBroadcast = false}) async {\n    if (broadcastMode && !skipBroadcast) {\n      for (var t in allTerminals) {\n        if (t != this) {\n          t._handleInput(data, skipBroadcast: true);\n        }\n      }\n    }\n',
    text
)
text = re.sub(
    r'terminal\.onOutput = \(data\) \{(\s*)if \(_suppressTerminalOutput\) return;(\s*)_handleInput\(data\);',
    r'terminal.onOutput = (data) {\1if (_suppressTerminalOutput) return;\2_handleInput(data, skipBroadcast: false);',
    text
)
with open("flutter/lib/models/terminal_model.dart", "w") as f: f.write(text)

print("Fleet Terminal completely rebuilt!")

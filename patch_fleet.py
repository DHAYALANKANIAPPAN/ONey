import re
# A. Force Terminals into Tabs (so only ONE window opens)
with open("flutter/lib/utils/multi_window_manager.dart", "r") as f: text = f.read()
text = re.sub(
    r'// Always create a new window for terminal[\s\S]*?return MultiWindowCallResult\(windowId, null\);',
    r'return _newSession(true, WindowType.Terminal, kWindowEventNewTerminal, remoteId, _terminalWindows, msg);',
    text
)
with open("flutter/lib/utils/multi_window_manager.dart", "w") as f: f.write(text)
# B. Add "Mass Terminal" green button to the Multi-Selection Bar
with open("flutter/lib/common/widgets/peer_tab_page.dart", "r") as f: text = f.read()
if "massTerminalSelection" not in text:
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
# C. Add Broadcast Logic to TerminalModel (syncs perfectly across tabs)
with open("flutter/lib/models/terminal_model.dart", "r") as f: text = f.read()
if 'allTerminals.add(this)' not in text:
    text = re.sub(
        r'class TerminalModel with ChangeNotifier \{',
        'class TerminalModel with ChangeNotifier {\n  static final List<TerminalModel> allTerminals = [];\n  static bool broadcastMode = true;',
        text
    )
    text = re.sub(
        r'TerminalModel\(this\.parent, this\.terminalId, \{this\.onClosed\}\) \{',
        'TerminalModel(this.parent, this.terminalId, {this.onClosed}) {\n    allTerminals.add(this);',
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

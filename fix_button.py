import re

with open("flutter/lib/common/widgets/peer_tab_page.dart", "r") as f:
    text = f.read()

# Precisely inject the missing 'context: context,' argument into our new button
text = re.sub(
    r'return _hoverAction\(\s*toolTip: \'Mass Terminal \(Broadcast to all selected\)\',',
    '''return _hoverAction(
      context: context,
      toolTip: 'Mass Terminal (Broadcast to all selected)',''',
    text
)

with open("flutter/lib/common/widgets/peer_tab_page.dart", "w") as f:
    f.write(text)

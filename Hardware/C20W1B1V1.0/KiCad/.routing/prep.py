from pathlib import Path
import re
p=Path('.routing/board.dsn')
s=p.read_text()
s=s.replace('(class kicad_default +3V3','(class kicad_default').replace('ACC_INT2 GND I2S_DATA','ACC_INT2 I2S_DATA')
i=s.index('    (class kicad_default')
s=s[:i]+'''    (class PowerSkip GND +3V3
      (circuit (use_via "Via[0-5]_500:300_um"))
      (rule (width 152.4) (clearance 152.4))
    )
'''+s[i:]
i=s.index('  (wiring')
s=s[:i]+s[i:].replace('(type route)','(type protect)')
p.with_name('work.dsn').write_text(s)

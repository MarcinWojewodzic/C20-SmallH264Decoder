from pathlib import Path
p=Path('.routing')
s=(p/'target.dsn').read_text()
layers=['F.Cu','In1.Cu','In2.Cu','In3.Cu','In4.Cu','B.Cu']
settings=['(autoroute on)','(postroute off)','(vias on)']
for i,layer in enumerate(layers):
    active='on' if i in (0,3,5) else 'off'
    direction='vertical' if i in (0,5) else 'horizontal'
    settings.append(f'(layer_rule {layer} (active {active}) (preferred_direction {direction}) (preferred_direction_trace_costs 1.0) (against_preferred_direction_trace_costs 1.4))')
where=s.index('    (boundary')
s=s[:where]+'    (autoroute_settings\n      '+'\n      '.join(settings)+'\n    )\n'+s[where:]
(p/'legacy.dsn').write_text(s)

"""Passive L2 filter calculations; does not model the TPS54495 control loop."""
from pathlib import Path
import json, csv, itertools
import numpy as np
from scipy import signal
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

out = Path('docs/analysis/audio_filter_2026-11-14')
out.mkdir(parents=True, exist_ok=True)
f = np.logspace(1, 6.3, 1800)

def response(freq, L=1e-6, rd=.027, cb=2e-3, rb=.0075, cc=88e-6, rc=.001, load=np.inf):
    s=2j*np.pi*np.asarray(freq)
    zl=rd+s*L
    yc=1/(rb+1/(s*cb))+1/(rc+1/(s*cc))+1/load
    zc=1/yc
    return zc/(zl+zc), 1/(1/zl+yc), 1/(zl+zc)

def system(L=1e-6, rd=.027, cb=2e-3, rb=.0075, cc=88e-6, rc=.001):
    # x=[inductor current, voltage on ideal bulk C, voltage on ideal ceramic C]
    # Inputs=[voltage before L2, downstream current sink].
    g=1/rb+1/rc
    v=np.array([1,1/rb,1/rc])/g
    a=np.zeros((3,3)); b=np.zeros((3,2))
    a[0]=-v/L; a[0,0]-=rd/L; b[0]=[1/L,1/(g*L)]
    a[1]=v/(rb*cb);a[1,1]-=1/(rb*cb); b[1,1]=-1/(g*rb*cb)
    a[2]=v/(rc*cc);a[2,2]-=1/(rc*cc); b[2,1]=-1/(g*rc*cc)
    return signal.StateSpace(a,b,np.vstack([v,[1,0,0]]),np.array([[0,-1/g],[0,0]]))

h,z,y=response(f)
hd,zd,yd=response(f,rb=.0075+.047/2)
freqs=[100,1000,3500,10000,20000,100000,700000]
rows=[]
for fi in freqs:
    hi,zi,yi=response(fi)
    rows.append(dict(frequency_Hz=fi,gain_dB=float(20*np.log10(abs(hi))),Zout_ohm=float(abs(zi)),filter_input_impedance_ohm=float(abs(1/yi))))
with (out/'frequency_points.csv').open('w',newline='') as fp:
    w=csv.DictWriter(fp,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

corners=[]
for L,rd,cb,rb,cc in itertools.product([.8e-6,1.2e-6],[.02,.03],[1.6e-3,2.4e-3],[.001,.0075],[44e-6,88e-6]):
    hc,zc,_=response(f,L,rd,cb,rb,cc)
    corners.append(dict(L=L,DCR=rd,Cbulk=cb,ESR_bulk_equiv=rb,Ccer=cc,peak_dB=float(np.max(20*np.log10(abs(hc)))),Zout_max_ohm=float(max(abs(zc))),h=hc,z=zc))

t=np.linspace(0,.035,70001)
ramps={};css=[10,100,220,330]
for c in css:
    ts=c*1e-9*.765/8e-6
    u=np.column_stack([3.298846*np.minimum(t/ts,1),np.zeros_like(t)])
    _,v,_=signal.lsim(system(),u,t)
    total=v[:,1]+66e-6*np.where(t<ts,3.298846/ts,0)
    ramps[c]=(v,total,ts)
tt=np.linspace(0,.002,4001)
_,step,_=signal.lsim(system(),np.column_stack([np.zeros_like(tt),np.ones_like(tt)]),tt)

fig,axs=plt.subplots(2,2,figsize=(12,8),layout='constrained')
ax=axs[0,0]
ax.semilogx(f,20*np.log10(abs(h)),label='Nominal (ESR model)')
ax.semilogx(f,20*np.log10(abs(hd)),ls='--',label='47 mOhm in series with each 1000 uF')
allh=np.array([20*np.log10(abs(c['h'])) for c in corners])
ax.fill_between(f,allh.min(0),allh.max(0),alpha=.2,label='Assumed parameter sweep')
ax.set(xlabel='Frequency [Hz]',ylabel='Vfiltered / Vbefore L2 [dB]',xlim=(10,1e6),ylim=(-100,5));ax.legend();ax.grid(True,which='both')
ax=axs[0,1];ax.loglog(f,abs(z),label='Nominal')
allz=np.array([abs(c['z']) for c in corners]);ax.fill_between(f,allz.min(0),allz.max(0),alpha=.2)
ax.set(xlabel='Frequency [Hz]',ylabel='Filter output impedance [ohm]',xlim=(10,1e6));ax.grid(True,which='both')
ax=axs[1,0]
for c,(v,total,ts) in ramps.items(): ax.plot(t*1000,total,label=f'C55={c} nF, SS={ts*1000:.1f} ms')
ax.set(xlabel='Time [ms]',ylabel='Capacitor charging current [A]',xlim=(0,35));ax.legend(fontsize=8);ax.grid(True)
ax=axs[1,1];ax.plot(tt*1000,-step[:,0]*1000)
ax.set(xlabel='Time [ms]',ylabel='Voltage sag for a +1 A load step [mV]');ax.grid(True)
fig.suptitle('L2=1 uH, DCR=27 mOhm, bulk=2000 uF / 7.5 mOhm, ceramic=88 uF / 1 mOhm\nIdeal regulated source before L2; no controller, ESL, current limit or switching model',fontsize=10)
fig.savefig(out/'filter_analysis.png',dpi=180);fig.savefig(out/'filter_analysis.pdf');plt.close(fig)

result=dict(model='Passive linear filter; ideal voltage source before L2. No closed-loop stability prediction.',
    nominal=dict(L_H=1e-6,DCR_ohm=.027,Cbulk_F=.002,ESR_bulk_equivalent_ohm=.0075,Ccer_F=88e-6,ESR_cer_equivalent_assumed_ohm=.001,
    approximate_f0_Hz=float(1/(2*np.pi*np.sqrt(1e-6*2088e-6))),peak_dB=float(max(20*np.log10(abs(h)))),Zout_max_ohm=float(max(abs(z))),
    one_amp_step_max_sag_mV=float(max(-step[:,0])*1000),one_amp_step_final_sag_mV=float(-step[-1,0]*1000)),
    softstart=[dict(C55_nF=c,tSS_ms=ts*1000,nominal_Icharge_A=2154e-6*3.298846/ts,linear_filter_peak_Icharge_A=float(max(total))) for c,(v,total,ts) in ramps.items()],
    corner_sweep_note='Illustrative assumptions, not guaranteed bounds. DCR min and ESR min unspecified; ESL absent.',
    max_corner_peak_dB=max(c['peak_dB'] for c in corners), max_corner_Zout_ohm=max(c['Zout_max_ohm'] for c in corners),frequency_points=rows)
extra=[]
for c in corners:
    hc,zc,_=response(f,c['L'],c['DCR'],c['Cbulk'],c['ESR_bulk_equiv']+.047/2,c['Ccer'])
    extra.append(float(max(20*np.log10(abs(hc)))))
result['optional_47mohm_each_bulk_series']=dict(nominal_peak_dB=float(max(20*np.log10(abs(hd)))),sweep_max_peak_dB=max(extra),nominal_Zout_max_ohm=float(max(abs(zd))))
hl,zl,_=response(.001)
assert abs(hl-1)<1e-5 and abs(zl-.027)<1e-5
assert abs(step[-1,0]+.027)<1e-6
assert all(abs(np.trapz(v[:,1],t)-2088e-6*3.298846)<1e-6 for v,total,ts in ramps.values())
(out/'results.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))

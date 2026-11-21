import xml.etree.ElementTree as E,json,pathlib,csv,collections
out=pathlib.Path('docs/analysis/review_2026-11-13_2235');r=E.parse(out/'netlist.xml').getroot();state=json.loads((out/'symbol_properties.json').read_text(encoding='utf-8'));cs={c.get('ref'):c for c in r.findall('./components/comp')};nets={}
for n in r.findall('./nets/net'):
 for p in n.findall('node'):nets[(p.get('ref'),p.get('pin'))]=n.get('name')
notes={}
def put(refs,status,note,source):
 for ref in refs:notes[ref]=(status,note,source)
def seq(prefix,a,b):return [prefix+str(i) for i in range(a,b+1)]
put(seq('C',1,76),'WARUNKOWO','Wartość napięciowa wystarczająca; brak MPN uniemożliwia weryfikację DC-bias/tolerancji/ESR; rozmieszczenie wymaga PCB.','schemat')
put(['C6','C7'],'OK_NOMINALNIE','100n z 10k: RC około 1 ms; BOOT0 do GND, NRST do 3V3 przez R2.','AN4938')
put(['C17','C19'],'WARUNKOWO','2.2u osobno z każdego VCAP do GND; potwierdzić efektywną pojemność i ESR <100mΩ.','AN4938')
put(['C43','C46'],'POPRAWIONO_WARUNKOWO','Równolegle: 2u nominalnie przy około 6.3 V; zapewnić >=1u efektywnie.','TPS923610')
put(['C44'],'WARUNKOWO','4.7u/10V przy 5V: zapewnić >=1u efektywnie, blisko VIN.','TPS923610')
put(['C47'],'OK_NOMINALNIE','100n odsprzęgania zasilania Y1; bez kondensatorów obciążenia na OUT oscylatora.','Kyocera_KC2520Z12_2880')
put(['C48','C76'],'OK_NOMINALNIE','100n lokalnego odsprzęgania MAX98357A.','MAX98357A_MAX98357B_LilyGO')
put(['C49','C50','C74','C75'],'WARUNKOWO','Po 2x22u na wzmacniacz; dobór nominalny wystarcza, potwierdzić >=10u efektywnej lokalnej pojemności.','MAX98357A_MAX98357B_LilyGO')
put(['C51','C52'],'OK_NOMINALNIE','100n bootstrap między VBST i SW właściwego kanału; nie do GND.','TPS54495')
put(['C55'],'DO_ZMIANY_LUB_PRZELICZENIA','10n -> tSS 0.956 ms; dla obecnych 2154u prąd ładowania około7.43A; rozruch i stabilność niezatwierdzone.','TPS54495')
put(['C56'],'WARUNKOWO','10n -> tSS 0.956ms; poprawne nominalnie dla niewielkiego obciążenia pojemnościowego kanału2.','TPS54495')
put(['C57'],'OK_NOMINALNIE','1u/10V z VREG5 do GND; potwierdzić pojemność efektywną.','TPS54495')
put(seq('C',58,63),'WARUNKOWO','Po3x22u=66u na wyjście przed dalszym odsprzęganiem; sprawdzić pojemność efektywną i całkowite obciążenie pętli DCAP2.','TPS54495')
put(seq('C',65,67)+seq('C',69,71),'OK_NOMINALNIE','Razem132u na wejściu5V; właściwa polaryzacja, ocena zależy od źródła5V i DC-bias. Nie zasilać12V.','TPS54495')
put(['C72','C73'],'DO_PRZELICZENIA','1000u/16V/15mΩ każdy; polaryzacja dobra, razem2000u zaL2 powoduje duże obciążenie rozruchowe i zmianę charakterystyki pętli.','KEMET_A768;TPS54495')
put(['R1','R2'],'OK','10k/63mW: BOOT0 pulldown i NRST pullup, wraz z C6/C7 około1ms.','AN4938')
put(['R3'],'NIEDOKONCZONE','10k pullup RESETX poprawny; brak sterowania/resetu sprzętowego LCD.','NHD-4.0-480480AF-ASXP-CTP')
put(['R4'],'OK','1.5Ω/1% ustawia133mA; moc około26.7mW.','TPS923610;Panasonic_ERJ;NHD')
put(['R5'],'OK','10k pulldown ADIM; PA7 podłączone. Moc przy3.3V około1.09mW.','TPS923610')
put(['R6','R7'],'OK','4.7k I2C do3V3 zgodnie z panelem; około0.70mA w stanieLOW.','NHD')
put(['R8'],'OK','0Ω ustawia GAIN U4 na GND, czyli12dB; R9 staje się dodatkowym obciążeniem szyny.','MAX98357A_MAX98357B_LilyGO')
put(['R9'],'ZBEDNY_ALE_NIESZKODLIWY','10k do3.3VA przy R8=0 doGND: 0.33mA,1.09mW; możnaDNP.','schemat')
put(['R10','R13'],'OK','73.2k górny rezystor FB; z22.1k daje3.29885V.','TPS54495')
put(['R11','R12'],'OK','22.1k dolny rezystor FB doGND; oba kanały3.29885V.','TPS54495')
put(['R14'],'DNP_WAZNE','Nie montować przy R15=0; jednoczesny montaż zwiera3.3VA zGND. AktualnyDNP poprawny.','schemat')
put(['R15'],'OK','0Ω doGND ustawia GAIN U6=12dB przy nieobsadzonym R14.','MAX98357A_MAX98357B_LilyGO')
put(['R16'],'OK','210k do3.3VA odpowiada prawemu kanałowi; ze wzoru94*3.3-100=210.2k.','MAX98357A_MAX98357B_LilyGO')
put(['L1'],'OK','10uH: wystarczające dla podświetlenia6.1V/133mA z5V.','AOTA-B252008S')
put(['L2'],'WARUNKOWO','1uH filtr3.3VA; prąd znamionowy wystarcza, ale 2mF za filtrem wymaga analizy rozruchu/rezonansu.','AOTA-B252010S')
put(['L3','L4'],'OK_NOMINALNIE','2.2uH,Irms7A,Isat10A typ.; odpowiedni zapas dla kanałów4A/2A; footprint8.3mm gap3.4mm zgodny.','Laird_MGAH0603;TPS54495')
put(['U1'],'WARUNKOWO','Pinout magistral poprawny; audio wymagaSAI1_B AF6,PC9 AF5; SWD/sterowanieLCD nadal nieukończone.','DS12117;RM0433')
put(['U2'],'UWAGA_NC','DQ/adresy sterujące poprawne; pin69 toNC, zbędna liniaFMC_A12 pozostaje.','IS45S32400J')
put(['U3'],'OK_WARUNKOWO','Topologia boost i ADIM poprawione; potrzebne5V i rzeczywiste parametry MLCC.','TPS923610')
put(['U4','U6'],'NIEDOKONCZONE','Zasilanie,I2S,GAIN,wybórL/R poprawne; OUTP/OUTN niepodłączone, brak złącza głośnika.','MAX98357A_MAX98357B_LilyGO')
put(['U5'],'RYZYKO_ROZRUCHU_STABILNOSCI','PinoutRSA16 i dzielniki poprawne; kanał1 obciążony2154u nominalnie przy SS10n.','TPS54495')
put(['Y1'],'OK','12.288MHz,3.3V,INH=HIGH,OUT->PC9/I2S_CKIN; nie jest źródłemHSE.','Kyocera_KC2520Z12_2880;DS12117;RM0433')
put(['J1'],'NIEDOKONCZONE','SPI39/40 poprawione,RGB zasilanie zgodne; CS/DC/RESET brakMCU. OrientacjaFPC wymaga sprawdzenia.','NHD')
put(['J2'],'NIEDOKONCZONE','VDD,GND,SCL,SDA zgodne; INT/RESET brakMCU;7=mechanicznepady.','NHD')
assert set(notes)==set(cs),(set(cs)-set(notes),set(notes)-set(cs))
with (out/'values_check.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.writer(f);w.writerow(['Reference','Value','DNP','Sheet','Status','Assessment','Source'])
 for ref,c in cs.items():w.writerow([ref,c.findtext('value'),state[ref]['dnp'],c.find('sheetpath').get('names'),*notes[ref]])
# DC continuity using populated zero-ohm resistors and inductors only.
parent={}
def find(x):
 parent.setdefault(x,x)
 if parent[x]!=x:parent[x]=find(parent[x])
 return parent[x]
def union(a,b):parent[find(a)]=find(b)
for ref,c in cs.items():
 if state[ref]['dnp']=='yes':continue
 if ref.startswith('L') or c.findtext('value')=='0R':union(nets[(ref,'1')],nets[(ref,'2')])
rails=['+5V','+3V3','+3.3VA','GND'];shorts=[(a,b) for i,a in enumerate(rails) for b in rails[i+1:] if find(a)==find(b)]
assert not shorts,shorts
res={'components':len(cs),'new_components':47,'DNP':['R14'],'DC_shorts_between_named_rails_with_populated_zero_ohms_and_inductors':shorts,'nominal_regulator_outputs_V':3.2988461538461538,'nominal_softstart_ms':0.95625,'channel1_nominal_capacitance_uF':2154,'nominal_charge_current_A':7.433411764705882,'scope':'Static DC union excludes IC internals; component values require MPN and PCB validation.'}
(out/'checks.json').write_text(json.dumps(res,indent=2),encoding='utf-8');print(json.dumps(res,indent=2))

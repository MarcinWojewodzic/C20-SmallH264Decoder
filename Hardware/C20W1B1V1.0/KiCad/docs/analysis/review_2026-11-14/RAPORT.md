# Przegląd schematu — 2026-11-14

Sprawdzono wszystkie 6 zapisanych plików schematu: 105 elementów, 187 sieci. Ponowny eksport KiCad CLI 10.0 i ERC wykonano dla aktualnych plików. Sumy SHA-256 potwierdziły zgodność wejść z istniejącymi materiałami roboczymi przeglądu `review_2026-11-13_2235`; wykorzystano je po weryfikacji. Schemat i PCB pozostawiono bez zmian. Względem pierwszej analizy doszło 47 elementów.

Uwzględniono informację projektanta: zwykłe GPIO i jeden INT będą przypisane podczas trasowania. Brak CS/DC/TP_INT/TP_RST oraz sterowania RESETX odnotowano jako planowane uzupełnienie, bez traktowania samego braku przypisania GPIO jako błędu projektu. Reset dotyku musi mieć zdefiniowany stan przed uruchomieniem.

## Najważniejsza poprawka: zasilanie audio

**Nie zatwierdzam obecnego zestawu C55/L2/C72/C73 do wykonania PCB.** U5.CH1 zasila przez L3 oraz L2 szynę +3.3VA. C72 i C73 to po 1000 µF/16 V/15 mΩ; oba są na tej samej szynie za L2. Wraz z C58–C60 i C49/C50/C74/C75 daje to około 2154 µF nominalnie, pomijając małe odsprzęganie. C55=10 nF daje według równania TI:

`tSS = C55 × 0,765 V / 8 µA = 0,956 ms`.

Gdyby wyjście miało śledzić tę rampę, samo ładowanie wymagałoby średnio `C × ΔV / Δt ≈ 7,43 A`, jeszcze bez obciążenia wzmacniaczy. CH1 jest kanałem 4 A. To oszacowanie wymaganego prądu, a nie prognoza rzeczywistego przebiegu: ograniczenie prądowe, filtr L2 i zabezpieczenia mogą spowodować wolniejszy start, zapadanie napięcia albo ponawianie startu.

Drugim problemem jest stabilność: TI zaleca dla 3,3 V L=2,2–3,3 µH i COUT=20–68 µF. L3=2,2 µH i lokalne 66 µF są bliskie układowi referencyjnemu, lecz dalsze 2088 µF za L2 zmieniają obciążenie i wprowadzają dodatkowy rezonans. Sprzężenie U5.VFB1 pobrano **przed L2**, więc nie kompensuje spadku DC na L2. Zwiększenie C55 samo nie potwierdzi stabilności. [TPS54495, równanie 2, tabela 1 i opis doboru filtra](https://www.ti.com/lit/ds/symlink/tps54495.pdf).

Zalecenie: najpierw usunąć z wariantu montażowego zbędne 2×1000 µF i dobrać rzeczywiste lokalne MLCC według wymagań wzmacniaczy; ponownie policzyć całkowite COUT, rozruch i obciążenie. Jeśli duża rezerwa energii jest wymagana, zaprojektować kontrolowane ładowanie oraz zweryfikować odpowiedź pętli i tłumienie filtra. Przy zachowaniu 2154 µF sam limit ładowania 1 A wymaga około 7,1 ms (około 75 nF SS nominalnie); to przykład obliczenia, nie zatwierdzony dobór C55.

CH2 ma lokalne 66 µF oraz odsprzęganie MCU/RAM/panelu. Trzeba uwzględnić całość i pojemność efektywną, a nie tylko C61–C63. Bez MPN kondensatorów nie da się zatwierdzić zgodności zakresu COUT.

## Pozostałe ustalenia wymagające działania

| Element / połączenie | Ocena i działanie |
|---|---|
| U2.69, FMC_A12 | Dokładny IS45S32400J używa A0–A11, pin 69 to NC. Usunąć zbędne połączenie i skorygować opis symbolu; nie traktować A12 jako kolejnego bitu adresu. |
| PA13/PA14, NRST | Nadal brak dostępu SWD. Zaplanować SWDIO, SWCLK, GND, odniesienie 3,3 V i NRST na złączu lub testpadach. To odrębne od dowolnych GPIO panelu. |
| Wejście +5V | Przetwornice są już pokazane, ale nie ma fizycznego wejścia zasilania. Dodać złącze/pady i określić wydajność źródła. Kondensatory 10 V oraz obwody podświetlenia wykluczają podanie tu 12 V mimo szerszego zakresu samego U5. |
| U4/U6.OUTP/OUTN | Cztery wyjścia są wolne. Zaplanować złącza głośników. Głośnik podłącza się między OUTP i OUTN; żaden z tych zacisków nie jest masą. Brak modelu/impedancji głośników uniemożliwia zatwierdzenie mocy i obciążenia. |
| R14 | Jest oznaczony DNP — poprawnie. Przy obsadzonym R15=0 Ω montaż R14=0 Ω spowoduje zwarcie +3.3VA do GND. Zachować DNP w BOM i produkcji. |
| R9 | Przy R8=0 Ω nie ustawia wzmocnienia; pobiera około 0,33 mA. Można pozostawić DNP. Nie powoduje zwarcia zasilania. |
| Kondensatory bez MPN | Same zapisy X5R/10 V/22 µF nie określają efektywnej pojemności, ESR i tolerancji. Szczególnie sprawdzić VCAP, wyjścia przetwornic, C43/C46 i lokalne zasilanie audio. |
| U1, odsprzęganie | VCAP mają osobne 2,2 µF do GND. Nadal brak wyraźnie przewidzianego lokalnego ≥4,7 µF przy MCU według AN4938; duża pojemność w innym miejscu szyny nie zastępuje odsprzęgania przy obudowie. |
| FPC J1/J2 | Numeracja elektryczna jest sprawdzona, ale orientację kontaktów i zgodność mechaniczną trzeba potwierdzić z panelem oraz footprintami przed zamówieniem PCB. |

## Co jest poprawne na poziomie schematu

- U5: pinout RSA16, oba bootstrapy 100 nF między VBST i SW, VREG5 z 1 µF do GND, EN1/EN2 na +5 V, masy i EP na GND. Dzielniki 73,2 kΩ/22,1 kΩ ustawiają oba wyjścia na **3,29885 V nominalnie**. Tolerancja rezystorów i napięcia odniesienia poszerza ten wynik; nie jest to gwarancja dokładności do milivolta.
- L3/L4=2,2 µH mają zapas znamionowego prądu względem kanałów 4 A/2 A. Przy 5 V i 3,3 V tętnienie nominalne wynosi około 0,73 A p-p. Prądy szczytowe przy pełnym obciążeniu to około 4,36 A i 2,36 A. Sprawdzenie temperatury i strat wymaga PCB.
- U4/U6: VDD, GND, EP, NC i cyfrowe wejścia odpowiadają TQFN16. PF6→DIN, PF8→BCLK, PF9→LRCLK realizować jako **SAI1_B, AF6**, mimo nazw sieci I2S. To nie jest zwykły dobór instancji SPI/I2S. U4 wybiera lewy kanał bezpośrednim SD_MODE do +3.3VA; U6 prawy przez R16=210 kΩ. R8/R15 do masy ustawiają 12 dB. [MAX98357A, konfiguracja SD_MODE i GAIN](https://www.analog.com/media/en/technical-documentation/data-sheets/MAX98357A-MAX98357B.pdf).
- Y1: aktywny oscylator 12,288 MHz, VCC=3,3 V, INH=HIGH, C47=100 nF, OUT→PC9. PC9 ustawić jako **I2S_CKIN, AF5**, a źródło zegara SAI wybrać z zewnętrznego wejścia. Nie jest to HSE ani MCLK wymagany przez MAX98357A; wzmacniacz nie potrzebuje MCLK. 12,288 MHz jest odpowiednie do rodziny 48 kHz przy poprawnych dzielnikach. Dla 44,1 kHz trzeba osobno dobrać źródło i konfigurację zegara.
- SDRAM: 32 DQ, A0–A11, BA0/BA1, DQM0–3 i sterowanie mają ciągłość i właściwe funkcje FMC, poza wspomnianym połączeniem do NC69. Pojemność 16 MiB. Timingi i odświeżanie wymagają konfiguracji firmware dla -6/A1.
- LCD: 24 bity RGB oraz synchronizacja zgodne z panelem NHD. **Poprawiono SPI: J1.39→PG11/SCK, J1.40→PD7/MOSI.** Poprzednie ostrzeżenie o ich zamianie jest nieaktualne.
- Podświetlenie: **PA7 jest już połączony z ADIM** (można użyć TIM3_CH2/AF2). R4=1,5 Ω daje około 133 mA i 26,7 mW, odpowiednio do wskazanego panelu. L1=10 µH ma zapas dla tego obciążenia. Dodano C46 równolegle do C43: 2 µF nominalnie, nadal trzeba zapewnić ≥1 µF efektywnie w warunkach pracy.
- Dotyk: J2.1/2/3/4=VDD/GND/SCL/SDA, podciąganie R6/R7=4,7 kΩ, PB6/PB7=I2C1 AF4. GPIO resetu i INT pozostają do przypisania zgodnie z planem projektanta.
- R1/R2=10 kΩ z C6/C7=100 nF tworzą około 1 ms RC dla BOOT0/NRST. Napięcia znamionowe pozostałych kondensatorów wystarczają dla oznaczonych szyn; polaryzacja C72/C73 jest poprawna.
- Nie wykryto zwarcia między +5V/+3V3/+3.3VA/GND przy uwzględnieniu obsadzonych rezystorów 0 Ω i dławików. Sprawdzenie statyczne nie modeluje wnętrza układów scalonych ani stanów przejściowych.

## ERC i materiały do weryfikacji

Aktualny ERC: **58 błędów i 14 ostrzeżeń**. 50 wpisów `pin_not_connected` obejmuje 46 wolnych pinów MCU i 4 wyjścia audio. Cztery `label_dangling` i cztery `isolated_pin_label` dotyczą planowanych GPIO/INT. Cztery `power_pin_not_driven` wynikają z deklaracji źródeł zasilania — najpierw dodać fizyczne wejście i poprawnie określić typy pinów, dopiero potem ewentualne PWR_FLAG. Ostrzeżenia o PAD audio na GND wynikają z typu `unspecified` w symbolu. Pozostają różnice bibliotek, dwie nazwy na tej samej sieci oraz końce przewodów/elementy poza siatką. Sama liczba ERC nie oznacza 58 niezależnych wad elektrycznych.

- [Ocena każdego ze 105 elementów](values_check.csv): referencja, wartość, DNP, wynik i uzasadnienie.
- [Komponenty](components.csv), [połączenia pin–sieć](connections.csv), [netlista XML](netlist.xml), [pełny ERC](erc.rpt), [wyniki obliczeń](checks.json), [sumy wejściowe](input_sha256.json).
- Dokumenty nowych części są zapisane w `../../datasheets`: TPS54495, MAX98357A/B (dwie kopie), AOTA-B252010S, dokładny Kyocera KC2520Z12.2880C1KX00, KEMET A768 i Laird MGAH0603. KEMET i Laird to kopie dokumentów producentów z serwerów dystrybucyjnych; historię źródeł i nieudanych pobrań zachowano w `../../download_logs`.
- W tym przeglądzie dodatkowo pobrano [TPS54495EVM — schemat, BOM i pomiary układu referencyjnego](../../datasheets/TPS54495EVM_user_guide.pdf) z [Texas Instruments](https://www.ti.com/lit/ug/slvu745a/slvu745a.pdf). Układ EVM nie zastępuje analizy przy 5 V oraz z filtrem L2 i dużą pojemnością.

Ocena obejmuje połączenia i nominalne wartości całego schematu. Nie stanowi zatwierdzenia routingu, termiki, DC-bias MLCC, charakterystyki pętli, EMC ani rzeczywistych sekwencji startu; te zależą od doboru konkretnych części, PCB i pomiarów. Dalsze poprawki można wykonać po rozstrzygnięciu pojemności na zasilaniu audio.

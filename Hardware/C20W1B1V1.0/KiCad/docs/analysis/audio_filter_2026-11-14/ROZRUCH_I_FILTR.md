# Rozruch TPS54495 i filtr zasilania audio

2026-11-14. R14 pozostaje DNP — ten punkt jest zamknięty. Poniżej propozycja zachowująca C72 i C73 po 1000 µF. Nie zmieniono schematu. Podczas analizy projektant zapisa? ponownie pliki; por?wnanie w?a?ciwo?ci element?w wykaza?o zmian? R9 na DNP. Parametry analizowanego zasilania i filtra pozosta?y takie same.

## Proponowany wariant do prototypu

1. **C55: 10 nF → 220 nF, X7R, ±10%, 16 V, np. 0603.** Ważna jest rzeczywista pojemność w zakresie napięcia SS do około 0,8 V, z uwzględnieniem temperatury. C56 nie trzeba zmieniać z powodu pojemności znajdującej się na CH1.
2. Zachować L3=2,2 µH, C58–C60 i L2=1 µH. Zachować sprzężenie R10/R11 **przed L2**. Nie przenosić samego punktu pomiarowego za L2: wymagałoby to ponownego zaprojektowania pętli z dodatkowym filtrem wewnątrz sprzężenia.
3. Zachować oba 1000 µF i lokalne kondensatory ceramiczne przy wzmacniaczach. Przewidzieć **osobny rezystor szeregowy przy każdym 1000 µF**, jako wariant montażowy 0 Ω / 47 mΩ. Dla pierwszego prototypu proponuję 47 mΩ, ±1%, co najmniej 0,25 W i z odpowiednią charakterystyką impulsową. Rezystory są wyłącznie w gałęziach kondensatorów, a nie szeregowo z całym zasilaniem wzmacniaczy. Ich prąd i moc w pracy zależą od przebiegu audio; 0,25 W nie zastępuje sprawdzenia prądu RMS.
4. **Nie rozpoczynać odtwarzania podczas rozruchu.** Firmware utrzymuje interfejs audio nieaktywny, a po ustaleniu zasilania rozpoczyna od zera i łagodnie zwiększa amplitudę. Jako początkowe założenie przy stabilnym 5 V przyjąć minimum 50 ms od włączenia EN1; docelowo uzależnić start od pomiaru gotowości szyny. U5 nie ma wyprowadzonego PGOOD. Sam upływ czasu przy niepoprawnym wejściu nie dowodzi gotowości.

To konkretny wariant do wykonania i sprawdzenia. Obliczenia potwierdzają zapas prądu ładowania i tłumienie samego filtra, ale nie są dowodem zapasu fazy całej przetwornicy D-CAP2.

## Obliczenia rozruchu

Za L3 jest około 2154 µF nominalnie: 66 µF przed L2 oraz 2000+88 µF za L2. Małe odsprzęganie pominięto. Przyjmuję napięcie wyjściowe 3,29885 V.

Według równania TI `tSS = CSS × 0,765 V / 8 µA`. Prąd potrzebny do śledzenia liniowej rampy to `I = C × V / tSS`:

| C55 | Czas nominalny | Prąd ładowania nominalny |
|---|---:|---:|
| 10 nF — obecnie | 0,956 ms | 7,43 A |
| 100 nF | 9,56 ms | 0,743 A |
| **220 nF — propozycja** | **21,04 ms** | **0,338 A** |
| 330 nF | 31,56 ms | 0,225 A |

Model liniowy L2 i rzeczywistych gałęzi pojemności daje dla 220 nF krótkie maksimum około 0,345 A zamiast 0,338 A. Nie jest to model ograniczenia prądowego ani sterowania TPS54495. Dla obecnych 10 nF wartość 7,43 A jest **zapotrzebowaniem**, a nie gwarantowanym prądem dostarczanym przez układ.

Z tolerancji CSS ±10%, prądu SS 7,6–8,4 µA oraz odniesienia 0,758–0,773 V wynika orientacyjnie 17,9–24,6 ms przy 25°C. Zakładając maksymalnie 2585 µF (+20% całej pojemności), napięcie 3,36 V i najkrótszy z tych czasów, prąd ładowania wynosi około **0,49 A**, bez drobnego przejściowego podbicia. To konserwatywny przykład tolerancji, a nie pełny gwarantowany zakres temperatur; brak MPN MLCC nie pozwala go zamknąć.

CH1 ma znamionowo 4 A. Przy braku odtwarzania zapas jest duży: do około 0,5 A ładowania dochodzi niewielki prąd spoczynkowy audio i pozostałe obciążenia tej szyny. Nawet obciążenie około 1 A podczas rampy daje orientacyjnie około 1,5 A, lecz należy uwzględnić faktyczny charakter obciążenia. Nie projektować normalnego rozruchu z celowym wchodzeniem w OCP. Wydłużenie SS wydłuża również powiązany z nim czas aktywacji UVP. [TPS54495: soft-start, ograniczenie prądowe, UVP](https://www.ti.com/lit/ds/symlink/tps54495.pdf).

Źródło 5 V musi wytrzymać równoczesny start CH2, wejściowe pojemności i podświetlenie. Powyższy wynik dotyczy ładowania na wyjściu CH1; nie jest całkowitym prądem pobieranym z 5 V.

## Model filtra i parametry

Analizowany układ:

```text
U5.SW1 ─ L3 2,2µH ── V1 ── L2 1µH / DCR ── +3.3VA ── wzmacniacze
                     │                       │
                  3×22µF              4×22µF + odsprzęganie
                     │                       │
                    GND               ┌───────┴───────┐
                                      R72           R73
                                       │             │
                                  C72 1000µF    C73 1000µF
                                       │             │
                                      GND           GND
Sprzężenie U5: z V1. R72/R73 to nowe proponowane elementy, bez nadanej
numeracji w projekcie; wartości 0Ω lub 47mΩ.
```

Z dokumentacji L2 AOTA-B252010S1R0MT: 1 µH ±20%, DCR typowo 27 mΩ, maksymalnie 30 mΩ; Isat 5,4/5,0 A i prąd cieplny 4,7/4,5 A według kolumn producenta. Wartości niższe nie są tu interpretowane jako limit maksymalnego dopuszczalnego prądu. [Abracon, tabela parametrów](https://abracon.com/datasheets/AOTA-B252010S.pdf).

C72 i C73 mają po 1000 µF; 15 mΩ na sztukę daje równolegle 7,5 mΩ przy przyjętym punkcie pracy. Jest to wartość katalogowa ESR przy 100 kHz, **nie znane minimum i nie pełna charakterystyka częstotliwościowa**. Cztery MLCC mają nominalnie 88 µF; przyjęto 1 mΩ ESR zastępczego. Brakuje ich MPN, więc to założenie modelu. Nie uwzględniono ESL, indukcyjności ścieżek, sprzężeń magnetycznych ani rozdzielenia kondensatorów po PCB.

Model częstotliwościowy:

`ZL = DCR + sL2`

`ZC = (ESRbulk + 1/(sCbulk)) || (ESRcer + 1/(sCcer))`

`H = ZC/(ZL+ZC)`, `Zout = ZL || ZC`.

Jest to filtr zasilany **idealnym, sztywnym źródłem w V1**, bez obciążenia rezystancyjnego. Odpowiedź na skok prądu obciążenia wyznaczono z modelu stanowego tych samych gałęzi.

## Wynik dla aktualnego filtra, bez dodatkowych rezystorów

- Częstotliwość charakterystyczna z 2088 µF i 1 µH: **około 3,48 kHz**.
- Zgrubny model drugiego rzędu daje `Z0≈21,9 mΩ` i `Q≈0,63`, po uwzględnieniu DCR oraz ESR. W dokładniejszym modelu równoległych gałęzi **nominalnie brak podbicia amplitudy**. Moje wcześniejsze ostrzeżenie o możliwym rezonansie wymaga więc doprecyzowania: duża pojemność sama nie dowodzi, że ten filtr jest źle tłumiony.
- Napięcie DC spada o około **27 mV na każdy amper**, do 30 mV/A według maksymalnego katalogowego DCR w warunkach jego specyfikacji. Przy 2 A: około 54 mV i 108 mW strat nominalnie, więcej po rozgrzaniu. Sprzężenie przed L2 tego spadku nie usuwa.
- Skok poboru o 1 A daje w modelu maksymalnie około **28,2 mV zapadu**, ustalającego się do 27 mV. To dodatkowa reakcja filtra; rzeczywista przetwornica może dodać własny zapad lub oscylacje.

| Częstotliwość | Nominalne przenoszenie tętnień V1 → +3.3VA |
|---|---:|
| 100 Hz | −0,001 dB |
| 1 kHz | −0,13 dB |
| 3,5 kHz | −3,39 dB |
| 10 kHz | −15,8 dB |
| 20 kHz | −23,8 dB |
| 100 kHz | −39,5 dB |
| 700 kHz | −65,5 dB w modelu bez ESL |

Filtr ogranicza przenikanie tętnień przetwornicy i wyższych częstotliwości. Nie izoluje skutecznie basowych zmian poboru prądu: przy 100 Hz i 1 kHz tłumienie jest znikome. Kondensatory magazynują energię, ale nie zastępują wydajnego źródła dla długiego impulsu basu. Wartość przy 700 kHz jest teoretyczna; rzeczywiste sprzężenia i pasożyty na PCB mogą ją istotnie pogorszyć.

## Czy dodawać tłumienie?

Nominalnie filtr go nie wymaga. Jednak producent nie podaje minimalnego DCR i minimalnego ESR; nie wolno traktować 15 mΩ jako gwarantowanego rezystora tłumiącego. W ilustracyjnym przeglądzie L=0,8–1,2 µH, Cbulk=1600–2400 µF, MLCC=44–88 µF, DCR=20–30 mΩ i ESRbulk równolegle=1–7,5 mΩ pojawiło się do **2,92 dB podbicia**. Część zakresów jest założona, więc to analiza wrażliwości, nie gwarantowane granice produkcyjne.

Dodanie **47 mΩ szeregowo z każdym 1000 µF** podnosi nominalny zastępczy ESR gałęzi bulk do `(15+47)/2=31 mΩ`. W tym samym przeglądzie podbicie spadło do około **0,04 dB**. Rezystory nie przewodzą prądu DC wzmacniaczy, więc nie dodają spadku DC całej szyny. Ceną jest mniejsza skuteczność gałęzi bulk przy szybkich zmianach oraz większe tętnienia i straty w tych gałęziach; lokalne MLCC pozostają podłączone bezpośrednio.

To powód proponowania miejsc na te rezystory. Można obsadzić 0 Ω po pozytywnych pomiarach bez dodatkowego tłumienia. Nie proponuję rezystora szeregowo z całym zasilaniem audio. Rezystor równoległy do L2 też tłumi, ale może mocniej pogorszyć tłumienie zakłóceń wysokiej częstotliwości. [TI o filtrach drugiego stopnia i kompromisach tłumienia](https://www.ti.com/document-viewer/lit/html/SSZT824/GUID-A0B0B1CE-7D79-4696-86B8-1B7446AB3B3C).

## Wpływ na TPS54495: co ustalono, a czego nie

Dużej pojemności **za dławikiem** nie można po prostu dodać do 66 µF i na tej podstawie zastosować zakresu COUT=20–68 µF z tabeli TI jak dla pojedynczego filtra. Poprzednia analiza była w tym punkcie zbyt uproszczona. Nie wynika z niej konieczność usunięcia C72/C73.

Filtr nadal wpływa na obciążenie V1. Dla parametrów nominalnych admitancja dodatkowej gałęzi przy 10 kHz ma moduł około 3,74 razy większy od admitancji samych lokalnych 66 µF; przy 20 kHz jest podobna i ma charakter głównie indukcyjny. Może więc częściowo kompensować admitancję lokalnych kondensatorów. Zmiana impedancji widzianej przez regulator jest realna mimo pozostawienia sprzężenia przed L2.

Nie wyznaczono zapasu fazy ani wzmocnienia pętli TPS54495. Model idealnego źródła nie obejmuje sterowania D-CAP2, przechodzenia CCM/Eco-mode, OCP i rzeczywistej impedancji wyjściowej regulatora. **Brak rezonansowego podbicia samego filtra nie oznacza automatycznie stabilności całej przetwornicy.** Dodatkowe tłumienie i wolniejszy start są uzasadnionym wariantem prototypowym, a nie zastępnikiem tego sprawdzenia.

## Sekwencja i sprawdzenie prototypu

Minimalny wariant bez nowych sygnałów sterujących: 220 nF SS1 i brak odtwarzania aż do ustalenia obu szyn. Obecnie U4.SD_MODE jest połączony bezpośrednio z +3.3VA, dlatego nie da się go wyciszyć GPIO bez zmiany tego połączenia. Jeśli potrzebne jest wymuszone sprzętowo wyłączenie wzmacniaczy podczas rampy lub awarii:

- zastąpić bezpośrednie połączenie U4.SD_MODE do szyny rezystorem około 2,2 kΩ;
- dodać osobny tranzystor NMOS do ściągania SD_MODE każdego wzmacniacza do GND; pozostawić R16=210 kΩ dla wyboru prawego kanału;
- wspólne bramki podciągnąć np. 100 kΩ do +3.3VA, aby domyślnie wyłączały audio, a MCU wyjściem open-drain zwierał bramki do GND dopiero po ustaleniu szyny;
- dobrać tranzystory do pewnego ściągania prądu przy napięciu bramki około 2,5–3,3 V. Nie zasilać SD_MODE z wcześniejszej, niezależnej szyny.

Tego wariantu nie trzeba dodawać wyłącznie po to, aby naładować kondensatory; daje kontrolowany stan audio niezależny od momentu rozpoczęcia pracy MCU. Sekwencja zegarów musi spełniać wymagania konkretnego trybu MAX98357A, zwłaszcza dodatkowe warunki dla BCLK=256 kHz / fs=8 kHz. [MAX98357A](https://www.analog.com/media/en/technical-documentation/data-sheets/MAX98357A-MAX98357B.pdf).

Na prototypie zmierzyć jednocześnie V1, +3.3VA, SS1 i prąd L3: zimny start, restart z częściowo naładowanymi kondensatorami, najniższe planowane 5 V i maksymalne obciążenie drugiego kanału. Następnie skoki obciążenia audio, np. 0,1→1 A oraz do rzeczywistego maksimum, z obserwacją obu stron L2. Sprawdzić brak hiccup, narastających lub podtrzymanych oscylacji, nadmiernego przeregulowania i zapadu 5 V. Dla oceny stabilności wykonać analizę pętli odpowiednią dla D-CAP2 / pomiary odpowiedzi, z docelowym BOM i PCB; orientacyjny cel projektu to ≥45° zapasu fazy i ≥6 dB zapasu wzmocnienia, przy poprawnej interpretacji pomiaru dla tego kontrolera.

## Pliki

- [Wykresy](filter_analysis.png), [wersja PDF](filter_analysis.pdf), [wyniki liczbowe](results.json), [punkty częstotliwościowe CSV](frequency_points.csv).
- Skrypt odtwarzający: `docs/tools/analyze_audio_filter.py`. Sprawdzono granice DC, ustalony spadek dla skoku 1 A oraz bilans ładunku w symulacji rampy.
- Dodatkowo pobrano [TI SNVA871](../../datasheets/TI_SNVA871_output_filter.pdf) i [TI SSZT824](../../datasheets/TI_SSZT824_second_stage_filter.pdf). Wnioski odnoszące się do TPS54495 oparto też na jego karcie; przykłady innych regulatorów nie stanowią potwierdzenia stabilności tego układu.

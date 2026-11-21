# Przegląd połączeń i dokumentacji — 18.11.2026

Sprawdzono netlistę i ERC aktualnego schematu oraz DRC z porównaniem PCB do schematu w KiCad 10. To przegląd projektu zapisanego na dysku. Poniższe przydziały pinów są propozycją do uzgodnienia z firmware.

## Sygnały bez połączenia z STM32

Siedem globalnych etykiet na arkuszu `uC` wisi bez przewodu. Każda ma drugi koniec podłączony do elementu na arkuszu Screen lub Sensors. Dodatkowo reset LCD ma jedynie podciągnięcie R3 do 3,3 V.

| Sygnał | Obecne zakończenie | Proponowany wolny GPIO U1 |
| --- | --- | --- |
| `~{TFT_CS}` | J1.37 (CSX) | PD4, pad 146, wyjście |
| `TFT_DC` | J1.38 (DCX) | PD5, pad 147, wyjście |
| `TFT_RST` | J1.31 (RESETX) i R3 | PD2, pad 144, wyjście |
| `TP_INT` | J2.5 | PG9, pad 152, EXTI9 |
| `TP_RST` | J2.6 | PG14, pad 157, wyjście |
| `MAG_INT` | U9.15 | PG3, pad 107, EXTI3 |
| `ACC_INT2` | IMU.9 | PH7, pad 84, EXTI7 |
| `ACC_INT1` | IMU.4 | PH6, pad 83, EXTI6 |
| Przycisk SW1 | styki 1+2 / 3+4 | PA0, pad 40, EXTI0 |
| Przycisk SW2 | styki 1+2 / 3+4 | PA2, pad 42, EXTI2 |

W proponowanym przydziale każde z sześciu wejść przerwań ma odrębną linię EXTI. GPIO dla LCD CS można sterować programowo. LCD ma już zegar i dane SPI na PG11 i PD7. Pozostałe wolne piny MCU z netlisty to PA11, PA12, PA15, PB4, PB5, PB12–PB15, PC0, PC1, PC2_C, PC3_C, PC7, PC8, PC12, PC13, PC15, PE2, PE3, PG13, PH1 i PI8. PC15 i PH1 są wyprowadzeniami oscylatorów, a PC2_C i PC3_C wymagają uwzględnienia przełączników analogowych MCU przy przydziale funkcji.

## SW1 i SW2

- **Pady footprintu odpowiadają rysunkowi CTS (rys. 2, str. 5).** Środki padów 1–4 są na X = ±4,20 mm, Y = ±2,25 mm, a padów LED na X = ±0,95 mm, Y = ±4,20 mm. Pady styków mają efektywnie 2,40 × 1,00 mm, a LED 0,80 × 2,40 mm. Numeracja i znacznik pinu 1 są zgodne z widokiem PCB producenta. Footprint ma przypisany lokalny model STEP. F.Fab i boczne linie F.SilkS mają rozstaw 6,4 mm, podczas gdy katalogowy korpus ma szerokość 6,8 mm. W projekcie footprintu brak F.CrtYd.
- **Styki w symbolu rozwijają się poprawnie.** Netlista zawiera osobno każdy pad z grup 1+2 i 3+4. Na obu przyciskach obie grupy są odłączone od reszty układu. Dla przycisku aktywnego stanem niskim można przypisać po jednej grupie do GPIO z podciągnięciem i po jednej do GND.
- **Symbol ma odwróconą topologię RGB.** Rysunek symbolu łączy katody we wspólny pin L3. W rzeczywistym 228CMVARGBFR L3 jest wspólną **anodą**, a L2, L4 i L1 to odpowiednio katody R, G i B. Wszystkie cztery wyprowadzenia LED są obecnie wolne. Przed podłączeniem RGB należy poprawić symbol i przewidzieć osobne ograniczenie prądu dla każdego koloru. Niebieska dioda ma katalogowo do 3,6 V napięcia przewodzenia, więc przy 3,3 V dostępny prąd i jasność zależą od egzemplarza i spadku napięcia na sterowniku. [CTS 228C](../../datasheets/CTS_228C.pdf)

## Pozostałe nowe elementy

- **J3 / STDC14 ma zamienione SWDIO i SWCLK.** Pin 4 (SWDIO) idzie do PA14, a pin 6 (SWCLK) do PA13. Poprawny przydział to J3.4 → PA13 i J3.6 → PA14. SWO na PB3, NRST, VTref, masy i krzyżowanie UART są zgodne z pinoutem STDC14. Footprint ma 14 padów elektrycznych i dwa otwory ustalające. [ST UM2910](../../datasheets/ST_UM2910.pdf), [rysunek Samtec](../../datasheets/Samtec_FTSH-DV.pdf)
- **Y2 i Y3 mają poprawny pinout elektryczny.** W obu generatorach 1 to wejście enable (podciągnięte do 3,3 V), 2 to GND, 3 to wyjście, a 4 to zasilanie. Y2 (25 MHz) trafia do PH0/OSC_IN, a Y3 (32,768 kHz) do PC14/OSC32_IN. Oba zegary wymagają trybu bypass w konfiguracji STM32. Pola Datasheet obu symboli wciąż wskazują kartę Kyocera, a przypisany footprint należy ocenić geometrycznie dla obu nowych obudów przed montażem. [Vishay XO22C](../../datasheets/Vishay_XO22C.pdf), [ECS-327MVATX](../../datasheets/ECS-327MVATX.pdf)
- **U10 jest podłączony do I²C1.** SDA.5 → PB7, SCL.6 → PB6, VDD.8 → +3V3, GND.4, A1.2, A2.3 i WP.7 → GND, NC.1 pozostawiony wolny. A1=A2=0 daje adresy 7-bitowe **0x50 i 0x51** dla dwóch stron po 256 bajtów. Brak kolizji z 0x30, 0x38, 0x6A i 0x76. [Infineon FM24CL04B](../../datasheets/FM24CL04B.pdf)
- **IMU ma oznaczenie `U?`.** KiCad ostrzega o niepełnej numeracji przy eksporcie netlisty.

## Stan PCB i reguły

- **ERC** zgłosił 93 naruszenia, w tym 7 wiszących etykiet i 7 ostrzeżeń o etykietach podłączonych tylko do jednego pinu.
- **DRC** zgłosił 285 brakujących połączeń, 137 naruszeń layoutu oraz 85 rozbieżności ze schematem (62 brakujące footprinty i 23 konflikty sieci). Brakuje na PCB m.in. J3, Y2, Y3, U10, SW1 i SW2. Połączenia styków przycisków i siedmiu sygnałów trzeba ustalić na schemacie przed aktualizacją PCB.

## Źródła pobranych PDF

| Dokument | Źródło |
| --- | --- |
| [CTS 228C Rev. H](../../datasheets/CTS_228C.pdf) | [CTS](https://www.ctscorp.com/Files/DataSheets/Switches/Tactile-Switches/CTS-Switches-Tactile-228C-Series-Datasheet.pdf) |
| [Vishay XO22C](../../datasheets/Vishay_XO22C.pdf) | [Vishay](https://www.vishay.com/docs/35065/xo22c.pdf) |
| [ECS-327MVATX](../../datasheets/ECS-327MVATX.pdf) | [ECS](https://helponline.ecsxtal.com/store/pdf/ECS-327MVATX.pdf) |
| [Infineon FM24CL04B](../../datasheets/FM24CL04B.pdf) | [Infineon](https://www.infineon.com/assets/row/public/documents/10/49/infineon-fm24cl04b-4-kbit-512-8-serial-i2c-f-ram-datasheet-en.pdf) |
| [Samtec FTSH-DV](../../datasheets/Samtec_FTSH-DV.pdf) | [Rysunek Samtec w kopii SnapEDA](https://s3.amazonaws.com/snapeda/datasheet/FTSH-107-01-L-DV-K-A-P-TR_Samtec.pdf) |
| [ST UM2910 Rev. 3](../../datasheets/ST_UM2910.pdf) | [Kopia STMcu Japan](https://www.stmcu.jp/wp/wp-content/uploads/2022/06/UM2910_Rev3.pdf), [Rev. 5 online](https://www.st.com/resource/en/user_manual/dm00813040-.pdf) |

# Analiza połączeń C20W1B1V1.0

Data: 2026-11-13. Zakres: zapisany schemat główny oraz arkusze uC, RAM i Screen. 58 elementów, 162 sieci (w tym sieci pojedynczych, niepodłączonych pinów). Schemat i PCB pozostawiono bez zmian.

## Wynik

Projekt wymaga uzupełnienia przed uruchomieniem. Potwierdzono brak sterowania podświetleniem z MCU oraz cztery niedokończone sygnały panelu/dotyku. Magistrale SDRAM i RGB mają ciągłość; dodatkowy adres pamięci dochodzi jednak do pinu NC. Brakuje także jawnego sposobu doprowadzenia 5 V i dostępu do programowania.

Podstawą są rzeczywista netlista KiCad (`netlist.xml`, `connections.csv`), ERC (`erc.rpt`) oraz dokumentacja w `../datasheets`. Nazwa sieci nie jest dowodem dostępności funkcji sprzętowej — sprawdzono również funkcje alternatywne MCU. Analiza nie obejmuje integralności sygnałowej, routingu, rozmieszczenia kondensatorów ani pomiarów gotowej płytki. Nieznany jest model LCD i kontrolera dotyku, więc ich pinoutów i wymagań nie można ostatecznie zatwierdzić.

## Problemy potwierdzone

| Priorytet | Połączenie | Dowód i skutek | Zalecenie |
|---|---|---|---|
| Wysoki | `uC_BACKLIGHT_PWM` | Sieć zawiera wyłącznie U3.2 i R5.1; R5.2 jest na GND. Nie ma pinu U1. Wejście ADIM pozostaje ściągnięte do masy, więc sterownik podświetlenia pozostanie wyłączony. | Doprowadzić sygnał z odpowiedniego wyjścia timera MCU. |
| Wysoki | `~{TFT_CS}`, `TFT_DC` | Każda sieć zawiera tylko J1.37 albo J1.38. Odpowiadające etykiety w uC wiszą bez połączenia. | Połączyć z GPIO, jeżeli wymaga tego sterownik LCD. Bez tego nie ma sterowania CS/DC. |
| Wysoki | `TP_INT`, `TP_RST` | Sieci zawierają tylko J2.5 i J2.6; po stronie uC etykiety nie dochodzą do pinów. | INT doprowadzić do GPIO/EXTI, RESET do GPIO lub obwodu resetu zgodnego z kontrolerem dotyku. |
| Średni | `FMC_A12` → U2.69 | Symbol opisuje pin jako A12/NC, lecz IS45S32400J w TSOP86 ma tutaj NC. Ta pamięć używa A0–A11. | Poprawić symbol dla dokładnej części, usunąć niepotrzebne połączenie do NC i oznaczyć pin jako niepodłączony. Nie zwiększa ono pojemności pamięci. |
| Średni | Brak dostępu SWD | U1.124/PA13 i U1.137/PA14 są niepodłączone. NRST ma tylko R2/C7. Brak złącza debug/programowania. | Zapewnić SWDIO, SWCLK, GND, odniesienie 3,3 V i najlepiej NRST na złączu lub testpadach. |

## Zasilanie, reset i start MCU

- `+5V` ma tylko C44.1, L1.1 i U3.1. W schemacie nie ma regulatora ani złącza dostarczającego to napięcie. Trzeba określić fizyczne wejście zasilania; sam symbol zasilania go nie tworzy.
- `+3V3` zasila U1, U2 oraz J1.4/J2.1. Nie ma pokazanego źródła/regulatora. Zasilanie przez jeden z tych styków jest możliwe tylko wtedy, gdy świadomie przewidziano je jako wejście i potwierdzono obciążalność oraz kierunek zasilania urządzenia zewnętrznego.
- Nie znaleziono bezpośredniego zwarcia między +5V, +3V3 i GND w netliście. Brak źródła na schemacie nie jest tym samym co zwarcie ani dowodem braku zasilania w większym systemie.
- Wszystkie pokazane piny VDD/VDD33_USB/VDDA/VREF+/VBAT i PDR_ON U1 dochodzą do +3V3, a VSS/VSSA do GND. U2 ma VDD/VDDQ na +3V3 oraz VSS/VSSQ na GND.
- VCAP U1.81 i U1.125 mają osobne kondensatory C17/C19 2,2 µF do GND. Nie są zwarte do 3,3 V. Parametry ESR, efektywna pojemność i ewentualne połączenie VCAP należy sprawdzić według zaleceń dla konkretnej rewizji MCU. [AN4938](https://www.st.com/resource/en/application_note/an4938-getting-started-with-stm32h74xig-and-stm32h75xig-mcu-hardware-development-stmicroelectronics.pdf)
- Na szynie MCU występują kondensatory 100 nF i 2,2 µF; brak osobnego kondensatora opisanego jako co najmniej 4,7 µF dla pakietu MCU. Dodać taki kondensator zgodnie z AN4938, a lokalne odsprzęganie potwierdzić na PCB. Suma pojemności na całej szynie nie potwierdza odsprzęgania przy pinie.
- BOOT0: R1 10 kΩ do GND i C6 100 nF do GND. NRST: R2 10 kΩ do +3V3 i C7 100 nF do GND. Stałe czasowe obu obwodów wynoszą około 1 ms. Brak łatwego przełączania BOOT0; sposób startu zależy również od option bytes.
- PH0/PH1 pozostają wolne, nie ma HSE ani LSE. To nie jest samo w sobie błąd: możliwa jest praca z oscylatorów wewnętrznych. Dokładność zegara obrazu i konfigurację PLL trzeba sprawdzić dla wymaganego trybu LCD.

## SDRAM: U1 ↔ U2

W netliście wszystkie 32 linie DQ mają po jednym końcu na U1 i U2, bez zamiany nazw bitów. Mapowanie danych MCU:

| DQ | GPIO U1 w kolejności rosnącego numeru DQ |
|---|---|
| 0–7 | PD14, PD15, PD0, PD1, PE7, PE8, PE9, PE10 |
| 8–15 | PE11, PE12, PE13, PE14, PE15, PD8, PD9, PD10 |
| 16–23 | PH8, PH9, PH10, PH11, PH12, PH13, PH14, PH15 |
| 24–31 | PI0, PI1, PI2, PI3, PI6, PI7, PI9, PI10 |

| Grupa | Połączenia MCU |
|---|---|
| A0–A5 | PF0–PF5 |
| A6–A9 | PF12–PF15 |
| A10/A11 | PG0/PG1 |
| BA0/BA1 | PG4/PG5 |
| DQM0–DQM3 | PE0, PE1, PI4, PI5 |
| CLK | PG8 |
| CKE / CS | PC5 / PC4 |
| RAS / CAS / WE | PF11 / PG15 / PH5 |

Mapowanie odpowiada funkcjom FMC. W szczególności PC4/PC5 obsługują SDNE0/SDCKE0 (AF12); nie trzeba przenosić tych sygnałów na zajęte przez LCD PH2/PH3. [DS12117, tabele pinów i AF](https://www.st.com/resource/en/datasheet/stm32h753ii.pdf)

Pinout U2 porównano z rysunkiem TSOP86 w lokalnej karcie ISSI: adresy, banki, DQ, DQM, sygnały sterujące i zasilanie są zgodne poza połączeniem do NC69. Pozostałe NC14/30/57/70/73 są oznaczone jako niepodłączone.

Parametry do firmware: 16 MiB, magistrala 32-bitowa, 4 banki wewnętrzne, 12 bitów adresu wiersza, 8 bitów kolumny; bank kontrolera odpowiadający SDNE0. Dla A1 wymagane jest 4096 odświeżeń w 64 ms (15,625 µs na odświeżenie). Timingi wyliczyć z rzeczywistego zegara FMC i karty wersji -6; częstotliwość graniczna SDRAM nie jest automatycznie dopuszczalną częstotliwością FMC. Sprawdzić sekwencję inicjalizacji, CAS, timingi i erratę MCU, następnie testować całą pamięć także podczas odczytu ramki przez LTDC. [Karta ISSI](https://www.issi.com/WW/pdf/42-45S32400J.pdf)

## LCD RGB, SPI i dotyk

| Sygnały | GPIO MCU w kolejności bitów 0–7 |
|---|---|
| R0–R7 | PH2, PH3, PA1, PB0, PA5, PA9, PB1, PG6 |
| G0–G7 | PE5, PE6, PA6, PG10, PH4, PB11, PI11, PD3 |
| B0–B7 | PE4, PA10, PD6, PA8, PG12, PA3, PB8, PB9 |

CLK=PG7, DE=PF10, HSYNC=PC6, VSYNC=PA4. Wszystkie 28 sygnałów RGB/synchronizacji dochodzi do J1. Mapowanie LTDC jest dostępne w MCU; część sygnałów wymaga AF9 zamiast typowego AF14 (PG10/G3, PG12/B4, PI11/G6). PH4/G4 używa AF14. [DS12117](https://www.st.com/resource/en/datasheet/stm32h753ii.pdf)

SPI: PG11 → J1.40 (SCK), PD7 → J1.39 (MOSI); wspólna instancja SPI1, AF5. Brak MISO może być zamierzony przy interfejsie tylko do zapisu. Nazwy lokalne SPI_CLK/SPI_MOSI i globalne TFT_CLK_SPI/TFT_DATA_SPI oznaczają te same przewody, co wyjaśnia dwa ostrzeżenia ERC.

TFT_RST (J1.31) ma tylko podciąganie R3 10 kΩ. MCU nie może wymusić resetu panelu. To ograniczenie może być dopuszczalne tylko przy odpowiedniej sekwencji startu i wymaganiach konkretnego LCD. J1.35 jest świadomie oznaczony NC — bez karty panelu nie da się potwierdzić, czy prawidłowo.

I²C: PB6 → J2.3/SCL i PB7 → J2.4/SDA, oba z podciąganiem 4,7 kΩ do 3,3 V. Dostępna instancja I2C1/AF4. Prąd stanu niskiego wynosi około 0,70 mA na linię. Poprawność czasów narastania zależy od pojemności taśmy, panelu i dodatkowych rezystorów na module. Nie ustalono modelu kontrolera dotyku ani jego wymagań INT/RESET.

## Podświetlenie

U3 ma zgodny z DRL pinout: 1 VIN, 2 ADIM, 3 FB, 4 GND, 5 VOUT, 6 SW. L1 jest między +5V i SW; VOUT dochodzi do J1.2 i C43 1 µF/35 V; J1.1 dochodzi do FB i R4 do masy. Topologia odpowiada synchronicznej przetwornicy boost. Nie jest potrzebna zewnętrzna dioda prostownicza. Polaryzację i układ LED musi potwierdzić karta panelu.

R4=1,5 Ω daje nominalnie 0,2 V/1,5 Ω = **133 mA** przy pełnym wysterowaniu. Moc R4 to około 26,7 mW. Nie potwierdzono, czy ten prąd jest dopuszczalny dla LCD. TPS923610 ma limit napięcia wyjściowego odpowiedni do wersji 24,5 V. C43 ma nominalnie 1 µF, dlatego utrata pojemności pod napięciem może zejść poniżej wymaganego minimum efektywnego. C44 4,7 µF/10 V po stronie wejścia wymaga analogicznej weryfikacji. Sterowanie ADIM powinno uwzględniać zalecany zakres PWM 10–200 kHz. [TPS923610](https://www.ti.com/lit/ds/symlink/tps923610.pdf)

L1=10 µH ma DCR do 570 mΩ, Isat min. 1,2 A i Irms min. 0,95 A według karty Abracon. Nie gwarantuje to zapasu do limitu przełącznika 1,8 A. Obliczyć prąd szczytowy przy minimalnym VIN, maksymalnym napięciu łańcucha LED i rozruchu; w razie potrzeby wybrać dławik z większym Isat. Brak parametrów LED uniemożliwia zamknięcie tego sprawdzenia. [Abracon](https://abracon.com/datasheets/AOTA-B252008S.pdf)

## Złącza i symbole

J2 `0522710679` ma **6 styków**, raster 1 mm, kontakty dolne. Footprint ma pady 1–6 oraz dwa pola mocujące o wspólnym numerze 7, podłączone do GND. Siedmiopinowy symbol jest więc mylący, ale nie oznacza braku siódmego styku sygnałowego: pin 7 reprezentuje mocowania. Warto zastąpić go symbolem 6 pinów + MH. [Molex](https://www.molex.com/en-us/products/part-detail/522710679?display=pdf)

J1 `62684-402100ALF` ma 40 styków, raster 0,5 mm i kontakty górne. Symbol zawiera dodatkowy pin MH41. Kierunek numeracji i stronę kontaktów taśmy należy zestawić z panelem — dokumentacja samego złącza nie ustala funkcji poszczególnych sygnałów LCD. Lokalna kopia dokumentacji rodziny ma stronę tytułową dla wersji 50-pinowej, lecz zawiera również rysunki i tabele rodziny 62684; nie jest kartą konkretnego LCD. [Amphenol](https://www.amphenol-cs.com/product/62684402100alf.html)

U3 nie został znaleziony w standardowej bibliotece Driver_LED; symbol jest osadzony w schemacie. J1 różni się od bibliotecznego Conn_01x40_Pin. Zachować i wersjonować własne symbole, żeby aktualizacja bibliotek nie usunęła pinów mocowań ani nie zmieniła numeracji.

## Interpretacja ERC

58 błędów i 12 ostrzeżeń = 70 wpisów:

| Typ | Liczba | Interpretacja |
|---|---:|---|
| pin_not_connected | 51 | Wolne GPIO MCU; dodać NC wyłącznie tam, gdzie faktycznie nie są potrzebne. Wśród nich są też nieudostępnione SWDIO/SWCLK. |
| label_dangling | 4 | Cztery niedokończone linie panelu/dotyku opisane wyżej. |
| power_pin_not_driven | 3 | Brak deklaracji źródła +3V3, GND, +5V; najpierw ustalić wejście zasilania, potem ewentualnie dodać PWR_FLAG. |
| isolated_pin_label | 4 | Te same cztery sygnały widziane od strony złączy. |
| unconnected_wire_endpoint | 2 | Końce przewodów do sprawdzenia w Screen; nie maskować bez ustalenia intencji. |
| endpoint_off_grid | 2 | Symbol +5V i przewód przy x=174,625 mm; wyrównać do siatki. |
| multiple_net_names | 2 | Dwie nazwy tych samych linii SPI. |
| lib_symbol_mismatch / lib_symbol_issues | 1 + 1 | Własne symbole J1 i U3. |

ERC opisuje część obiektów Screen jako arkusz `/`; przypisanie funkcjonalne sprawdzono w netliście. Brak błędu ERC na arkuszu RAM nie wyklucza problemu NC69 ani błędów firmware. Odłączone sterowanie ADIM również nie zostało bezpośrednio wychwycone przez ERC.

## Kolejność dalszych prac

1. Ustalić model LCD/dotyku, pinout FPC, dopuszczalny prąd LED i tryb interfejsu panelu.
2. Uzupełnić sterowanie podświetleniem, CS/DC i INT/RESET; zapewnić SWD i rzeczywiste wejścia zasilania.
3. Poprawić NC69 U2, symbole złączy i dostępność bibliotek; uzupełnić numery katalogowe elementów biernych.
4. Zweryfikować odsprzęganie i przetwornicę dla wybranych rzeczywistych części, następnie ponowić ERC.
5. Sprawdzić PCB pod kątem powrotów prądu, pętli SW, długości/opóźnień SDRAM i RGB. Uruchomić testy pamięci, obrazu, dotyku oraz pomiary napięć i temperatury przetwornicy.

Brak kompletnej aktualnej dokumentacji MCU w lokalnym pobraniu opisano w `../README.md`. Archiwalnego PDF DS12117 Rev 5 nie należy traktować jako potwierdzenia bieżących limitów 480 MHz; mapowania wymagające rozstrzygnięcia porównano z internetową wersją Rev 10.

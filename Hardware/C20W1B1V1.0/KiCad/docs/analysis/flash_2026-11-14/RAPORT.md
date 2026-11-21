# Flash U8 — W25R256JVEIQ

2026-11-14. Sprawdzono aktualnie zapisany schemat, ponownie eksportując netlistę oraz ERC KiCad CLI. Zakres tego przeglądu: nowy arkusz Flash i jego połączenia z MCU. Schemat i PCB pozostawiono bez zmian.

**Połączenia sygnałowe i zasilanie są poprawne. Zalecana poprawka przed wykonaniem: rezystor 10 kΩ z QSPI_CS do +3V3.** Obecnie CS łączy wyłącznie U8 i MCU, bez zewnętrznego podciągnięcia. W czasie resetu MCU nie zapewnia to pewnego stanu nieaktywnego. Karta wymaga, aby /CS podczas włączania podążał za VCC; wskazuje podciągnięcie jako sposób zapewnienia tego warunku.

## Przypisanie pinów

| Sygnał | U8 | U1 STM32H753II | Funkcja MCU |
|---|---|---|---|
| /CS | 1 | PB10, pin 79 | QUADSPI_BK1_NCS, AF9 |
| CLK | 6 | PB2, pin 58 | QUADSPI_CLK, AF9 |
| IO0 | 5 | PD11, pin 99 | QUADSPI_BK1_IO0, AF9 |
| IO1 | 2 | PD12, pin 100 | QUADSPI_BK1_IO1, AF9 |
| IO2 | 3 | PF7, pin 25 | QUADSPI_BK1_IO2, AF9 |
| IO3 | 7 | PD13, pin 101 | QUADSPI_BK1_IO3, AF9 |

Wszystkie sześć sieci zawiera dokładnie właściwy pin U8 i U1. Nie wykryto zamiany IO ani pomieszania banków. PF7 pozostaje dostępny: audio używa PF6/PF8/PF9. Pinout porównano z kartą W25R256JV, a funkcje alternatywne z DS12117 STM32H753 w lokalnej dokumentacji.

U8.8 ma +3V3; U8.4 i pad środkowy U8.9 mają GND. Dla obudowy E pad środkowy może być połączony z masą. C77=100 nF jest prawidłowo włączony między zasilanie i GND; umieścić go bezpośrednio przy U8 z krótką drogą powrotną do masy. 3,3 V mieści się w zakresie pamięci 2,7–3,6 V.

Footprint `WSON-8-1EP_8x6mm_P1.27mm_EP3.4x4.3mm` odpowiada nominalnym wymiarom obudowy E: korpus 8×6 mm, raster 1,27 mm i pad 3,4×4,3 mm. Nie sprawdzano wykonania montażu ani routingu PCB.

## Symbol i opis wymagają uporządkowania

U8 ma wartość **W25R256JVEIQ**, ale używa symbolu `Memory_Flash:W25Q128JVE`. Numery pinów są zgodne, więc sam wybór symbolu nie powoduje tu złego połączenia. Pozostały jednak nieprawidłowe metadane:

- opis 128 Mbit / 16 MiB zamiast **256 Mbit / 32 MiB**;
- link Datasheet do **W25Q128JV DTR**, zamiast W25R256JV;
- nazwy WP/HOLD/RESET na IO2/IO3 pochodzą z innej części i nie powinny być podstawą projektowania resetu tej pamięci.

Wariant IQ ma QE ustawione na stałe na 1 oraz domyślny DRV=50%. IO2 i IO3 należy zachować jako linie danych, bez zwierania do szyny. Nie ma potrzeby dodawania do nich podciągnięć tylko z powodu nazw WP/HOLD na użytym symbolu. W25R256JV obsługuje reset programowy.

## Konfiguracja i trasowanie

Użyć banku 1 QUADSPI, bez trybu dual-flash. Dla całych 32 MiB potrzebna jest obsługa adresowania ponad 24 bity — np. dedykowane instrukcje z adresem 4-bajtowym. Samo zwiększenie rozmiaru w kontrolerze nie zmienia formatu komend pamięci. Dla STM32 pole FSIZE wynosi 24, zgodnie z `2^(FSIZE+1)=32 MiB`. Skonfigurować właściwą instrukcję odczytu i dummy cycles; to pamięć STR, a nie zamiennik DTR/QPI tylko dlatego, że symbol ma takie słowa kluczowe.

Przy trasowaniu zapewnić ciągłą płaszczyznę masy i krótkie CLK/IO. Opcjonalnie przewidzieć miejsce na rezystor szeregowy CLK przy MCU, początkowo np. 22–33 Ω, z doborem po pomiarze zboczy. To propozycja do strojenia, nie wymagany rezystor wynikający z netlisty. Maksymalny zegar pamięci nie jest automatycznie osiągalnym zegarem interfejsu na tej PCB.

ERC nie zgłasza naruszeń w arkuszu `/Flash/`. Pełny projekt ma 93 wpisy; obejmują również inne, niedokończone arkusze. Nie są to 93 błędy nowej pamięci. Brak ostrzeżenia ERC o CS nie zastępuje sprawdzenia warunków startu.

## Zapisana dokumentacja i dowody

- [W25R256JV Rev D, 16.06.2020](../../datasheets/W25R256JV_RevD.pdf) — dokument Winbond, kopia z [Mouser](https://www.mouser.cn/datasheet/2/949/W25R256JV_RevD_06162020-1879221.pdf), obejmuje dokładny wariant W25R256JVEIQ. Dokument oznaczony jako Preliminary; nie przedstawiam go jako potwierdzonego najnowszego wydania.
- [W25R256JV Rev B, 03.09.2018](../../datasheets/W25R256JV.pdf) — dodatkowa starsza kopia z [DigiKey](https://mm.digikey.com/Volume0/opasdata/d220001/medias/docus/7957/256_W25R256JVEIQ.pdf).
- [Porównanie pinów CSV](pin_check.csv), [netlista](netlist.xml), [ERC](erc.rpt), [sumy wejściowych schematów](input_sha256.json).
- [Źródła pobrań i SHA-256](../../download_logs/sources_flash_2026-11-14.json). Pobranie z amerykańskiego serwera Mouser zakończyło się timeoutem; kopię Rev D zapisano z domeny Mouser.cn.

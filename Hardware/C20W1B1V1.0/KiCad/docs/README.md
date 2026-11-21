# Przegląd 2026-11-18

[GPIO, SW1/SW2 i dokumentacja nowych elementów](analysis/review_2026-11-18/RAPORT.md)

# Aktualny przegl?d ? 2026-11-16

[Raport: nowe czujniki i ca?y uk?ad](analysis/review_2026-11-16/RAPORT.md): 117 element?w, 200 sieci; brak kolizji I?C (0x30, 0x38, 0x6A, 0x76). Footprinty BME280 i MMC5983MA poprawne, geometria pad?w IMU do dopracowania wed?ug ST; typy pin?w symboli IMU i magnetometru do poprawy. INT celowo pomini?to. Panel: NHD-4.0-480480AF-ASXP-CTP.

Nowe dokumentacje: [BME280](datasheets/BME280.pdf), [MMC5983MA](datasheets/MMC5983MA.pdf), [LSM6DSV80X Rev 2](datasheets/LSM6DSV80X.pdf), [ST TN0018 Rev 7](datasheets/ST_TN0018_Mouser.pdf). ?r?d?a, wersje i ograniczenia w raporcie. C55 ma ju? 220 nF; starsze ostrze?enie o rozruchu z 10 nF jest nieaktualne.

Poni?sze wpisy opisuj? wcze?niejsze przegl?dy i mog? zawiera? nieaktualne ustalenia.

---

[Nowy przegl?d flash W25R256JVEIQ](analysis/flash_2026-11-14/RAPORT.md): pinout poprawny, zalecane 10 k? na CS; [karta Rev D](datasheets/W25R256JV_RevD.pdf) zapisana.

[Uzupe?nienie: rozruch z 2?1000 ?F i obliczenia filtra audio](analysis/audio_filter_2026-11-14/ROZRUCH_I_FILTR.md) ? propozycja C55=220 nF, wariant t?umienia i wykresy.

# Aktualny przegl?d ? 2026-11-14

[Raport ca?ego schematu: 105 element?w i 187 sieci](analysis/review_2026-11-14/RAPORT.md) oraz [ocena warto?ci ka?dego elementu](analysis/review_2026-11-14/values_check.csv). Najwa?niejsze: rozruch i stabilno?? zasilania audio z 2?1000 ?F. GPIO/INT uwzgl?dniono jako celowo niedoko?czone.

Dokumentacja nowych cz??ci: [TPS54495](datasheets/TPS54495.pdf), [uk?ad referencyjny TPS54495EVM](datasheets/TPS54495EVM_user_guide.pdf), [MAX98357A/B](datasheets/MAX98357A_MAX98357B.pdf), [AOTA-B252010S](datasheets/AOTA-B252010S.pdf), [Kyocera 12,288 MHz](datasheets/Kyocera_KC2520Z12_2880.pdf), [KEMET A768](datasheets/KEMET_A768.pdf), [Laird MGAH0603](datasheets/Laird_MGAH0603.pdf). ?r?d?a, kopie i ograniczenia opisano w raporcie.

Poni?ej zachowano **historyczny opis pierwszego przegl?du**, kt?rego liczby i cz??? otwartych problem?w s? ju? nieaktualne.

# Dokumentacja projektu C20W1B1V1.0

Zebrano 2026-11-13: **10 plików PDF dokumentacji**, obejmujących wszystkie **7 elementów z konkretnym numerem katalogowym** oraz dokumentację uzupełniającą. Nie jest to komplet wszystkich publikacji i rewizji producentów. Część pobrań jest blokowana; braki i starsze wydania opisano poniżej. Dodatkowy PDF `analysis/schematic.pdf` to eksport schematu projektu.

## Od czego zacząć

- [Analiza połączeń i zalecenia](analysis/ANALIZA_POLACZEN.md)
- [Schemat wszystkich arkuszy w PDF](analysis/schematic.pdf)
- [Oryginalny raport ERC: 58 błędów, 12 ostrzeżeń](analysis/erc.rpt)
- [Lista 58 elementów](components.csv)
- [Połączenia pin–sieć](analysis/connections.csv), [netlista XML](analysis/netlist.xml)
- [Rozmiary i sumy SHA-256 pobranych PDF](files.json)
- [Historia prób pobierania, źródła i błędy](download_log.json)

## Pobrane dokumenty

| Element | Lokalny dokument | Źródło i uwagi |
|---|---|---|
| U1 STM32H753IITx | [DS12117](datasheets/STM32H753_DS12117_octopart.pdf) | [Kopia dokumentu ST](https://datasheet.octopart.com/STM32H753ZIT6-STMicroelectronics-datasheet-159009244.pdf), **Rev 5, archiwalna**. Obejmuje rodzinę xI i LQFP176, mimo nazwy ZIT6 w adresie kopii. Aktualny [DS12117 Rev 10](https://www.st.com/resource/en/datasheet/stm32h753ii.pdf) odczytano przez wyszukiwarkę, lecz pobranie PDF do pliku kończyło się timeoutem. |
| U1 | [RM0433](datasheets/RM0433_mirror.pdf) | [Kopia dokumentu ST w repozytorium SparkFun](https://raw.githubusercontent.com/sparkfun/SparkFun_Qwiic_WAV_Trigger_Pro/main/Documents/dm00314099-stm32h742-stm32h743-753-and-stm32h750-value-line-advanced-arm-based-32-bit-mcus-stmicroelectronics.pdf), Rev 8, styczeń 2023, 3353 strony. |
| U1 | [AN4938 — projektowanie hardware](datasheets/AN4938_mirror.pdf) | [Kopia dokumentu ST w repozytorium SparkFun](https://raw.githubusercontent.com/sparkfun/SparkFun_Qwiic_WAV_Trigger_Pro/main/docs/assets/component_documentation/an4938-getting-started-with-stm32h74xig-and-stm32h75xig-mcu-hardware-development-stmicroelectronics.pdf), Rev 6, sierpień 2023. Nowsza [Rev 7](https://www.st.com/resource/en/application_note/an4938-getting-started-with-stm32h74xig-and-stm32h75xig-mcu-hardware-development-stmicroelectronics.pdf) dostępna pod linkiem producenta; bezpośrednie pobranie nie powiodło się. |
| U2 IS45S32400J-6TLA1-TR | [Karta IS42/45S32400J](datasheets/IS45S32400J_datasheet.pdf) | [Kopia dokumentu ISSI](https://atta.szlcsc.com/upload/public/pdf/source/20241111/FDF8C3E7BCEB7FD1F1BFC63B568651A5.pdf), wrzesień 2024. Wspólna karta obejmuje wariant -6, A1 i TSOP86. [Oryginał ISSI](https://www.issi.com/WW/pdf/42-45S32400J.pdf) zwracał stronę ochrony zamiast PDF. |
| U3 TPS923610DRLR | [Karta TPS923610](datasheets/TPS923610.pdf) | [Texas Instruments](https://www.ti.com/lit/ds/symlink/tps923610.pdf), Rev B, październik 2026. |
| U3 | [TPS923610EVM — instrukcja i schemat referencyjny](datasheets/TPS923610EVM_user_guide.pdf) | [Texas Instruments, SLVUDI4](https://www.ti.com/lit/ug/slvudi4/slvudi4.pdf). |
| L1 AOTA-B252008S100MT | [Karta rodziny AOTA-B252008S](datasheets/AOTA-B252008S.pdf) | [Abracon](https://abracon.com/datasheets/AOTA-B252008S.pdf), obejmuje dokładny wariant 10 µH. |
| R4 ERJ-3RQF1R5V | [Katalog rezystorów niskoomowych ERJ](datasheets/Panasonic_ERJ.pdf) | [Panasonic](https://industrial.panasonic.com/cdbs/www-data/pdf/RDN0000/AOA0000C313.pdf), zawiera ERJ3RQ, oznaczenia i zakres 1–9,1 Ω. Dokument rodziny, nie indywidualny certyfikat R4. |
| J1 62684-402100ALF | [Archiwalny dokument rodziny 62684](datasheets/Amphenol_octopart.pdf) | [Kopia dokumentu FCI/Amphenol](https://datasheet.octopart.com/62684-502100ALF-Amphenol-Communications-Solutions-datasheet-13508140.pdf). Strona produktowa dotyczy 50 styków; dołączone rysunki rodziny zawierają też 40 styków. **To nie jest aktualna karta dokładnego wariantu J1.** [Aktualna strona J1](https://www.amphenol-cs.com/product/62684402100alf.html). |
| J2 0522710679 | [Karta produktowa Molex 522710679](datasheets/Molex_product_sheet.pdf) | [Kopia dokumentu Molex](https://images.100y.com.tw/pdf_file/10-molex-52271-0679.pdf). Wiodące 0 w numerze jest równoważne; złącze ma 6 styków. [Strona Molex](https://www.molex.com/en-us/products/part-detail/522710679?display=pdf). |

Nazwy „mirror” i „octopart” oznaczają miejsce pobrania kopii; autorem dokumentu pozostaje producent. Starsze dokumenty zachowano świadomie i nie przedstawia się ich jako najnowszych specyfikacji.

## Dokumenty odnalezione, których nie udało się zapisać jako PDF

- U1: [bieżąca karta DS12117](https://www.st.com/resource/en/datasheet/stm32h753ii.pdf), [ES0392 — errata](https://www.st.com/resource/en/errata_sheet/es0392-stm32h742xig-and-stm32h743xig-device-limitations-stmicroelectronics.pdf), [PM0253 — Cortex-M7 programming manual](https://www.st.com/resource/en/programming_manual/pm0253-stm32f7-series-and-stm32h7-series-cortexm7-processor-programming-manual-stmicroelectronics.pdf) i nowsza AN4938: timeouty bezpośredniego połączenia z ST. **Errata nie jest dołączona jako lokalny PDF.**
- J1: [rysunek 62684](https://cdn.amphenol-cs.com/media/wysiwyg/files/drawing/62684.pdf), [specyfikacja 110-450H](https://cdn.amphenol-cs.com/media/wysiwyg/files/drawing/110-450h.pdf), [instrukcja aplikacyjna GS-20-097](https://cdn.amphenol-cs.com/media/wysiwyg/files/documentation/gs-20-097.pdf), [broszura OPU](https://cdn.amphenol-cs.com/media/wysiwyg/files/documentation/datasheet/flex/flexconnectors_050mm_opu.pdf): HTTP 403 przy zapisie, mimo możliwości odczytu przez wyszukiwarkę.
- J2: [rysunek Molex](https://www.molex.com/content/dam/molex/molex-dot-com/products/automated/en-us/salesdrawingpdf/522/52271/522710679_sd.pdf): timeout. Dokument odczytano online, ale nie zapisano jego pełnej kopii.

## Elementy bez jednoznacznej karty

**C1–C45 oraz R1–R3/R5–R7** nie mają producenta ani MPN. Podano jedynie wartości, dielektryk/napięcie/moc i obudowę. Nie przypisano im arbitralnie kart podobnych części. Do pełnej weryfikacji potrzeba dokładnego BOM, zwłaszcza ze względu na DC-bias i efektywną pojemność MLCC.

Brakuje też modelu LCD, łańcucha LED i kontrolera dotyku. J1/J2 to numery złączy, a nie paneli. Z tego powodu zgodność pinoutów i obciążenia podświetlenia pozostaje otwarta.

## Odtwarzalność

`tools/` zawiera skrypty pobierania i tworzenia zestawień. Uruchamiać je z katalogu głównego projektu, np. `python docs/tools/build_inventory.py`. Zapisane eksporty wykonano przez lokalny KiCad CLI 10.0. Komunikaty o braku uprawnień do klucza rejestru KiCad nie przeszkodziły w eksporcie; netlistę następnie poprawnie sparsowano. Nie wykonano zmian w plikach źródłowych projektu.

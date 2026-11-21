# Przegląd całego schematu i nowych czujników — 2026-11-16

Sprawdzono 8 arkuszy, 117 elementów i 200 sieci. Ponownie wyeksportowano netlistę, schemat PDF i ERC przez KiCad CLI 10.0.8. Uwzględniono dokładny panel **NHD-4.0-480480AF-ASXP-CTP**. Nie traktowano niepodłączonych INT czujników i panelu jako usterek. Pliki schematów, bibliotek i PCB pozostawiono bez zmian.

**Nie ma kolizji adresów I²C. Numery pinów nowych czujników są zgodne z dokumentacjami. BME280 i MMC5983MA mają poprawnie dobrane footprinty; footprint IMU ma zgodną numerację, ale wymaga dopracowania geometrii według ST. Symbole IMU i magnetometru mają nieprawidłowe typy elektryczne pinów.**

## 1. Wspólna magistrala I²C

Wszystkie cztery urządzenia są na tych samych sieciach SCL/SDA, sterowanych przez U1: PB6/pin164 i PB7/pin165 — I2C1, AF4. Nie są to odrębne magistrale.

| Urządzenie | Ustawienie na schemacie | Adres 7-bitowy | Bajt adresowy zapis / odczyt |
|---|---|---|---|
| U7 BME280 | CSB.2=3,3 V; SDO.5=GND | **0x76** | 0xEC / 0xED |
| U9 MMC5983MA | SPI_CS.4=3,3 V; adres fabrycznie stały | **0x30** | 0x60 / 0x61 |
| U? LSM6DSV80XTR | CS.12=3,3 V; SDO/TA0.1=GND | **0x6A** | 0xD4 / 0xD5 |
| FT5426G w panelu NHD, przez J2 | Adres z przykładu producenta panelu, str. 19 | **0x38** | 0x70 / 0x71 |

**0x70 podane przez NHD jest bajtem adresowym do zapisu, a nie adresem 7-bitowym.** W STM32 HAL argument adresu zwykle ma postać `adres_7bit << 1`; stosować konwencję konkretnej używanej funkcji. ST7701SN, część wyświetlająca panelu, korzysta z RGB i SPI, więc nie dodaje kolejnego adresu I²C. Pozostałe układy projektu również nie są urządzeniami tej magistrali.

R6/R7=4,7 kΩ są jedyną parą podciągnięć do +3V3; nie trzeba powielać jej przy każdym czujniku. Poziomy 3,3 V są zgodne z urządzeniami. **Magistralę ograniczyć do maks. 400 kHz** ze względu na MMC5983MA; uruchomienie zacząć od 100 kHz. Przy 4,7 kΩ i limicie narastania 300 ns budżet pojemności wynosi około `300 ns/(0,8473×4,7 kΩ)=75 pF`. Dla 100 kHz i 1000 ns jest to około 251 pF. To obliczenie RC, nie pomiar: uwzględnić FPC, panel, pady i ścieżki, a po wykonaniu sprawdzić zbocza oscyloskopem. Nie dokładać automatycznie kolejnych pull-upów.

Źródła: BME280, §6.2; MMC5983MA, str. 9 oraz opis I²C; LSM6DSV80X, tabela 12; lokalna karta dokładnego panelu NHD, str. 19.

## 2. Symbole, footprinty i połączenia czujników

### U7 — BME280

- Symbol: numery i funkcje pinów 1…8 odpowiadają tabeli producenta. GND.1/.7 i SDO.5 są na GND; VDD.8/VDDIO.6/CSB.2 na +3V3; SDI.3→SDA, SCK.4→SCL. **Połączenie poprawne dla I²C 0x76.**
- Footprint `Package_LGA:Bosch_LGA-8_2.5x2.5mm_P0.65mm_ClockwisePinNumbering`: poprawny. Potwierdzono kierunek numeracji po obrocie rysunku producenta, raster 0,65 mm, korpus 2,5×2,5 mm i pady 0,5×0,35 mm. Nie zastępować wersją z przeciwną numeracją. Rysunki: str. 38, 42–43 karty.
- C81/C82=4,7 µF są poprawnie włączone do masy. Bosch zaleca dwa lokalne 100 nF (str. 39). Zalecam przewidzieć po 100 nF bezpośrednio przy VDD/VDDIO; 4,7 µF mogą zostać jako dodatkowa pojemność. Sama większa pojemność nominalna nie dowodzi lepszego odsprzęgania przy wysokich częstotliwościach.
- Oddalić od przetwornic, MCU i wzmacniaczy; zapewnić dostęp powietrza do otworu obudowy. Sam pomiar temperatury BME280 odzwierciedla też nagrzanie PCB.
- Ostrzeżenie ERC o różnicy symbolu z biblioteką nie oznacza błędnego pinoutu — porównano numery z kartą.

### U9 — MMC5983MA

- Numery pinów są poprawne: SCL.1, VDD.2, CS.4, SDO.5, GND.9/.11, CAP.10, VDDIO.13, INT.15, SDA.16. Piny NC: 3, 6, 7, 8, 12, 14.
- VDD/VDDIO/CS są na +3V3, obie masy na GND; SCL/SDA na właściwych sieciach. SDO.5 jest pozostawione bez połączenia — poprawne dla I²C. C78/C79 są przy zasilaniu, C80=10 µF pomiędzy CAP a GND. **Topologia jest poprawna.** CAP i VDD są wewnętrznie zwarte według karty — CAP nie jest niezależnym regulowanym wyjściem.
- C80: producent wymaga minimum 10 µF o małym ESR blisko CAP (str. 11). Nominalne 10 µF X5R/0603 bez MPN nie gwarantuje tego po uwzględnieniu tolerancji i DC-bias przy 3,3 V. Dobrać konkretny kondensator zapewniający wymaganą pojemność efektywną, ewentualnie zwiększyć nominalną pojemność/obudowę. To warunek doboru części, nie błąd sieci.
- Footprint `Package_LGA:LGA-16_3x3mm_P0.5mm`: **zgodny** z rysunkiem na str. 20. Korpus 3×3 mm, raster 0,5 mm, rozstaw środków przeciwległych rzędów 2,55 mm, pady 0,45×0,30 mm, poprawna numeracja po obrocie. Nazwa odwołująca się do MMC5883MA w opisie biblioteki nie przeszkadza zgodności geometrii z MMC5983MA.
- **Symbol wymaga poprawy typów elektrycznych.** INT.15 powinien być wyjściem, SDO.5 wyjściem, SDA.16 dwukierunkowym, VDD/VDDIO/GND pinami `power_in`. Obecnie wszystkie są `input`, co zubaża lub fałszuje ERC. NC są ukrytymi wejściami — ustawić `no_connect` i widocznie udokumentować; nie łączyć ich do masy tylko dla usunięcia ERC. Złączone graficznie piny GND.9/.11 są w netliście obecne osobno i oba trafiają do GND.
- Biblioteka `MMC5983MA` ma w `sym-lib-table` bezwzględną ścieżkę poza projektem. Na tym komputerze istnieje; dla przenośności skopiować ją do `Lib/` i odwołać się przez `${KIPRJMOD}`. Brakuje też linku Datasheet w symbolu.
- Rozmieszczenie krytyczne: odsunąć magnetometr od L1–L4, głośników, torów dużych prądów i ferromagnetycznych części LCD. Kalibracja nie usuwa dowolnych, zmiennych zakłóceń od wzmacniaczy i przetwornic.

### U? — LSM6DSV80XTR

- **Przypisać oznaczenie**, np. U10 po sprawdzeniu wolnych numerów; U8 jest już pamięcią Flash. Eksport ostrzega o numeracji, mimo że robocza netlista powstała.
- Numery pinów odpowiadają tabeli 2 dokumentacji ST. VDD.8/VDDIO.5/CS.12→+3V3, GND.6/.7→GND, SDO/TA0.1→GND, SCL.13→SCL, SDA.14→SDA. SDX.2 i SCX.3 do GND są **prawidłowe w mode 1**; nie są to główne SCL/SDA. Nie włączać w firmware kontrolera sensor hub na tych zwartych do masy pinach. NC.10/.11 mają pozostać elektrycznie niepodłączone, ale przylutowane do padów.
- C83/C84=4,7 µF są poprawnie włączone, lecz ST pokazuje lokalne 100 nF na każdym z VDD/VDDIO (str. 40). Dodać/uwzględnić po 100 nF bezpośrednio przy pinach.
- Symbol ma wszystkie piny jako `passive`. Poprawić co najmniej zasilanie/masy na `power_in`, INT na `output`, SDA na `bidirectional`, SCL/CS na `input`; wielofunkcyjne piny uwzględnić zgodnie z interfejsem. NC ustawić `no_connect`. To kwestia jakości symbolu i działania ERC, nie wykryta zamiana numerów. Zgrupowane GND.6/.7 są poprawnie rozwinięte w netliście.
- Footprint `Package_LGA:Bosch_LGA-14_3x2.5mm_P0.5mm`: korpus, raster, kolejność padów i orientacja pinu 1 **pasują** do rysunku ST po przejściu z bottom view na top view. **Nie zatwierdzam jednak geometrii jako zgodnej z zalecanym land pattern ST.** Pady Bosch mają 0,675×0,25 mm. ST podaje metalizację układu 0,475×0,25 mm; TN0018 zaleca dla odstępu >0,2 mm powiększenie długości i szerokości o 0,1 mm, co daje nominalnie **0,575×0,35 mm**. Bosch daje większy występ na zewnątrz, ale nie poszerza padów. Zalecany jest footprint lokalny według ST i uzgodnienie pasty/maski z montażystą. Sam prefiks Bosch nie był podstawą oceny.
- Standardowy `LGA-14_3x2.5mm_P0.5mm_LayoutBorder3x4y` ma inną geometrię (0,625×0,35 mm) i również nie jest automatycznie dokładną realizacją wyliczenia TN0018. Nie podmieniałem footprintu na podstawie samej nazwy.

## 3. Cały układ — aktualne ustalenia

Porównano każdą parę element–pin z netlistą przeglądu 14.11. Wszystkie wcześniej obecne połączenia pozostały takie same poza sześcioma pinami MCU podłączonymi teraz do QSPI. Zmiana wartości w poprzednich elementach: C55 z 10 nF na 220 nF. DNP R9/R14 potwierdzono w bieżących plikach. Poniższa ocena dotyczy aktualnego zapisu.

| Obszar | Wynik / wymagane działanie |
|---|---|
| MCU, zasilanie i reset | Piny zasilania i VCAP mają połączenia; VCAP mają osobne 2,2 µF. NRST/BOOT0 mają RC 10 kΩ/100 nF. Nadal zaplanować lokalne ≥4,7 µF przy MCU zgodnie z AN4938 oraz dostęp SWDIO/PA13, SWCLK/PA14, GND, Vref i NRST. Pojemność przy czujnikach nie zastępuje lokalnej przy MCU. |
| SDRAM U2 | DQ0…31, A0…11, banki, DQM i sterowanie FMC mają właściwe połączenia. **U2.69 jest NC dla IS45S32400J**, a pozostaje podłączone do FMC_A12/PG2. Odłączyć i poprawić opis symbolu. Pojemność to 16 MiB, 12 bitów adresu wiersza. |
| Flash U8 | QSPI: PB2→CLK, PB10→CS, PD11→IO0, PD12→IO1, PF7→IO2, PD13→IO3; funkcje QUADSPI bank1 AF9 są poprawne i nie kolidują z audio. **Na CS nadal brak podciągnięcia**, zalecane 10 kΩ do +3V3 dla startu/resetu. Symbol W25Q128JVE ma zgodny pinout, ale błędne metadane dla W25R256JVEIQ: pojemność i Datasheet. WSON8 8×6 mm odpowiada obudowie E. U8 ma 32 MiB; firmware musi obsłużyć adresy ponad 24 bity. |
| Panel NHD | J1.5…28 to RGB24; J1.30/32/33/34 to PCLK/HS/VS/DE, zasilanie i masy zgodne. J1.39→PG11/SPI1_SCK i J1.40→PD7/SPI1_MOSI są poprawne. J1.35 jest NC. **CSX/J1.37 i DCX/J1.38 nadal bez sterowania**. RESETX/J1.31 ma pull-up R3, ale brak sterowania resetem; zapewnić wymagany przebieg startowy. |
| Dotyk FT5426G | J2.1…6=VDD/GND/SCL/SDA/INT/RST zgodnie z dokładnym panelem. **TP_RST/J2.6 nadal nie ma sterowania ani zewnętrznego ustalenia stanu**; zapewnić prawidłowy reset/sekwencję startu. Pominięto brak TP_INT zgodnie z poleceniem. |
| Złącza panelu | J2 to zalecany Molex 522710679, 6 pinów/1 mm. J1 jest 40 pinów/0,5 mm; NHD jako przykład podaje Molex 5051104091, a projekt używa Amphenol 62684-402100ALF. Zgodność sygnałów i rastra nie potwierdza strony kontaktów, kierunku wsunięcia FPC i wymiarów zatrzasku. Te cechy wymagają dopasowania mechanicznego z rzeczywistym panelem. |
| Podświetlenie | TPS923610 ma poprawną topologię i PA7→ADIM. R4=1,5 Ω przy 200 mV daje około 133 mA i 26,7 mW — blisko typowych 140 mA panelu i poniżej jego 168 mA maks. C43+C46 dają 2 µF nominalnie; sprawdzić pojemność efektywną przy napięciu LED. LED_K jest prawidłowo na rezystorze pomiarowym, nie należy go zwierać bezpośrednio do GND. |
| TPS54495 | Oba dzielniki 73,2 kΩ/22,1 kΩ dają nominalnie 3,299 V; bootstrapy, VREG5, masy i EP połączone poprawnie. C55=220 nF wydłuża nominalny soft-start CH1 do **21,04 ms**. Ładowanie około 2,154 mF do 3,3 V odpowiada średnio **0,338 A** bez obciążenia — poprzednia uwaga o zbyt szybkim starcie z 10 nF nie jest już aktualna. |
| Stabilność toru audio | C72/C73 po 1000 µF nadal są na +3.3VA za L2. Sprzężenie CH1 pobrane przed L2. Wolniejszy start nie dowodzi stabilności pętli i tłumienia filtra; nadal potrzebne pomiary odpowiedzi skokowej/startu i weryfikacja obciążenia. Patrz wcześniejsza analiza filtra. |
| Audio MAX98357A | VDD, GND, EP i wejścia poprawne; PF6/PF8/PF9 użyć jako SAI1_B AF6. Y1=12,288 MHz→PC9/I2S_CKIN AF5; dobrać konfigurację zegara SAI. U4/U6 wybierają kanały L/R. **R14 oraz R9 mają DNP**; R14 nie obsadzać przy R15=0 Ω. OUTP/OUTN nadal wymagają złączy głośników; wyjścia są mostkowe. |
| Wejście zasilania | W schemacie nadal brak fizycznego złącza/padów wejścia +5 V. Zdefiniować wydajność źródła i poprawnie zadeklarować źródła zasilania do ERC. |
| Nowe czujniki a zasilanie | Dodano sześć kondensatorów po 4,7 µF oraz 10 µF CAP magnetometru (CAP jest wewnętrznie zwarte z VDD). To zwiększa obciążenie pojemnościowe CH2 o około 38,2 µF nominalnie; uwzględnić cały rozproszony COUT, DC-bias i rozruch tej gałęzi. |

Nie stwierdzono statycznego zwarcia szyn przez obsadzone połączenia, rezystory 0 Ω i dławiki. Ocena nie modeluje wewnętrznych stanów układów i przebiegów startowych.

## 4. Kontrola bibliotek, ERC i stan PCB

Dla **wszystkich 117 elementów** odnaleziono przypisany plik footprintu i porównano komplety numerów pinów symbolu oraz padów footprintu: **brak brakujących lub dodatkowych numerów**. Wyniki w [footprint_pad_check.json](footprint_pad_check.json). To kontrola zgodności numeracji; nie zastępuje porównania wymiarów z dokumentacją. Nowe czujniki porównano również geometrycznie, jak opisano wyżej.

ERC: **67 błędów, 18 ostrzeżeń, łącznie 85 wpisów**. Znaczna część dotyczy wolnych GPIO MCU, wyjść audio i modelowania NC. W Sensors 12 wpisów pochodzi od sześciu NC magnetometru, dwa od NC IMU, a jeden od błędnego typu INT magnetometru. Nie są to dowody, że należy podłączyć NC albo obecnie uzupełnić INT. Nie traktuję braków INT jako usterek. Pozostają też cztery wpisy `power_pin_not_driven`, brak numeracji IMU, otwarte CS/DC/reset panelu, różnice bibliotek i końce przewodów poza siatką. ERC nie wykrywa kolizji adresów I²C ani nie potwierdza poprawności footprintów.

PCB ma 65 footprintów i tylko U1–U4 spośród układów scalonych; nie zawiera jeszcze czujników ani pozostałych nowych układów. **Ta analiza potwierdza przypisania footprintów w schemacie, nie rozmieszczenie i połączenia czujników na PCB.** Nie aktualizowano PCB automatycznie.

## 5. Dokumentacja i odtwarzalność

Pobrano i zweryfikowano jako PDF:

- [BME280](../../datasheets/BME280.pdf): Bosch BST-BME280-DS001-24, Rev 1.24, luty 2024, 60 stron, bezpośrednio od producenta. W stopkach części stron pozostało oznaczenie 1.23.
- [MMC5983MA](../../datasheets/MMC5983MA.pdf): MEMSIC Rev A, 3.04.2019, 20 stron, bezpośrednio od producenta.
- [LSM6DSV80X](../../datasheets/LSM6DSV80X.pdf): ST DS14764 Rev 2, kwiecień 2025, 180 stron; kopia dokumentu producenta z Mouser.cn. Bezpośrednie serwery ST zwracały timeouty.
- [ST TN0018](../../datasheets/ST_TN0018_Mouser.pdf): Rev 7, czerwiec 2023, 9 stron; kopia z Mouser.cn. Aktualniejszą Rev 8 odnaleziono na stronie ST, lecz nie udało się pobrać; ta sama reguła wymiarowania padów występuje również w Rev 8.
- Dodatkowe kopie zachowane jawnie jako starsze: [LSM6DSV80X Rev 1](../../datasheets/LSM6DSV80X_Rev1_DigiKey.pdf) i [TN0018 Rev 6](../../datasheets/ST_TN0018_Mouser_older.pdf). Podstawą oceny były odpowiednio Rev 2 i Rev 7 oraz porównanie reguły z Rev 8 online.

Istniejące karty panelu NHD, ST7701SN i FT5426G już były w `docs/datasheets`; nie pobierano ich ponownie. Nowe kondensatory nie mają MPN — nie przypisano arbitralnych kart podobnych części. Starsze braki dokumentacyjne MCU i złączy z poprzednich raportów pozostają odrębnymi ograniczeniami; nie deklaruję kompletności wszystkich not i errat projektu.

Źródła i hashe nowych pobrań: [download_log.json](download_log.json), [download_lsm_final.json](download_lsm_final.json), [download_TN0018.json](download_TN0018.json); nieudane próby również zachowano. Dowody: [schemat PDF](schematic.pdf), [netlista XML](netlist.xml), [połączenia CSV](connections.csv), [elementy CSV](components.csv), [ERC](erc.rpt), [właściwości symboli](symbol_properties.json), [sumy wejściowych schematów](input_sha256.json). Fragmenty kart i ich teksty zapisano w tym samym katalogu analizy.

Oficjalne źródła: [BME280](https://www.bosch-sensortec.com/media/boschsensortec/downloads/datasheets/bst-bme280-ds002.pdf), [MMC5983MA](https://www.memsic.com/Public/Uploads/uploadfile/files/20220119/MMC5983MADatasheetRevA.pdf), [LSM6DSV80X](https://www.st.com/resource/en/datasheet/lsm6dsv80x.pdf), [TN0018 Rev 8](https://www.st.com/resource/en/technical_note/CD00134799.pdf). Kopia ST Rev 2: [Mouser](https://www.mouser.cn/pdfDocs/lsm6dsv80x-2.pdf).

# Weryfikacja NHD-4.0-480480AF-ASXP-CTP

2026-11-13. Porównano ponownie wyeksportowaną netlistę projektu z kartą dokładnego panelu. Nie zmieniano schematu ani PCB. Ten raport uzupełnia i rozstrzyga otwarte punkty poprzedniej analizy.

## Dokumentacja

- [Panel NHD-4.0-480480AF-ASXP-CTP](../datasheets/NHD-4.0-480480AF-ASXP-CTP.pdf), 20 stron, wydanie początkowe z datą 09/03/2025: [źródło Newhaven](https://newhavendisplay.com/content/specs/NHD-4.0-480480AF-ASXP-CTP.pdf).
- [Sterownik LCD ST7701SN](../datasheets/ST7701SN.pdf), N1.0, 2021/11: [źródło Newhaven](https://support.newhavendisplay.com/hc/en-us/articles/14147699906711-ST7701SN).
- [Kontroler dotyku FT5426G](../datasheets/FT5426G.pdf): [źródło Newhaven](https://support.newhavendisplay.com/hc/en-us/articles/17688730921367-FT5426G).
- [Porównanie wszystkich 46 styków panelu z netlistą](NHD_pin_check.csv).

## Wynik: są wymagane poprawki

**Zamieniono SCK i MOSI na J1.39/J1.40.** Schemat trzeba poprawić, nawet przy prawidłowym sterowaniu podświetleniem. Ponadto brak połączeń MCU do CS/DC uniemożliwia wysłanie wymaganej inicjalizacji LCD.

| Pin J1 | Funkcja panelu | Obecna sieć i pin MCU | Wynik |
|---|---|---|---|
| 39 | SCL, zegar SPI | TFT_DATA_SPI → PD7/SPI1_MOSI | Błąd |
| 40 | SDA, dane SPI | TFT_CLK_SPI → PG11/SPI1_SCK | Błąd |
| 37 | CSX | ~{TFT_CS}, bez MCU | Uzupełnić GPIO |
| 38 | DCX | TFT_DC, bez MCU | Uzupełnić GPIO |
| 31 | RESETX | TFT_RST, tylko R3 do +3V3 | Brak możliwości wykonania resetu sprzętowego |

**Docelowo: PG11/SPI1_SCK → J1.39, PD7/SPI1_MOSI → J1.40.** Samo przemianowanie etykiet w jednym miejscu nie wystarczy, jeżeli nie zmieni rzeczywistego połączenia. Po poprawce ponownie wyeksportować netlistę. Programowe SPI na obecnych przewodach byłoby obejściem, ale nie pozwoli użyć obecnej pary jako sprzętowego SPI1.

Panel wymaga inicjalizacji ST7701SN przez SPI przed transmisją obrazu RGB. SPI nie służy tu do przesyłania pikseli. Zapewnić CS, DC oraz sterowany RESET; sam rezystor R3 nie wytwarza kontrolowanego impulsu resetującego. [Karta panelu, str. 4, 7 i 15](https://newhavendisplay.com/content/specs/NHD-4.0-480480AF-ASXP-CTP.pdf)

## Połączenia poprawne

Przypisanie wszystkich 24 bitów RGB i czterech linii synchronizacji odpowiada numeracji panelu. Nie wykryto odwrócenia kolejności bitów ani kanałów:

| J1 | Połączenie |
|---|---|
| 5–12 / 13–20 / 21–28 | R0–R7 / G0–G7 / B0–B7 |
| 30 / 32 / 33 / 34 | PCLK / HS / VS / DE |
| 4 | +3V3 |
| 3 / 29 / 36 | GND |
| 35 | NC — prawidłowo pozostawiony wolny |
| 2 / 1 | LED_A z U3.VOUT / LED_K do U3.FB i R4 |

LED_K nie należy zwierać bezpośrednio do GND mimo uproszczonego opisu „Ground” w tabeli panelu: w tym układzie prąd wraca przez R4, a FB mierzy spadek około 0,2 V. Zwarcie R4 pozbawiłoby układ pomiaru prądu.

## Podświetlenie: pozostawić TPS923610

Karta panelu podaje typowo **140 mA przy 6,1 V**, zakres prądu 117–168 mA oraz napięcie 5,4–6,8 V przy 140 mA. [Parametry panelu, str. 8](https://newhavendisplay.com/content/specs/NHD-4.0-480480AF-ASXP-CTP.pdf)

Z tego wynika dla obecnego obwodu:

- R4=1,5 Ω ustawia **133,3 mA** nominalnie, czyli około 95% typowego prądu panelu. To odpowiedni punkt pracy; nie trzeba zmieniać R4. Nie oznacza to dokładnie 95% luminancji.
- Z tolerancji FB 195–206 mV i R4 ±1% wynika około **128,7–138,7 mA** przy pełnym wysterowaniu, bez dodatkowego wpływu temperatury rezystora. Prąd pozostaje poniżej 168 mA. Moc R4 nominalnie wynosi 26,7 mW.
- Dla dokładnie około 140 mA można rozważyć 1,43 Ω/1%, ale ta zmiana jest opcjonalna. Nie ma powodu podnosić prądu do maksimum 168 mA.
- U3 reguluje napięcie między VOUT i GND: trzeba uwzględnić także 0,2 V na R4. Typowo będzie to około **6,3 V**, orientacyjnie do około 7 V przy górnej wartości napięcia LED. To odpowiedni zakres dla boost z wejściem 5 V.
- Przy 7 V/133 mA i założonej sprawności 85% prąd średni L1 to około 0,22 A. Przy 10 µH/1,1 MHz oszacowany prąd szczytowy wynosi około 0,29 A. Zapas obecnego dławika jest duży dla normalnej pracy tego konkretnego panelu; wcześniejsze zastrzeżenie dla obciążenia 24 V przestaje być istotne. Nadal obowiązuje weryfikacja rozruchu i PCB.
- C43=1 µF/35 V: napięciowo wystarcza. Należy jednak zapewnić co najmniej 1 µF **efektywnej** pojemności w warunkach pracy, uwzględniając tolerancję i DC-bias. Ponieważ brak MPN, nie da się tego potwierdzić. Dobrać konkretny MLCC; większa nominalna pojemność daje praktyczny zapas.
- C44=4,7 µF/10 V: zweryfikować efektywną pojemność przy 5 V i lokalne położenie przy VIN/GND. Obciążenie wyjścia nie wymaga prądu wejściowego rzędu 1 A; potrzebne są jednak odpowiednio krótkie połączenia i zapas zasilania na rozruch.
- Doprowadzić ADIM z MCU, zachowując R5 jako pulldown; wybrać PWM zgodnie z kartą TI. Bez tej poprawki U3 pozostanie wyłączony.

Obliczenia są oszacowaniem pracy ustalonej, a nie pomiarem sprawności i temperatury. Topologia i pinout U3 pozostają prawidłowe. [TPS923610, sekcje 6 i 8](https://www.ti.com/lit/ds/symlink/tps923610.pdf), [dławik Abracon](https://abracon.com/datasheets/AOTA-B252008S.pdf).

## Dotyk: J2

J2.1/2/3/4 odpowiadają VDD/GND/SCL/SDA panelu. R6/R7=4,7 kΩ do 3,3 V są właściwymi podciągnięciami wymaganymi w dokumentacji. J2 jest dokładnie zalecaną rodziną Molex 52271-0679. Pin 7 symbolu reprezentuje dwa mocowania footprintu, nie dodatkowy styk taśmy.

J2.5/INT i J2.6/RST mają poprawne numery, ale nie dochodzą do MCU. Dodać sterowanie resetem i połączenie INT do wejścia, najlepiej EXTI. INT można pominąć tylko przy świadomie zaimplementowanym odpytywaniu i odpowiedniej konfiguracji kontrolera; RST nie powinien pozostać bez zdefiniowanego stanu. Kontroler wymaga właściwej sekwencji zasilania/resetu. [FT5426G, rozdziały 2.5 i 3.5](https://support.newhavendisplay.com/hc/en-us/article_attachments/18307582846103)

Przykład producenta używa bajtów adresowych 0x70/0x71, co odpowiada **adresowi 7-bitowemu 0x38**. W API wymagającym adresu 7-bitowego nie podawać 0x70.

## Firmware i mechanika

Punkt startowy timingów LTDC według panelu: 480×480, PCLK 25 MHz; HSW/HBP/HFP=10/150/150, VSW/VBP/VFP=10/20/20. Razem 790×530, czyli około 59,7 Hz. Przy wpisywaniu do rejestrów LTDC uwzględnić ich kodowanie wartościami skumulowanymi i przesunięcie o 1; nie kopiować samych porchów do wszystkich pól.

Zgodność elektrycznych numerów pinów nie potwierdza orientacji złącza. J1 to Amphenol z kontaktami górnymi, podczas gdy karta wskazuje przykładowe Molex 5051104091. Przed produkcją porównać stronę odsłoniętych kontaktów FPC, kierunek wsunięcia i położenie styku 1 z rzeczywistym montażem panelu i footprintem. Sam raster 0,5 mm/40 pinów nie wystarcza do zatwierdzenia zamiennika.

## Minimalny zestaw poprawek

1. Zamienić połączenia SPI na J1.39/40.
2. Doprowadzić CSX, DCX, RESETX i ADIM do MCU.
3. Zapewnić reset dotyku oraz obsługę INT lub świadomie wybrane odpytywanie.
4. Dobrać rzeczywiste C43/C44 z potwierdzoną pojemnością efektywną; R4 i L1 można zachować dla tego panelu.
5. Zweryfikować orientację FPC J1, doprowadzenie zasilania oraz wykonać inicjalizację ST7701SN i test obrazu/dotyku.

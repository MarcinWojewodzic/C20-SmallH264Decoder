# Dokumentacja C20W1B1V1.0

## Układy scalone na schemacie

| Oznaczenie | Układ | Dokumentacja PDF |
| --- | --- | --- |
| U1 | STM32H753IITx | [DS12117](datasheets/STM32H753_DS12117_octopart.pdf), [RM0433](datasheets/RM0433_mirror.pdf), [ES0392](datasheets/STM32H753_ES0392.pdf), [PM0253](datasheets/STM32H753_PM0253.pdf), [AN4938](datasheets/AN4938_mirror.pdf) |
| U2 | IS45S32400J-6TLA1-TR | [Karta ISSI](datasheets/IS45S32400J_datasheet.pdf) |
| U3 | TPS923610DRLR | [Karta TI](datasheets/TPS923610.pdf), [Instrukcja płytki ewaluacyjnej](datasheets/TPS923610EVM_user_guide.pdf) |
| U4, U5 | MAX98357A | [Karta Analog Devices](datasheets/MAX98357A_MAX98357B.pdf) |
| U6 | TPS54495RSAR | [Karta TI](datasheets/TPS54495.pdf), [Instrukcja płytki ewaluacyjnej](datasheets/TPS54495EVM_user_guide.pdf) |
| U7 | W25R256JVEIQ | [Karta Winbond, Rev D](datasheets/W25R256JV_RevD.pdf) |
| U8 | MMC5983MA | [Karta MEMSIC](datasheets/MMC5983MA.pdf) |
| U9 | BME280 | [Karta Bosch](datasheets/BME280.pdf) |
| U10 | LSM6DSV80XTR | [Karta ST](datasheets/LSM6DSV80X.pdf), [Wytyczne montażu MEMS](datasheets/ST_TN0018_Mouser.pdf) |
| U11 | FM24CL04B-GTR | [Karta Infineon](datasheets/FM24CL04B.pdf) |

## Pozostałe elementy z numerem katalogowym

| Oznaczenie | PN | Dokumentacja PDF |
| --- | --- | --- |
| C51, C82 | A768MS108M1CLAS015 | [KEMET A768](datasheets/KEMET_A768.pdf) |
| J1 | FTSH-107-01-L-DV-K-A | [Rysunek Samtec](datasheets/Samtec_FTSH-DV.pdf), [zalecany footprint](datasheets/Samtec_FTSH-DV_footprint.pdf) |
| J2 | 62684-402100ALF | [Dokument rodziny Amphenol 62684](datasheets/Amphenol_octopart.pdf) |
| J3 | 0522710679 | [Karta produktowa Molex 522710679](datasheets/Molex_product_sheet.pdf) |
| L1 | AOTA-B252008S100MT | [Abracon AOTA-B252008S](datasheets/AOTA-B252008S.pdf) |
| L2, L3 | MGAH06032R2M-10 | [Laird MGAH0603](datasheets/Laird_MGAH0603.pdf) |
| L4 | AOTA-B252010S1R0MT | [Abracon AOTA-B252010S](datasheets/AOTA-B252010S.pdf) |
| MK1, MK2 | IM69D130V01XTSA1 | [Karta Infineon](datasheets/IM69D130.pdf), [karta produktu z pełnym PN](datasheets/IM69D130_product_brief.pdf) |
| R6 | ERJ-3RQF1R5V | [Panasonic ERJ-3RQ](datasheets/Panasonic_ERJ.pdf) |
| SW1, SW2 | 228CMVARGBFR | [CTS 228C](datasheets/CTS_228C.pdf) |
| Y1 | XO22C3EREHX25M000 | [Vishay XO22C](datasheets/Vishay_XO22C.pdf) |
| Y2 | KC2520Z12.2880C1KX00 | [Kyocera KC2520Z](datasheets/Kyocera_KC2520Z12_2880.pdf) |
| Y3 | ECS-327MVATX-2-CN-TR | [ECS-327MVATX](datasheets/ECS-327MVATX.pdf) |
| Panel LCD, opis na arkuszu Screen | NHD-4.0-480480AF-ASXP-CTP | [Panel Newhaven](datasheets/NHD-4.0-480480AF-ASXP-CTP.pdf), [sterownik ST7701SN](datasheets/ST7701SN.pdf), [kontroler dotyku FT5426G](datasheets/FT5426G.pdf) |

Tabele obejmują 28 oznaczeń elementów z podanym PN lub modelem oraz panel LCD wskazany w opisie schematu.

## Źródła i wydania

[Rejestr źródeł](sources.json) zawiera adresy pobrań, kopie wykorzystane z Git, sumy SHA-256 i adresy dokumentów, których nie udało się pobrać. Dla STM32 lokalne DS12117, RM0433, AN4938 i PM0253 pochodzą ze starszych wydań. Dla pamięci Winbond lokalnie dostępna jest m.in. rewizja D, a nowsza rewizja E jest dostępna pod odnośnikiem. [Dokumentacja STM32H753II](https://www.st.com/en/microcontrollers-microprocessors/stm32h753ii.html) · [W25R256JV Rev E](https://static6.arrow.com/aropdfconversion/5119136c1181785a4815dd38be975c04ef908305/w25r256jvreve03162022.pdf)

Dla J2 dostępny lokalnie PDF Amphenol 62684 obejmuje rysunek rodziny z wariantem 40-stykowym. Dla J3 zapisano kartę dokładnego modelu Molex, a osobny rysunek jest pod odnośnikiem producenta. [Amphenol 62684-402100ALF](https://www.amphenol-cs.com/product/62684402100alf.html) · [Rysunek Molex 522710679](https://www.molex.com/content/dam/molex/molex-dot-com/products/automated/en-us/salesdrawingpdf/522/52271/522710679_sd.pdf)

# C20 — H.264 decoding on STM32

C20 is an embedded video project built around a custom STM32H753 board and a software H.264/AVC decoder written from scratch. The first goal is to decode a short, low-resolution clip and display it on the board's LCD. From there, the project will measure how far the Cortex-M7 and external SDRAM can take it.

**Project status:** KiCad hardware design and STM32Cube firmware scaffolding are in the repository. The H.264 decoder and playback pipeline are planned.

## Hardware

Board revision **C20W1B1V1.0** pairs the STM32H753 with external SDRAM for decoded pictures and display buffers, and a touch display driven by the MCU's LCD controller.

| Subsystem | Schematic design |
| --- | --- |
| Microcontroller | STM32H753IITx, Arm Cortex-M7, with an STDC14 debug connector |
| Working memory | 16 MiB ISSI IS45S32400J SDR SDRAM on a 32-bit FMC bus |
| Display | Newhaven NHD-4.0-480480AF-ASXP-CTP, a 4-inch 480 × 480 capacitive-touch LCD with parallel RGB driven by LTDC |
| Nonvolatile memory | 32 MiB Winbond W25R256JVEIQ Quad-SPI NOR flash and FM24CL04B I²C FRAM |
| Audio | MAX98357A digital-input Class-D speaker amplifier |
| Sensors | LSM6DSV80X IMU, MMC5983MA magnetometer, and BME280 temperature, humidity, and pressure sensor |

## Decoder roadmap

1. **Bring up the video hardware.** Verify SDRAM reads and writes, then display a test pattern from an SDRAM framebuffer through LTDC.
2. **Decode a first frame.** Start with a small Annex B H.264 elementary stream. Parse NAL units and parameter sets, reconstruct an intra-coded picture from a controlled test stream, and compare the decoded pixels with a reference decoder.
3. **Play a short clip.** Add P-slice decoding, motion compensation, and reference picture management. Convert the decoded frames into a display framebuffer and show them on the LCD.
4. **Measure performance on the board.** Track decode time per frame and peak memory use while LTDC scans out the framebuffer. Use those measurements to determine practical resolution and frame-rate targets.

H.265/HEVC is a tentative follow-up. Once H.264 playback can be profiled on the board, the measurements can inform a feasibility study for a limited HEVC decoding experiment.

## Open the project

- **Hardware** — Open the [KiCad project](Hardware/C20W1B1V1.0/KiCad/C20W1B1V1.0.kicad_pro) to browse the [schematic](Hardware/C20W1B1V1.0/KiCad/C20W1B1V1.0.kicad_sch) and [PCB layout](Hardware/C20W1B1V1.0/KiCad/C20W1B1V1.0.kicad_pcb).
- **Firmware** — Import [Software/C20](Software/C20/) as an existing STM32CubeIDE project. The [CubeMX configuration](Software/C20/C20.ioc) defines the MCU and peripheral setup.

## License

The project is released under the [MIT License](LICENSE).

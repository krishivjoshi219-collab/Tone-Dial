# Tone Dial Firmware (Soul King Brook Edition)

Standalone synthesizer, optical theremin, USB-MIDI controller, and AI companion firmware written in CircuitPython for the **ESP32-S3-DevKitC-1 (N16R8)**.

## Hardware Pinout
- **Audio I2S (MAX98357A):**
  - BCLK: `IO4`
  - LRC: `IO5`
  - DIN: `IO6`
- **Microphone I2S (INMP441):**
  - SCK: `IO1`
  - WS: `IO2`
  - SD: `IO3`
- **I2C Bus (VL53L0X Time-of-Flight):**
  - SDA: `IO8`
  - SCL: `IO12`
- **SPI Display (1.28" GC9A01 240x240 Round LCD):**
  - SCLK: `IO14`
  - MOSI: `IO13`
  - DC: `IO15`
  - CS: `IO16`
  - RST: `IO42`
- **Controls:**
  - 60mm Slide Potentiometer: `IO7` (ADC1_CH6)
  - Rotary Encoder A / B: `IO9`, `IO10`
  - Rotary Encoder Button: `IO11` (Brook AI trigger)
  - 4 Mechanical Keypad Keys: `IO17`, `IO18`, `IO21`, `IO47`

## Required CircuitPython Libraries (in `/lib` on `CIRCUITPY`)
- `adafruit_midi`
- `adafruit_vl53l0x`
- `adafruit_display_text`
- `adafruit_requests`
- `gc9a01`

## Files
- `code.py`: Main non-blocking firmware
- `brook.bmp`: 96x96 24-bit Brook character avatar for GC9A01 LCD
- `brook.png`: Preview image

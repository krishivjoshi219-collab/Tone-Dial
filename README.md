# Tone Dial (Soul King Brook Edition) 💀🎸

A standalone hardware synthesizer, optical theremin, USB-MIDI controller, and AI companion built on the **ESP32-S3 (N16R8)**.

Developed for **Hack Club Half-Life (Week 3: Make Some Noise)**.

---

## 📸 Highlights & Features
- **Sound Engine (`synthio` + `audiomixer`):** Real-time sine-wave synthesizer driven by 4 mechanical keys (Major 7th Chord: C4, E4, G4, B4) through an onboard MAX98357A I2S amplifier and speaker.
- **Optical Theremin (VL53L0X Laser ToF):** Real-time non-contact pitch bending up to +1 octave with hand gestures.
- **USB-MIDI Controller:** Sends MIDI Note On/Off, Pitch Bend, and Control Change (CC 74 filter/cutoff) over USB.
- **Visual Display (GC9A01 1.28" 240x240 Round LCD):** Custom Soul King Brook avatar, real-time Soul Meter (Tamagotchi health), and dynamic status HUD.
- **Soul King Brook AI Companion:** Integrated with Groq Cloud (Llama 3.1 8B Instant) for interactive musical skull jokes and banter triggered by the rotary encoder switch.
- **Tamagotchi Meltdown Mode:** Drops 1% soul every 3 minutes. At 0%, triggers a continuous alarm tone until CPR is performed by pressing Key 1 + Key 4 simultaneously!

---

## 📁 Repository Structure
```
├── firmware/
│   ├── code.py           # CircuitPython 8.x / 9.x main non-blocking firmware
│   ├── brook.bmp         # 24-bit GC9A01 LCD character graphic
│   ├── brook.png         # Brook avatar preview
│   └── README.md         # Firmware flashing & library setup guide
├── Tone Dial/
│   ├── Tone Dial.kicad_pcb # Full 2-layer PCB layout
│   ├── Tone Dial.kicad_sch # Schematic
│   ├── Tone Dial.kicad_pro # KiCad project configuration
│   └── Tone Dial.step     # 3D PCB STEP export
├── 3D CAD & Enclosures/
│   ├── Base_Tray.stl     # Hollow base tray with PCB mounting posts & USB-C port
│   ├── Top_Faceplate.stl # Domed top faceplate with speaker grille & key bezels
│   ├── Tone_Dial_Knob.stl# Knurled rotary knob with EC11 D-shaft bore
│   ├── Tone_Dial_Complete_Enclosure.stl # Full assembled enclosure model
│   └── Tone_Dial_Complete.dxf           # Laser/CNC/CAD vector profiles
├── Gerbers/
│   └── Tone Dial.zip     # Ready-to-order PCB production gerbers
└── README.md
```

---

## 🛠️ Hardware Specifications
- **MCU:** ESP32-S3-DevKitC-1 (N16R8 - 16MB Flash, 8MB Octal PSRAM)
- **Audio DAC / Amp:** MAX98357A I2S Class-D mono amplifier
- **Microphone:** INMP441 I2S MEMS microphone
- **Distance Sensor:** VL53L0X Time-of-Flight laser rangefinder (I2C)
- **Display:** GC9A01 1.28" 240x240 SPI round TFT LCD
- **Controls:** 4x mechanical keyswitches, 1x EC11 rotary encoder with push button, 1x 60mm slide potentiometer

---

## 🚀 Getting Started with Firmware
1. Flash **CircuitPython 9.x** (or 8.x) onto the ESP32-S3.
2. Copy the contents of `firmware/` (`code.py` and `brook.bmp`) to the root of `CIRCUITPY`.
3. Ensure the required libraries are installed into `/lib`:
   - `adafruit_midi`
   - `adafruit_vl53l0x`
   - `adafruit_display_text`
   - `adafruit_requests`
   - `gc9a01`
4. Power up and enjoy!

# 💀 How to Flash the Tone Dial Firmware (Without Crying)

yo if you got the ESP32-S3-DevKitC-1 (N16R8) and you want Brook to come to life on your desk heres litterly all you gotta do:

---

## ⚡ The Quick Step-by-Step

1. **Plug in your ESP32-S3** with a proper USB-C data cable (dont use a dumb charging-only cable lol).
2. **Flash CircuitPython 9.x** (or 8.x) onto it.
3. Open the `CIRCUITPY` drive that pops up on your computer.
4. Drag and drop `code.py` and `brook.bmp` right into the main root of `CIRCUITPY`.
5. Make sure you have these libraries in your `/lib` folder on `CIRCUITPY`:
   - `adafruit_midi`
   - `adafruit_vl53l0x`
   - `adafruit_display_text`
   - `adafruit_requests`
   - `gc9a01`
6. (Optional for AI) If you want Brook to talk back to you with skull jokes, add your WiFi and Groq API key into `settings.toml`:
   ```toml
   WIFI_SSID = "your_wifi_name"
   WIFI_PASSWORD = "your_wifi_password"
   GROQ_API_KEY = "gsk_your_groq_api_key_here"
   ```
7. Reset the board and ENJOY THE CHORDS !!!!!!!

---

## 📌 Hardware Pin Map (Just In Case)
- **I2S Audio Amp (MAX98357A):** BCLK = `IO4`, LRC = `IO5`, DIN = `IO6`
- **I2S Mic (INMP441):** SCK = `IO1`, WS = `IO2`, SD = `IO3`
- **I2C Laser ToF (VL53L0X):** SDA = `IO8`, SCL = `IO12`
- **SPI Round LCD (GC9A01 240x240):** SCLK = `IO14`, MOSI = `IO13`, DC = `IO15`, CS = `IO16`, RST = `IO42`
- **Slide Fader:** `IO7` (ADC1)
- **Rotary Encoder:** A = `IO9`, B = `IO10`, Button = `IO11` (triggers Brook AI!)
- **Keypad Switches:** `IO17`, `IO18`, `IO21`, `IO47`

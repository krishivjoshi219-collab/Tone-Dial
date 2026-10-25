"""
Tone Dial (Brook Edition) - Standalone Synthesizer, Optical Theremin & AI Companion
Developed for Hack Club Half-Life (Week 3: Make Some Noise)
Target MCU: ESP32-S3-DevKitC-1 (N16R8) - CircuitPython 8.x / 9.x
"""

import os
import time
import ssl
import board
import digitalio
import analogio
import keypad
import rotaryio
import busio
import audiobusio
import audiomixer
import synthio
import ulab.numpy as np
import usb_midi
import adafruit_midi
from adafruit_midi.note_on import NoteOn
from adafruit_midi.note_off import NoteOff
from adafruit_midi.pitch_bend import PitchBend
from adafruit_midi.control_change import ControlChange
import adafruit_vl53l0x
import displayio
import terminalio
from adafruit_display_text import label
import gc9a01
import wifi
import socketpool
import adafruit_requests

# FourWire import compatibility across CP 8.x and 9.x
try:
    from fourwire import FourWire
except ImportError:
    from displayio import FourWire

# ==========================================
# 1. HARDWARE PIN DEFINITIONS
# ==========================================
PIN_I2S_BCLK = board.IO4
PIN_I2S_LRC  = board.IO5
PIN_I2S_DIN  = board.IO6

PIN_MIC_SCK  = board.IO1
PIN_MIC_WS   = board.IO2
PIN_MIC_SD   = board.IO3

PIN_I2C_SDA  = board.IO8
PIN_I2C_SCL  = board.IO12

PIN_SPI_SCLK = board.IO14
PIN_SPI_MOSI = board.IO13
PIN_LCD_DC   = board.IO15
PIN_LCD_CS   = board.IO16
PIN_LCD_RST  = board.IO42

PIN_FADER_ADC= board.IO7
PIN_ENC_A    = board.IO9
PIN_ENC_B    = board.IO10
PIN_ENC_SW   = board.IO11

KEY_PINS     = (board.IO17, board.IO18, board.IO21, board.IO47)

# ==========================================
# 2. DISPLAY INITIALIZATION (1.28" GC9A01 240x240)
# ==========================================
displayio.release_displays()
spi_bus = busio.SPI(clock=PIN_SPI_SCLK, MOSI=PIN_SPI_MOSI)
display_bus = FourWire(
    spi_bus, command=PIN_LCD_DC, chip_select=PIN_LCD_CS, reset=PIN_LCD_RST, baudrate=40000000
)
display = gc9a01.GC9A01(display_bus, width=240, height=240)

splash = displayio.Group()
display.root_group = splash

# Brook Character Graphic (Centered on Round Display)
try:
    brook_bmp = displayio.OnDiskBitmap("/brook.bmp")
    brook_grid = displayio.TileGrid(brook_bmp, pixel_shader=brook_bmp.pixel_shader, x=72, y=60)
    splash.append(brook_grid)
except (OSError, ValueError) as err:
    print("Brook bitmap not loaded:", err)

# UI Status Labels
status_label = label.Label(terminalio.FONT, text="TONE DIAL: ONLINE", color=0x00FFCC, x=45, y=30)
soul_label = label.Label(terminalio.FONT, text="SOUL: 100%", color=0xFFFF00, x=80, y=180)
theremin_label = label.Label(terminalio.FONT, text="TOF: --- mm", color=0xFFFFFF, x=70, y=205)
splash.append(status_label)
splash.append(soul_label)
splash.append(theremin_label)

# ==========================================
# 3. AI COMPANION (GROQ API / BROOK)
# ==========================================
API_KEY = os.getenv("GROQ_API_KEY", "")
NET_SSID = os.getenv("WIFI_SSID", "")
NET_AUTH = os.getenv("WIFI_PASSWORD", "")

BROOK_PROMPT = (
    "You are Soul King Brook from One Piece. Respond in character with skull jokes, "
    "dramatic musical flair, and 'Yo-ho-ho-ho!'. Keep responses under 2 sentences."
)

class BrookAI:
    def __init__(self, ssid, auth_key):
        self.connected = False
        try:
            wifi.radio.connect(ssid, auth_key)
            pool = socketpool.SocketPool(wifi.radio)
            ssl_context = ssl.create_default_context()
            self.requests = adafruit_requests.Session(pool, ssl_context)
            self.connected = True
            print("WiFi Connected for Brook AI!")
        except (RuntimeError, OSError) as err:
            print("WiFi Connection Failed:", err)

    def chat(self, user_text="Play some music for me!"):
        if not self.connected:
            return "NO WIFI! Yo-ho-ho!"
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "llama-3.1-8b-instant",
            "messages": [
                {"role": "system", "content": BROOK_PROMPT},
                {"role": "user", "content": user_text}
            ],
            "max_tokens": 80
        }
        try:
            res = self.requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                json=payload,
                headers=headers
            )
            return res.json()["choices"][0]["message"]["content"]
        except (RuntimeError, OSError, ValueError) as err:
            return f"ERR: {err}"

brook = None
if NET_SSID:
    brook = BrookAI(NET_SSID, NET_AUTH)

# ==========================================
# 4. CONTROLS INITIALIZATION
# ==========================================
keys = keypad.Keys(KEY_PINS, value_when_pressed=False, pull=True)
currently_pressed_keys = set()

# Rotary Encoder & Push Switch
encoder = rotaryio.IncrementalEncoder(PIN_ENC_A, PIN_ENC_B)
enc_btn = digitalio.DigitalInOut(PIN_ENC_SW)
enc_btn.direction = digitalio.Direction.INPUT
enc_btn.pull = digitalio.Pull.UP
last_enc_btn_state = enc_btn.value

# 60mm Slide Potentiometer (ADC1)
fader = analogio.AnalogIn(PIN_FADER_ADC)

# USB-MIDI Setup
midi = adafruit_midi.MIDI(midi_out=usb_midi.ports[1], out_channel=0)
MIDI_NOTES = [60, 64, 67, 71]  # C4, E4, G4, B4 (Major 7th Chord)

# Optical Theremin (VL53L0X Laser Sensor)
i2c = busio.I2C(scl=PIN_I2C_SCL, sda=PIN_I2C_SDA)
try:
    tof = adafruit_vl53l0x.VL53L0X(i2c)
    has_tof = True
except (RuntimeError, OSError, ValueError) as err:
    print("VL53L0X not detected:", err)
    has_tof = False

# ==========================================
# 5. AUDIO & SYNTH ENGINE (MAX98357A I2S)
# ==========================================
i2s_audio = audiobusio.I2SOut(bit_clock=PIN_I2S_BCLK, word_select=PIN_I2S_LRC, data=PIN_I2S_DIN)
mixer = audiomixer.Mixer(voice_count=2, sample_rate=22050, channel_count=1, bits_per_sample=16, samples_signed=True)
i2s_audio.play(mixer)

synth = synthio.Synthesizer(sample_rate=22050, channel_count=1)
mixer.voice[0].play(synth)
mixer.voice[0].level = 0.8

SAMPLE_SIZE = 512
raw_sine = np.sin(np.linspace(0, 2 * np.pi, num=SAMPLE_SIZE, endpoint=False))
wave_sine = np.array(raw_sine * 32767, dtype=np.int16)

active_synth_notes = {}

# ==========================================
# 6. STATE VARIABLES & TIMERS
# ==========================================
soul_meter = 100
last_interaction = time.monotonic()
last_soul_tick = time.monotonic()
last_tof_time = time.monotonic()
is_meltdown = False
last_enc_pos = encoder.position
last_fader_val = 0

print("Tone Dial initialized. Starting event loop...")

# ==========================================
# 7. NON-BLOCKING EVENT LOOP
# ==========================================
while True:
    now = time.monotonic()

    # --- SOUL METER & MELTDOWN STATE ---
    if not is_meltdown and (now - last_soul_tick > 180):
        last_soul_tick = now
        soul_meter = max(0, soul_meter - 1)
        soul_label.text = f"SOUL: {soul_meter}%"
        if soul_meter == 0:
            is_meltdown = True
            status_label.text = "HEART ATTACK!"
            status_label.color = 0xFF0000

    if is_meltdown:
        emergency_pitch = 880 if int(now * 4) % 2 == 0 else 440
        if 999 not in active_synth_notes:
            n = synthio.Note(frequency=emergency_pitch, waveform=wave_sine)
            synth.press(n)
            active_synth_notes[999] = n
        else:
            active_synth_notes[999].frequency = emergency_pitch

    # --- 4-KEY SCANNING & CPR REVIVAL ---
    event = keys.events.get()
    if event:
        last_interaction = now
        key_idx = event.key_number
        midi_note = MIDI_NOTES[key_idx]

        if event.pressed:
            currently_pressed_keys.add(key_idx)

            if is_meltdown and (0 in currently_pressed_keys and 3 in currently_pressed_keys):
                is_meltdown = False
                soul_meter = 100
                if 999 in active_synth_notes:
                    synth.release(active_synth_notes[999])
                    del active_synth_notes[999]
                status_label.text = "YO-HO-HO-HO!"
                status_label.color = 0x00FFCC
                soul_label.text = "SOUL: 100%"
                continue

            freq = 440.0 * (2.0 ** ((midi_note - 69) / 12.0))
            synth_note = synthio.Note(frequency=freq, waveform=wave_sine)
            synth.press(synth_note)
            active_synth_notes[key_idx] = synth_note
            midi.send(NoteOn(midi_note, 100))
            status_label.text = f"NOTE: {midi_note}"

        elif event.released:
            currently_pressed_keys.discard(key_idx)
            if key_idx in active_synth_notes:
                synth.release(active_synth_notes[key_idx])
                del active_synth_notes[key_idx]
            midi.send(NoteOff(midi_note, 0))

    # --- ENCODER BUTTON (BROOK AI TRIGGER) ---
    enc_btn_val = enc_btn.value
    if enc_btn_val != last_enc_btn_state:
        last_enc_btn_state = enc_btn_val
        if not enc_btn_val and brook:
            status_label.text = "THINKING..."
            status_label.color = 0xFF88FF
            ai_reply = brook.chat("Tell me a musical skull joke!")
            status_label.text = ai_reply[:18]

    # --- ROTARY ENCODER (VOLUME CONTROL) ---
    enc_pos = encoder.position
    if enc_pos != last_enc_pos:
        diff = enc_pos - last_enc_pos
        last_enc_pos = enc_pos
        last_interaction = now
        new_vol = max(0.0, min(1.0, mixer.voice[0].level + (diff * 0.05)))
        mixer.voice[0].level = new_vol
        status_label.text = f"VOL: {int(new_vol * 100)}%"

    # --- SLIDE FADER (FILTER / RESONANCE) ---
    fader_raw = fader.value
    if abs(fader_raw - last_fader_val) > 800:
        last_fader_val = fader_raw
        last_interaction = now
        midi_cc = int((fader_raw / 65535.0) * 127)
        midi.send(ControlChange(74, midi_cc))

    # --- OPTICAL THEREMIN (VL53L0X LASER) ---
    if has_tof and (now - last_tof_time > 0.1):
        last_tof_time = now
        try:
            dist = tof.range
            if 30 <= dist <= 400:
                theremin_label.text = f"TOF: {dist} mm"
                pitch_mult = 1.0 + ((dist - 30) / 370.0)
                for k_idx, s_note in active_synth_notes.items():
                    if k_idx != 999:
                        base_freq = 440.0 * (2.0 ** ((MIDI_NOTES[k_idx] - 69) / 12.0))
                        s_note.frequency = base_freq * pitch_mult
                bend_val = 8192 + int(((dist - 30) / 370.0) * 8191)
                midi.send(PitchBend(bend_val))
            else:
                theremin_label.text = "TOF: OUT OF RANGE"
                midi.send(PitchBend(8192))
        except (RuntimeError, OSError) as err:
            print("TOF read error:", err)

    time.sleep(0.005)

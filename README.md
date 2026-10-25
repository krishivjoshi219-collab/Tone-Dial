# 💀🐚 TONE DIAL (SOUL KING BROOK EDITION) 🎻⚡
> *"YO-HO-HO-HO! I HAVE NO EARS BUT THIS SYNTH SOUNDS SO FIRE BROOO!!!"*

YO WHAT IS UP HACK CLUB REVIWRES AND RAMDOM GITHUB PEOPLE !!!!!!!!! 👋
so basically this is my project for **Half-Life Week 3 (Make Some Noise / Music week)** and its called **TONE DIAL** (yes from skypiea in one piece bcuz brook is litterly the GOAT no debate 😤). 

and like its NOT just a dumb boring speaker or some basic 3 button macropad that just beep boops lol... its a **LITTERAL STANDALONE SYNTHESIZER + OPTICAL THEREMIN + USB MIDI CONTROLLER + AI DESK PET COMPANION THINGY** THAT ACTUALLY LIVES ON MY DESK !!!!!!! (bruh it took so long to finilaze the idea my brain was melting)

---

## 🤯 WHAT DOES THIS EVEN DO LIKE ACTUALLY?!?!?!

* 🎹 **CHORD SYNTH THAT DOESNT SOUND TRASH:** 4 mech switches wired to play a fire C-maj7 chord (C4, E4, G4, B4) runing on circuitpython `synthio` + `audiomixer` so it actually sounds like real music and not a microwave buzzer lmao
* 📡 **OPTICAL THEREMIN (PEW PEW LASER THINGY):** i put a literal VL53L0X laser sensor on it so i can just wave my hand in the air like a madman to bend pitch and filter cutoff without even touching anything like a crazy sci-fi theremin !!!!!!!
* 💀 **BROOK AI COMPANION (GROQ CLOUD GO BRRR):** if you click the rotary encoder knob it talks to Groq Llama 3.1 8B Instant over wifi to tell you unhinged skull jokes (*"Can I see your panties? Wait I don't have eyes! Yo-ho-ho-ho!"*)
* 🫀 **TAMAGOTCHI HEART ATTACK MELTDOWN:** brook has a "soul meter" on the round LCD. every 3 mins it drops 1%. if it hits 0%, HE GETS A LITTERAL HEART ATTACK and a super loud screech alarm blasts until you do **CPR by spamming Key 1 + Key 4 together** to revive him lol 😭
* 🎛️ **SLIDER & DIAL:** a 60mm slide potentiometer for sweeping the filter brightness + EC11 dial for volume !!
* 📺 **ROUND SCREEN:** 1.28 inch round GC9A01 LCD showing brooks animated skull face, his soul level, and the theremin laser distance in real time.

---

## 💻 THE HARDWARE (HOW I ALMOST BLEW UP MY PC LOL)

fun fact: i had to disgn this ENTIRE 3D enclosure on a litteral ancient 2012 intel 2nd gen Core i5 tower with NO gpu and onshape litterly froze my pc like 50 times at 3 AM and crashed my browser and i wanted to cry but WE FINIALLY MADE IT OUT ALIVE !!!!!!!! (i spent 40 mins wondering why my extrude was broken until i relized i had to click new instead of add lmaooo)

* **Brain:** ESP32-S3-DevKitC-1 (N16R8) with dual core 240mhz + 8MB octal psram (core 0 does the wifi + groq ai and core 1 does audio so the synth never stutters or lags)
* **Audio Out:** MAX98357A I2S 3W class D amp going into a 40mm speaker inside a custom acoustic sealed chamber
* **Display:** 1.28" circular SPI TFT (GC9A01) 240x240
* **Sensor:** VL53L0X I2C laser distance sensor
* **Keys:** 4x mechanical keyswitches + 1x 60mm slide fader + EC11 encoder knob
* **Enclosure:** custom 12 degree tilted desktop wedge tray with built-in pcb holder clips and a nice clean USB C rectangle hole so you can plug it in without snapping the port !!

---

## 📂 WHAT IS WHERE IN THIS REPO (SO YOU DONT GET LOST)

```
├── firmware/
│   ├── code.py         <-- the big brain non-blocking circuitpython code!
│   ├── brook.bmp       <-- 96x96 pixel art of brook with his afro & tiny hat
│   ├── brook.png       <-- preview pic so you can see how cool he looks
│   └── README.md       <-- how to flash it without crying
├── Tone Dial/
│   ├── Tone Dial.kicad_pcb  <-- full 2 layer pcb layout that took forever
│   ├── Tone Dial.kicad_sch  <-- the massive schemetic
│   ├── Tone Dial.kicad_pro  <-- kicad project file
│   └── Tone Dial.step       <-- 3d step model of the pcb
├── Base_Tray.stl            <-- 3d printable bottom wedge with usb-c hole & pcb posts
├── Top_Faceplate.stl        <-- top plate with speaker grill, dial ring & button cutouts
├── Tone_Dial_Knob.stl       <-- knurled volume knob for the EC11 shaft
├── Tone_Dial_Complete_Enclosure.stl <-- full assembled 3d model
├── Tone Dial.zip            <-- ready to order gerbers for jlcpcb
├── BOM.csv                  <-- bill of materials (kept under budget lets gooo)
└── JOURNAL.md               <-- my devlog for hack club reviewers!
```

---

## 🚀 HOW TO RUN THE FIRMWARE

1. plug in the esp32-s3 with a usb c cable
2. drop **CircuitPython 9.x** onto the board
3. open the `CIRCUITPY` drive on your pc
4. copy `code.py` and `brook.bmp` from `firmware/` right into the root of `CIRCUITPY`
5. put these libraries inside the `lib/` folder:
   - `adafruit_midi`
   - `adafruit_vl53l0x`
   - `adafruit_display_text`
   - `adafruit_requests`
   - `gc9a01`
6. (optional) add your wifi ssid and groq api key in `settings.toml` so brook can talk back to you!
7. JAM OUT AND DONT LET BROOK DIE OF A HEART ATTACK !!!!!!!!

---

### BIG SHOUTOUT TO HACK CLUB HALF LIFE REVIWRES PLEASE APPROVE MY GRANT SO I CAN SOLDER THIS BEAUTY IRL TYSM <33333333333

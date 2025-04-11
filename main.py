import pigpio
import threading
import time

DIR = 20
STEP = 21
DIR2 = 13
STEP2 = 19
BUTTON_PIN = 17

pi = pigpio.pi()
pi.set_mode(DIR, pigpio.OUTPUT)
pi.set_mode(STEP, pigpio.OUTPUT)
pi.set_mode(DIR2, pigpio.OUTPUT)
pi.set_mode(STEP2, pigpio.OUTPUT)
pi.set_mode(BUTTON_PIN, pigpio.INPUT)
pi.set_pull_up_down(BUTTON_PIN, pigpio.PUD_UP)

# PWM başlangıç
frequency = 500
pi.set_PWM_dutycycle(STEP, 128)
pi.set_PWM_frequency(STEP, frequency)
pi.set_PWM_dutycycle(STEP2, 128)
pi.set_PWM_frequency(STEP2, frequency)

running = True
direction = 1

def komut_dinleyici():
    global frequency, direction, running
    while True:
        cmd = input("Komut (r/l/u/d/q): ").strip().lower()
        if cmd == "r":
            direction = 1
            pi.write(DIR, direction)
            pi.write(DIR2, direction)
            print("→ Sağa dönüyor", flush=True)
        elif cmd == "l":
            direction = 0
            pi.write(DIR, direction)
            pi.write(DIR2, direction)
            print("← Sola dönüyor", flush=True)
        elif cmd == "u":
            frequency = min(3000, frequency + 100)
            pi.set_PWM_frequency(STEP, frequency)
            pi.set_PWM_frequency(STEP2, frequency)
            print(f"⚡ Hız artırıldı: {frequency} Hz", flush=True)
        elif cmd == "d":
            frequency = max(100, frequency - 100)
            pi.set_PWM_frequency(STEP, frequency)
            pi.set_PWM_frequency(STEP2, frequency)
            print(f"🐢 Hız azaltıldı: {frequency} Hz", flush=True)
        elif cmd == "q":
            running = False
            print("Çıkılıyor...", flush=True)
            break
        else:
            print("Geçersiz komut.", flush=True)

# Komut dinleyici thread başlat
threading.Thread(target=komut_dinleyici, daemon=True).start()

try:
    while running:
        button_state = pi.read(BUTTON_PIN)
        if button_state == 0:  # Butona basılıyorsa
            pi.set_PWM_dutycycle(STEP, 0)
            pi.set_PWM_dutycycle(STEP2, 0)
            print("🛑 Motor durdu! Butona basıldı.", flush=True)
        else:
            pi.set_PWM_dutycycle(STEP, 128)
            pi.set_PWM_dutycycle(STEP2, 128)
        time.sleep(0.1)

except KeyboardInterrupt:
    pass

finally:
    pi.set_PWM_dutycycle(STEP, 0)
    pi.set_PWM_dutycycle(STEP2, 0)
    pi.stop()

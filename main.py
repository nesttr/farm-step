import pigpio
from time import sleep

DIR = 20    # Yön pini
STEP = 21   # Step pini
DIR2 = 13 # Yön pini 2
STEP2 = 19 # Step pini 2

# pigpio bağlantısı
pi = pigpio.pi()
pi.set_mode(DIR, pigpio.OUTPUT)
pi.set_mode(STEP, pigpio.OUTPUT)

# Başlangıç değerleri
direction = 1
frequency = 500  # Hz
step_count = 0

# PWM duty cycle %50
pi.set_PWM_dutycycle(STEP, 128)
pi.set_PWM_frequency(STEP, frequency)

pi.set_PWM_dutycycle(STEP2, 128)
pi.set_PWM_frequency(STEP2, frequency)

print("""
🔧 Komutlar:
r → sağa dön
l → sola dön
u → hızı artır
d → hızı azalt
q → çık
""")

try:
    while True:
        cmd = input("Komut (r/l/u/d/q): ").strip().lower()

        if cmd == "r":
            direction = 1
            pi.write(DIR, direction)
            pi.write(DIR2, direction)
            print("→ Sağa dönüyor")

        elif cmd == "l":
            direction = 0
            pi.write(DIR, direction)
            pi.write(DIR2, direction)
            print("← Sola dönüyor")

        elif cmd == "u":
            frequency += 100
            if frequency > 3000:
                frequency = 3000
            pi.set_PWM_frequency(STEP, frequency)
            pi.set_PWM_frequency(STEP2, frequency)
            print(f"⚡ Hız artırıldı: {frequency} Hz")

        elif cmd == "d":
            frequency -= 100
            if frequency < 100:
                frequency = 100
            pi.set_PWM_frequency(STEP, frequency)
            pi.set_PWM_frequency(STEP2, frequency)
            print(f"🐢 Hız azaltıldı: {frequency} Hz")

        elif cmd == "q":
            print("Çıkılıyor...")
            break

        else:
            print("Geçersiz komut.")

        step_count += 1
        print(f"Yön: {'Sağ' if direction else 'Sol'} | Frekans: {frequency} Hz | Toplam Adım: {step_count}")

except KeyboardInterrupt:
    print("Durduruluyor...")

finally:
    pi.set_PWM_dutycycle(STEP, 0)
    pi.set_PWM_dutycycle(STEP2, 0)
    pi.stop()

import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import speech_recognition as sr
from googletrans import Translator

duration = 5  # kayıt saniyesi
sample_rate = 44100

translator = Translator()

# Kullanıcıdan hedef dili al
print("===================================")
print("     KONUŞMA ÇEVİRİ PROGRAMI")
print("===================================")

target_language = input("Hangi dile çevirmek istiyorsunuz? (Örn: de, en, fr): ")

print()
print("Şimdi konuşun...")

recording = sd.rec(
    int(duration * sample_rate),
    samplerate=sample_rate,
    channels=1,
    dtype="int16"
)

sd.wait()

wav.write("output.wav", sample_rate, recording)

print("Kayıt tamamlandı!")
print("Konuşma tanınıyor...")

recognizer = sr.Recognizer()

with sr.AudioFile("output.wav") as source:
    audio = recognizer.record(source)

try:
    # Türkçe konuşmayı metne çevir
    text = recognizer.recognize_google(audio, language="tr")

    print()
    print("Şunu söylediniz:", text)

    # Kullanıcının seçtiği dile çevir
    translated = translator.translate(
        text,
        dest=target_language
    )

    print("Çeviri:", translated.text)

except sr.UnknownValueError:
    print("Konuşma tanınamadı.")

except sr.RequestError as e:
    print(f"Hizmet hatası: {e}")

except Exception as e:
    print(f"Çeviri hatası: {e}")

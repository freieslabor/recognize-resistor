#!/usr/bin/python
# -*- coding: utf-8 -*-

import speech_recognition as sr
import os


def color2resistance(colors):
        ext = {
            0: "",
            1: "k",
            2: "M"
        }

        color2value = {
            "silber": -2,
            "gold": -1,
            "schwarz": 0,
            "braun": 1,
            "rot": 2,
            "orange": 3,
            "gelb": 4,
            u"gr\xfcn": 5,
            "blau": 6,
            "lila": 7,
            "grau": 8,
            u"wei\xdf": 9
        }

        r = 0
        for color in colors:
            r = r * 10 + color2value[color]

        r = r * 10 ** color2value[colors[-1]]

        exp = 0
        while r >= 1000:
                r /= 1000.0
                exp += 1

        while r < 1:
                r *= 1000
                exp -= 3

        return "%.1f%s" % (r, ext[exp])


r = sr.Recognizer()
m = sr.Microphone()

with m as source:
    print("Setze Stillegrenzwert (nicht sprechen!)..")
    r.adjust_for_ambient_noise(source)
    r.dynamic_energy_threshold = False
    print("Stillegrenzwert auf %s gesetzt." % r.energy_threshold)
    while True:
        try:
            print("Bitte 4 Farben ablesen.")
            audio = r.listen(source, timeout=3)
            print("Danke. Erkennung läuft..")
            # recognize speech using Google Speech Recognition
            spoken = r.recognize_google(audio, language="de-DE")
            # ignore everything but last 4 words
            input = spoken.split()[:4]
            resistance = color2resistance(input)

            print("%s: %s Ohm" % (" ".join(input), resistance))
            os.system("espeak -s150 -vde \"%s ist ein %s Ohm Widerstand.\""
                      % (" ".join(input).encode("utf-8"), resistance))

        except sr.UnknownValueError:
            print("Satz war nicht verständlich.")
        except KeyError as e:
            print("Konnte %s nicht erkennen." % e.message)
        except sr.WaitTimeoutError:
            print("Timeout erreicht.")

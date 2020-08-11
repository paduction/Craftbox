#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Paduction.com : Craftbox - 05/08/17

import RPi.GPIO as GPIO  # bibliothèque pour utiliser les GPIO
import time              # bibliothèque pour gestion du temps
from mcstatus import MinecraftServer  # bibliothéque de status du serveur
import socket

# If you know the host and port, you may skip this and use MinecraftServer("example.org", 1234)
server = MinecraftServer.lookup("localhost:25565")


def is_connected():
    try:
        # see if we can resolve the host name -- tells us if there is a DNS listening
        host = socket.gethostbyname("www.google.com")
        # connect to the host -- tells us if the host is actually reachable
        socket.create_connection((host, 80), 2)
        print("WIFI fonctionnel")
        GPIO.output(21, GPIO.HIGH)  # allume la LED jaune
        return True
    except:
        GPIO.output(21, GPIO.LOW)
        print("Le wifi ne marche pas !")
        pass
    return False


def blink(players):
    i = 0
    print("LED joueurs")
    while i < 5:
        if players > 0:
            GPIO.output(25, GPIO.HIGH)
            if players > 1:
                GPIO.output(24, GPIO.HIGH)
                if players > 2:
                    GPIO.output(23, GPIO.HIGH)
                    if players > 3:
                        GPIO.output(18, GPIO.HIGH)
        time.sleep(0.2)
        GPIO.output(18, GPIO.LOW)
        GPIO.output(23, GPIO.LOW)
        GPIO.output(24, GPIO.LOW)
        GPIO.output(25, GPIO.LOW)
        time.sleep(0.2)
        i += 1


def process():
    print("Process DEF")

    # boucle répétée jusqu'à l'interruption du programme
    while True:
        # 'status' est supporté par toutes les versions également ou supéreieur à 1.7
        status = server.status()
        # Affiche les informations sur le nombre de joueurs et le nombre de réponse
        print("Le serveur a {0} joueur(s) et répond en {1} ms".format(
            status.players.online, status.latency))
        if status.players.online > 0:
            # Si il y a un ou plusieurs joueurs alors on allume la/les leds
            blink(status.players.online)
        else:
            # Si il n'y a pas de joueur alors on eteint la/les LEDs
            GPIO.output(18, GPIO.LOW)  # sortie au niveau logique bas (0 V)
            GPIO.output(23, GPIO.LOW)
            GPIO.output(24, GPIO.LOW)
            GPIO.output(25, GPIO.LOW)
            time.sleep(3)  # on ne change rien pendant 1 seconde


def setup():
    print("Setup")
    GPIO.setmode(GPIO.BCM)  # Mode de numérotation des pins du GPIO
    GPIO.setup(18, GPIO.OUT)
    GPIO.setup(21, GPIO.OUT)
    GPIO.setup(23, GPIO.OUT)
    GPIO.setup(24, GPIO.OUT)
    GPIO.setup(25, GPIO.OUT)
    print("end setup")


def destroy():
    GPIO.output(18, GPIO.LOW)  # eteint la led
    GPIO.output(21, GPIO.LOW)
    GPIO.output(23, GPIO.LOW)
    GPIO.output(24, GPIO.LOW)
    GPIO.output(25, GPIO.LOW)
    GPIO.cleanup()  # Libère les ressources
    print("Fin du programme, on sort proprement")


if __name__ == '__main__':  # Le script demarre
    while True:
        try:
            setup()
            is_connected()
            process()
        except KeyboardInterrupt:  # Quand on clique sur "Ctrl+c" on renvoie sur detroy
            destroy()
            break
        except Exception as err:
            destroy()
            print('Erreur: ', err)
            break
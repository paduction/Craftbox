#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Paduction.com : Craftbox - 05/08/16

import RPi.GPIO as GPIO  # bibliothèque pour utiliser les GPIO
import time              # bibliothèque pour gestion du temps
from mcstatus import MinecraftServer # bibliothéque de status du serveur
import urllib2 # bibliothèque de gestion url
import socket

# If you know the host and port, you may skip this and use MinecraftServer("example.org", 1234)
server = MinecraftServer.lookup("localhost:25565")

def is_connected():
  try:
    # see if we can resolve the host name -- tells us if there is a DNS listening
    host = socket.gethostbyname("www.google.com")
    # connect to the host -- tells us if the host is actually reachable
    s = socket.create_connection((host, 80), 2)
    print("WIFI fonctionnel")
    GPIO.output(21, GPIO.HIGH)
    print("Allumage des LED")
    return True
  except:
    print("Le wifi ne marche pas !")
    pass 
  return False

def internet_on():
    try:
      print("Test du WIFI")
      urllib2.urlopen('http://google.com', timeout=1)
	  print("WIFI fonctionnel")
	  GPIO.output(21, GPIO.HIGH)
      return True
    except urllib2.URLError as err:
	  print("Le wifi ne marche pas !",  err)
	  GPIO.output(21, GPIO.LOW)
    return False

def blink(players):
  i = 0
  print("LED joueurs")
  while i < 10:
    if players > 0:
       GPIO.output(25,GPIO.HIGH)
       if players > 1:
          GPIO.output(24,GPIO.HIGH)
          if players > 2:
             GPIO.output(23,GPIO.HIGH)
             if players > 3:
                GPIO.output(18,GPIO.HIGH)
    time.sleep(0.2)
    GPIO.output(18,GPIO.LOW)
    GPIO.output(23,GPIO.LOW)
    GPIO.output(24,GPIO.LOW)
    GPIO.output(25,GPIO.LOW)
    time.sleep(0.2)
    i += 1 

def process():
   print("Process DEF")
   while True:     # boucle répétée jusqu'à l'interruption du programme
     
     status = server.status()
     # Affiche les informations sur le nombre de joueurs et le nombre de réponse
     print("Le serveur a {0} joueur(s) et répond en {1} ms".format(status.players.online, status.latency))
     if status.players.online > 0:
    	 # si il y a un joueur alors on allume la led    
         # GPIO.output(25,GPIO.HIGH)   # sortie au niveau logique haut (3.3 V)
         blink(status.players.online)
         # blink(2)
         # time.sleep(3)               # on ne change rien pendant 1 seconde
     else:
         # Si il n'y a pas de joueur alors on eteint la diode 
    	 # 'status' is supported by all Minecraft servers that are version 1.7 or higher.
    	 GPIO.output(25,GPIO.LOW)    # sortie au niveau logique bas (0 V)
    	 time.sleep(3)               # on ne change rien pendant 1 seconde


def setup():
   print("Setup")
   GPIO.setmode(GPIO.BCM) # Mode de numérotation des pins du GPIO
   GPIO.setup(18, GPIO.OUT)
   GPIO.setup(21, GPIO.OUT)
   GPIO.setup(23, GPIO.OUT)
   GPIO.setup(24, GPIO.OUT)
   GPIO.setup(25, GPIO.OUT)
   print("end setup")
     
def destroy():
   GPIO.output(18, GPIO.LOW) # eteint la led
   GPIO.output(21, GPIO.LOW)
   GPIO.output(23, GPIO.LOW)
   GPIO.output(24, GPIO.LOW)
   GPIO.output(25, GPIO.LOW)
   GPIO.cleanup() # Libère les ressources
   print("Fin du programme, on sort proprement")

if __name__ == '__main__': # Le script demarre
  while True:
   try:
     setup()
     is_connected()
     process()
   except KeyboardInterrupt: # Quand on clique sur "Ctrl+c" on renvoie sur detroy
     destroy()
     break
   except Exception as err:
     destroy()
     print('Erreur: ', err )
     break

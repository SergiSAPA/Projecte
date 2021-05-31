# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT
#!usr/bin/env python

import mysql.connector
import time
import board
import busio
from digitalio import DigitalInOut, Direction
import adafruit_fingerprint

led = DigitalInOut(board.D13)
led.direction = Direction.OUTPUT

#uart = busio.UART(board.TX, board.RX, baudrate=57600)

# If using with a computer such as Linux/RaspberryPi, Mac, Windows with USB/serial converter:
# import serial
# uart = serial.Serial("/dev/ttyUSB0", baudrate=57600, timeout=1)

# If using with Linux/Raspberry Pi and hardware UART:
import serial
uart = serial.Serial("/dev/ttyS0", baudrate=57600, timeout=1)

finger = adafruit_fingerprint.Adafruit_Fingerprint(uart)

##################################################

def get_fingerprint():
    """Get a finger print image, template it, and see if it matches!"""
    print("Posa el dit al lector...")
    while finger.get_image() != adafruit_fingerprint.OK:
        pass
    if finger.image_2_tz(1) != adafruit_fingerprint.OK:
        return False
    if finger.finger_search() != adafruit_fingerprint.OK:
        return False
    return True

# pylint: disable=too-many-statements
def enroll_finger(location):
    """Take a 2 finger images and template it, then store in 'location'"""
    for fingerimg in range(1, 3):
        if fingerimg == 1:
            print("Posa el dit al lector...", end="", flush=True)
        else:
            print("Torna a posar el dit al lector...", end="", flush=True)

        while True:
            i = finger.get_image()
            if i == adafruit_fingerprint.OK:
                print("\nGuardant imatge")
                break
            if i == adafruit_fingerprint.NOFINGER:
                print(".", end="", flush=True)
            elif i == adafruit_fingerprint.IMAGEFAIL:
                print("Error al guardar l'imatge")
                return False
            else:
                print("Hi ha hagut un error")
                return False

        i = finger.image_2_tz(fingerimg)
        if i == adafruit_fingerprint.OK:
            print("Imatge guardada")
        else:
            if i == adafruit_fingerprint.IMAGEMESS:
                print("L'imatge es borrosa")
            elif i == adafruit_fingerprint.FEATUREFAIL:
                print("No s'ha pogut identificar correctament")
            elif i == adafruit_fingerprint.INVALIDIMAGE:
                print("Imatge invalida")
            else:
                print("Hi ha hagut un error")
            return False

        if fingerimg == 1:
            print("Treu el dit")
            time.sleep(1)
            while i != adafruit_fingerprint.NOFINGER:
                i = finger.get_image()

    i = finger.create_model()
    if i == adafruit_fingerprint.OK:
        print("L'empremta s'ha creat correctament!")
    else:
        if i == adafruit_fingerprint.ENROLLMISMATCH:
            print("\nLes empremtes no coincideixen, torna a guardar-les")
        else:
            print("Hi ha hagut un error")
        return False

    i = finger.store_model(location)
    if i == adafruit_fingerprint.OK:
        print("L'empremta s'ha guardat correctament!")
    else:
        if i == adafruit_fingerprint.BADLOCATION:
            print("Error d'emmagatzematge")
        elif i == adafruit_fingerprint.FLASHERR:
            print("Error d'emmagatzematge")
        else:
            print("Hi ha hagut un error")
        return False

    return True

##################################################

def get_num():
    """Use input() to get a valid number from 1 to 127. Retry till success!"""
    i = 0
    while (i > 127) or (i < 1):
        try:
            print("Aquests son els ID que ja estan guardats:", finger.templates)
            print("L'ID ha de coincidir amb l'ID que tingui l'empleat, per veure quin es utilitza l'opcio E")
            i = int(input("Introdueix el numero d'ID que tindra l'empremta, ha de ser un nombre entre el 1-127: "))
        except ValueError:
            pass
    return i

while True:
    print("--------------------------------")
    if finger.read_templates() != adafruit_fingerprint.OK:
        raise RuntimeError("Hi ha hagut un error")
    print("Benvingut!")
    print("A) Desar empremta")
    print("B) Desar empleat")
    print("C) Fitxar")
    print("D) Esborrar empremta")
    print("E) Llista d'empleats")
    print("--------------------------------")
    opcio = input("Selecciona una opcio: ")

    if opcio == "a" or opcio == "A":
        enroll_finger(get_num())
        
    if opcio == "b" or opcio == "B":
        nom = input("Introdueix el nom de l'empleat: ")
        cognom1 = input("Introdueix el primer cognom de l'empleat: ")
        cognom2 = input("Introdueix el segon cognom de l'empleat: ")
        dni = input("Introdueix el DNI de l'empleat: ")
        connexio = mysql.connector.connect(host='ipdelservidor', user='projecte', passwd='P@ssw0rd', db='fixatges')
        cursor = connexio.cursor()
            
        insert = "INSERT INTO treballadors (nom, cognom1, cognom2, dni) VALUES (%s, %s, %s, %s)"
        values = (nom, cognom1, cognom2, dni)
        cursor.execute(insert, values)
        connexio.commit()
        
    if opcio == "c" or opcio == "C":
        if get_fingerprint():
            
            connexio = mysql.connector.connect(host='ipdelservidor', user='projecte', passwd='P@ssw0rd', db='fixatges')
            cursor = connexio.cursor()
            
            insert = "INSERT INTO fixatges (id, datahora) VALUES (%s, NOW())"%(finger.finger_id)
            cursor.execute(insert)
            connexio.commit()
            
            select = "SELECT nom, cognom1, cognom2 FROM treballadors WHERE id = %s"%(finger.finger_id)
            cursor.execute(select)
            for nom, cognom1, cognom2 in cursor.fetchall():
                print ("Benvingut,", nom, cognom1, cognom2)
            cursor.close()

        else:
            print("Empremta no trobada")
            
    if opcio == "d" or opcio == "D":
        if finger.delete_model(get_num()) == adafruit_fingerprint.OK:
            print("L'empremta s'ha esborrat!")
        else:
            print("Hi ha hagut un error al esborrar l'empremta")
            
    if opcio == "e" or opcio == "E":
        connexio = mysql.connector.connect(host='ipdelservidor', user='projecte', passwd='P@ssw0rd', db='fixatges')
        cursor = connexio.cursor()
        select = "SELECT ID, Nom, Cognom1, Cognom2 FROM treballadors"
        cursor.execute(select)
        print ("ID Nom Cognom1 Cognom2")
        for id, nom, cognom1, cognom2 in cursor.fetchall():
            print (id, nom, cognom1, cognom2)
        cursor.close()

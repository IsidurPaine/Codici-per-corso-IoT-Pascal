#########################################################################################
# Read data from serial port                                                            #
#                                                                                       #
# author: Pietro Boccadoro                                                              #
# email: pieroboccadoro13[at]gmail[dot]com                                              #
# date: 2025-02-01                                                                      #
# version: 0.1                                                                          #
#                                                                                       #
# Script Python per leggere i dati del sensore da una porta seriale                     #
# collegata ad Arduino e stampare i valori sulla console.                               #
#                                                                                       #
# Per eseguire questo script, è necessario installare la libreria paho-mqtt e pyserial. #
# Puoi installare le libreria eseguendo il seguente comando:                            #
# pip install pyserial                                                                  #
# Oppure, nella cartella del progetto, esegui il comando:                               #
# pip install -r requirements.txt                                                       #
#########################################################################################

# Importa le librerie necessarie
import serial # Importa la libreria serial per la comunicazione seriale
import time # Importa la libreria time per gestire la temporizzazione delle operazioni e introdurre ritardi

# Configurazione della porta seriale
ser = serial.Serial('COM5', 9600)  # Sostituisci 'COM3' con la porta seriale corretta

# Leggi i dati dalla seriale
try:
    while True:
        if ser.in_waiting > 0:
            # Leggi la linea dalla seriale
            line = ser.readline().decode('utf-8').rstrip() # Rimuovi i caratteri di newline e carriage return
            print(f"Temperatura: {line} C") # Stampa la temperatura
            
            time.sleep(1) # Ritardo di 1 secondo
except KeyboardInterrupt:
    print("Interruzione manuale") # Stampa un messaggio di interruzione manuale
finally:
    ser.close() # Chiudi la porta seriale
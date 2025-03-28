#########################################################################################
# Read data from serial port and send it to MQTT broker                                 #
# author: Pietro Boccadoro                                                              #
# email: pieroboccadoro13[at]gmail[dot]com                                              #   
# date: 2025-02-01                                                                      #
# version: 0.11                                                                         #
#                                                                                       #
# Questo script legge i dati dalla porta seriale e li invia al broker MQTT              #
# tramite il protocollo MQTT. Il messaggio MQTT contiene la temperatura letta           #
# dal sensore di temperatura collegato alla porta seriale.                              #
#                                                                                       #
# Per eseguire questo script, è necessario installare la libreria paho-mqtt e pyserial. #
# Puoi installare le libreria eseguendo il seguente comando:                            #
# pip install paho-mqtt pyserial                                                        #
# Oppure, nella cartella del progetto, esegui il comando:                               #
# pip install -r requirements.txt                                                       #
#########################################################################################

# Importa le librerie necessarie
import serial # Importa la libreria serial per la comunicazione seriale
import time # Importa la libreria time per gestire la temporizzazione delle operazioni e introdurre ritardi
import paho.mqtt.client as mqtt # Importa la libreria paho-mqtt per la comunicazione MQTT

# Configurazione della porta seriale
ser = serial.Serial('COM5', 9600)  # Sostituisci 'COM3' con la porta seriale corretta

# Configurazione MQTT
broker = "localhost" # Indirizzo del broker MQTT
port = 2883 # Porta di default per MQTT
username = ""  # Inserisci il tuo username di shiftr.io
password = ""  # Inserisci la tua password di shiftr.io
topic = "temperatura" # Topic MQTT in cui inviare i dati

# Funzione callback per la connessione
def on_connect(client, userdata, flags, rc):
    print("Connesso con codice risultato: " + str(rc)) # Stampa il codice di connessione

# Inizializza il client MQTT
client = mqtt.Client() # Crea un'istanza del client MQTT
client.username_pw_set(username, password) # Imposta username e password
client.on_connect = on_connect # Imposta la funzione di callback per la connessione

# Connessione al broker MQTT
client.connect(broker, port, 60) # Connessione al broker MQTT
client.loop_start() # Avvia il loop del client MQTT

# Leggi i dati dalla seriale e inviali al broker MQTT
try:
    while True:
        if ser.in_waiting > 0:
            # Leggi la linea dalla seriale
            line = ser.readline().decode('utf-8').rstrip() # Rimuovi i caratteri di newline e carriage return
            print(line) # Stampa la linea letta
            # Controllo della stringa per mandare solo il dato di temperatura in gradi celsius
            # Dalla stringa ricevuta, estrai la parte della temperatura (primo slit)
            # da cui estraggo solo la parte in gradi celsius eliminando (secondo split)
            # il simbolo °C (terzo split)
            line_temperature_celsius = line.split(", ")[1].split(" ")[2].split("°")[0]
            print(f"Temperatura: {line_temperature_celsius} C") # Stampa la temperatura
            
            # Pubblica il messaggio MQTT
            client.publish(topic, line_temperature_celsius) # Invia la temperatura al topic 'temperature'
            
            #TODO: Creare un altro topic dove pubblicare dati
            
            #time.sleep(1) # Ritardo di 1 secondo
except KeyboardInterrupt:
    print("Interruzione manuale") # Stampa un messaggio di interruzione manuale
finally:
    ser.close() # Chiudi la porta seriale
    client.loop_stop() # Ferma il loop del client MQTT
    client.disconnect() # Disconnetti il client MQTT
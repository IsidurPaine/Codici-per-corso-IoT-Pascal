############################################################################
# Generate random data and send it to MQTT broker
# author: Pietro Boccadoro
# date: 2021-09-21
#
# Implementata la lettura dei parametri da un file JSON denominato 'parameters.json'.
#
# Questo script genera dati casuali e li invia al broker MQTT
# tramite il protocollo MQTT. Il messaggio MQTT contiene la temperatura letta
# dai dati generati casualmente.
#
# Per eseguire questo script, è necessario installare la libreria paho-mqtt.
# Puoi installare la libreria eseguendo il seguente comando:
# pip install paho-mqtt
# Oppure, nella cartella del progetto, esegui il comando:
# pip install -r requirements.txt
#
############################################################################

# Importa le librerie necessarie
import re  # Importa la libreria re per utilizzare le espressioni regolari
import json # Importa la libreria per leggere i file json
import time  # Importa la libreria time per gestire i ritardi
import random  # Importa la libreria random per generare dati casuali
import paho.mqtt.client as mqtt  # Importa la libreria paho-mqtt per la comunicazione MQTT


# Variabili globali
parameters_file = "parameters.json" # File JSON contenente i parametri


# Funzione che legge i parametri dal file JSON
def read_parameters(file_path):
    global broker, port, username, password
    try:
        with open(file_path, 'r') as file:
            params = json.load(file)
        broker = params['broker'] # Indirizzo del broker MQTT
        port = params['port'] # Porta del broker MQTT
        username = params['username'] # Inserisci il tuo username di shiftr.io
        password = params['password'] # Inserisci la tua password di shiftr.io
    except FileNotFoundError:
        print("Il file JSON non esiste.") # Stampa un messaggio di errore se il file non esiste
    except json.JSONDecodeError as e:
        print(f"Errore nel parsing del file JSON: {e}") # Stampa un messaggio di errore se c'è un errore nel parsing del file JSON


# Funzione callback per la connessione
def on_connect(client, userdata, flags, rc):
    print("Connesso con codice risultato: " + str(rc)) # Stampa il codice di connessione


# Funzione per generare dati casuali
def generate_random_data():
    data_dict = {
        "Humidity": round(random.uniform(20.0, 80.0), 2),
        "Temperature": round(random.uniform(10.0, 30.0), 2),
        "IdC": round(random.uniform(15.0, 35.0), 2)
    }
    return data_dict


# Funzione principale
def main():
    read_parameters(parameters_file) # Leggi i parametri dal file JSON
    
    # Inizializza il client MQTT
    client = mqtt.Client() # Crea un'istanza del client MQTT
    client.username_pw_set(username, password) # Imposta username e password
    client.on_connect = on_connect # Imposta la funzione di callback per la connessione

    # Connessione al broker MQTT
    client.connect(broker, port, 60) # Connessione al broker MQTT
    client.loop_start() # Avvia il loop del client MQTT

    try:
        while True:  # Inizia un loop infinito
            sensor_data = generate_random_data()  # Genera dati casuali
            print(sensor_data)  # Stampa i dati generati

            # Pubblica un messaggio MQTT per ogni chiave del dizionario
            for key, value in sensor_data.items():  # Cicla sulle chiavi del dizionario
                client.publish(key, value)  # Pubblica il valore sul topic corrispondente alla chiave
                print(f"Pubblicato sul topic {key}: {value}")  # Stampa il messaggio pubblicato per debug

            time.sleep(1) # Aspetta un secondo prima di generare nuovi dati
    
    except KeyboardInterrupt: # Gestisce l'interruzione manuale (Ctrl+C)
        print("Interruzione manuale")  # Stampa un messaggio di interruzione
    finally:
        client.loop_stop()  # Ferma il loop del client MQTT
        client.disconnect()  # Disconnetti il client MQTT


# Avvio del programma
if __name__ == "__main__":
    main()  # Chiama la funzione principale per avviare il programma

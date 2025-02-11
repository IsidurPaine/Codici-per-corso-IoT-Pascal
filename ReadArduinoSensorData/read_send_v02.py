###########################################################################################
# Read data from serial port and send it to MQTT broker                                   #
# author: Pietro Boccadoro                                                                #
# email: pieroboccadoro13[at]gmail[dot]com                                                #
# date: 2025-02-01                                                                        #
# version: 0.2                                                                            #
#                                                                                         #
# Implementata la lettura dei parametri da un file JSON denominato 'parameters.json'.     #
#                                                                                         #
# Questo script legge i dati dalla porta seriale e li invia al broker MQTT                #
# tramite il protocollo MQTT. I messaggi MQTT contengono le singole letture               #
# dal sensore di temperatura collegato alla porta seriale.                                #
#                                                                                         #
# Per eseguire questo script, è necessario installare la libreria paho-mqtt e pyserial.   #
# Puoi installare le libreria eseguendo il seguente comando:                              #
# pip install paho-mqtt pyserial                                                          #
# Oppure, nella cartella del progetto, esegui il comando:                                 #
# pip install -r requirements.txt                                                         #
###########################################################################################


# Importa le librerie necessarie
import re  # Importa la libreria re per utilizzare le espressioni regolari
import json # Importa la libreria per leggere i file json
import time  # Importa la libreria time per gestire i ritardi
import serial  # Importa la libreria serial per la comunicazione seriale
import paho.mqtt.client as mqtt  # Importa la libreria paho-mqtt per la comunicazione MQTT


# Variabili globali
parameters_file = "parameters.json" # File JSON contenente i parametri


# Funzione che legge i parametri dal file JSON
def read_parameters(file_path):
    # Variabili globali in cui verranno salvati i valori letti dalla porta seriale
    global broker, port, username, password, SERIAL_COM_PORT, SERIAL_DATARATE
    try:
        # Carica i dati dal file JSON
        with open(file_path, 'r') as file: # Apre il file in modalità lettura
            params = json.load(file) # Carica i dati dal file JSON
        
        # Assegna i valori alle variabili globali
        broker = params['broker'] # Indirizzo del broker MQTT
        port = params['port'] # Porta del broker MQTT
        username = params['username'] # Inserisci il tuo username di shiftr.io
        password = params['password'] # Inserisci la tua password di shiftr.io
        SERIAL_COM_PORT = params['SERIAL_COM_PORT'] # Porta seriale da cui leggere i dati (sostituisci 'COM3' con la porta corretta)
        SERIAL_DATARATE = params['SERIAL_DATARATE'] # Valore del datarate da usare per leggere dalla seriale.
    except FileNotFoundError: # Gestisce l'eccezione se il file non esiste
        print("Il file JSON non esiste.") # Stampa un messaggio di errore se il file non esiste
    except json.JSONDecodeError as e: # Gestisce l'eccezione se c'è un errore nel parsing del file JSON
        print(f"Errore nel parsing del file JSON: {e}") # Stampa un messaggio di errore se c'è un errore nel parsing del file JSON


# Funzione callback per la connessione
def on_connect(client, userdata, flags, rc): # Funzione di callback per la connessione
    print("Connesso con codice risultato: " + str(rc)) # Stampa il codice di connessione


# Funzione per estrarre i valori dalla stringa
def parse_sensor_data(data_string):
    # Dizionario per i dati estratti
    data_dict = {} # Dizionario vuoto per i dati estratti

    # Pattern regex per individuare i valori
    humidity_pattern = r"Humidity:\s*([\d.]+)%"  # Pattern per l'umidità
    temperature_pattern = r"Temperature:\s*([\d.]+)°C"  # Pattern per la temperatura
    heat_index_pattern = r"IdC:\s*([\d.]+)°C"  # Pattern per l'indice di calore

    # Cerca i valori con regex
    humidity_match = re.search(humidity_pattern, data_string)  # Trova il valore dell'umidità
    temperature_match = re.search(temperature_pattern, data_string)  # Trova il valore della temperatura
    heat_index_match = re.search(heat_index_pattern, data_string)  # Trova il valore dell'indice di calore

    # Aggiungi i valori al dizionario
    if humidity_match: # Se è stato trovato un valore di umidità
        data_dict["Humidity"] = float(humidity_match.group(1))  # Aggiungi l'umidità al dizionario
    if temperature_match: # Se è stato trovato un valore di temperatura
        data_dict["Temperature"] = float(temperature_match.group(1))  # Aggiungi la temperatura al dizionario
    if heat_index_match: # Se è stato trovato un valore di indice di calore
        data_dict["IdC"] = float(heat_index_match.group(1))  # Aggiungi l'indice di calore al dizionario

    return data_dict  # Ritorna il dizionario con i dati estratti


# Funzione per leggere dalla porta seriale
def read_from_serial(serial_port):
    if serial_port.in_waiting > 0:  # Controlla se ci sono dati in attesa di essere letti
        line = serial_port.readline().decode('utf-8').rstrip()  # Leggi una linea dalla seriale, decodifica e rimuovi gli spazi vuoti
        print(f"Ricevuto: {line}")  # Stampa la linea letta per debug
        return line  # Ritorna la linea letta
    return None  # Se non ci sono dati, ritorna None


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

    ser = serial.Serial(SERIAL_COM_PORT, SERIAL_DATARATE)  # Inizializza la comunicazione seriale sulla porta COM3 a 9600 baud (sostituisci 'COM3' con la porta corretta)
    try:
        while True:  # Inizia un loop infinito
            input_string = read_from_serial(ser)  # Leggi i dati dalla porta seriale
            if input_string:  # Se è stata letta una stringa valida
                sensor_data = parse_sensor_data(input_string)  # Estrarre i dati sensoriali dalla stringa
                print(sensor_data)  # Stampa i dati sensoriali estratti

                # Pubblica un messaggio MQTT per ogni chiave del dizionario
                for key, value in sensor_data.items():  # Cicla sulle chiavi del dizionario
                    client.publish(key, value)  # Pubblica il valore sul topic corrispondente alla chiave
                    print(f"Pubblicato sul topic {key}: {value}")  # Stampa il messaggio pubblicato per debug

                time.sleep(1) # Aspetta un secondo prima di leggere nuovamente
    
    except KeyboardInterrupt: # Gestisce l'interruzione manuale (Ctrl+C)
        print("Interruzione manuale")  # Stampa un messaggio di interruzione
    finally:
        ser.close()  # Chiude la porta seriale
        client.loop_stop()  # Ferma il loop del client MQTT
        client.disconnect()  # Disconnetti il client MQTT


# Avvio del programma
if __name__ == "__main__":
    main()  # Chiama la funzione principale per avviare il programma
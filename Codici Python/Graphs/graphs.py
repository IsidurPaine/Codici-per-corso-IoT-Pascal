#########################################################################################
# graphs.py                                                                             #
# author: Pietro Boccadoro                                                              #
# email: pieroboccadoro13[at]gmail[dot]com                                              #
# date: 2025-10-29                                                                      #
# version: 0.1                                                                          #
#                                                                                       #
# # Descrizione: Script Python per la lettura di dati da un sensore tramite seriale     #
# e la visualizzazione in tempo reale di grafici multipli utilizzando Matplotlib.       #
# I dati letti includono umidità, temperatura in Celsius e Fahrenheit, e IDC.           #
#                                                                                       #
# Per eseguire questo script, è necessario installare la libreria matplotlib e pyserial.#
# Puoi installare le libreria eseguendo il seguente comando:                            #
# pip install matplotlib pyserial                                                       #
# Oppure, nella cartella del progetto, esegui il comando:                               #
# pip install -r requirements.txt                                                       #
#########################################################################################


# Importa le librerie necessarie
import serial  # Per la comunicazione seriale con dispositivi esterni
import time    # Per gestire funzioni e ritardi relativi al tempo
import matplotlib.pyplot as plt  # Per creare e gestire grafici
from collections import deque    # Per creare buffer di dati efficienti a dimensione fissa

# Configura la comunicazione seriale sulla porta COM11 con velocità 9600 baud
ser = serial.Serial('COM11', 9600)  

# Definisce il numero massimo di punti dati da memorizzare
max_len = 100  
# Crea oggetti deque (buffer a dimensione fissa) per ogni tipo di dato
humidity_data = deque(maxlen=max_len)        # Memorizza valori di umidità
temperature_c_data = deque(maxlen=max_len)   # Memorizza valori di temperatura Celsius
temperature_f_data = deque(maxlen=max_len)   # Memorizza valori di temperatura Fahrenheit
idc_f_data = deque(maxlen=max_len)          # Memorizza valori IDC Fahrenheit

# Abilita la modalità interattiva per matplotlib
plt.ion()  
# Crea una figura con sottografici 2x2
fig, axs = plt.subplots(2, 2, figsize=(12, 8))
# Imposta il titolo principale per l'intera figura
fig.suptitle('Dati Sensore in Tempo Reale')

# Funzione per aggiornare tutti e quattro i grafici
def update_plots():
    # Aggiorna il grafico dell'umidità (in alto a sinistra)
    axs[0, 0].clear()  # Pulisce il grafico precedente
    axs[0, 0].plot(list(humidity_data), label='Umidità (%)', color='blue')  # Disegna i dati dell'umidità
    axs[0, 0].legend(loc='upper right')  # Aggiunge la legenda
    axs[0, 0].set_title('Umidità')  # Imposta il titolo del sottografico

    # Aggiorna il grafico della temperatura Celsius (in alto a destra)
    axs[0, 1].clear()  # Pulisce il grafico precedente
    axs[0, 1].plot(list(temperature_c_data), label='Temperatura (°C)', color='red')  # Disegna i dati Celsius
    axs[0, 1].legend(loc='upper right')  # Aggiunge la legenda
    axs[0, 1].set_title('Temperatura Celsius')  # Imposta il titolo del sottografico

    # Aggiorna il grafico della temperatura Fahrenheit (in basso a sinistra)
    axs[1, 0].clear()  # Pulisce il grafico precedente
    axs[1, 0].plot(list(temperature_f_data), label='Temperatura (°F)', color='orange')  # Disegna i dati Fahrenheit
    axs[1, 0].legend(loc='upper right')  # Aggiunge la legenda
    axs[1, 0].set_title('Temperatura Fahrenheit')  # Imposta il titolo del sottografico

    # Aggiorna il grafico IDC Celsius (in basso a destra)
    axs[1, 1].clear()  # Pulisce il grafico precedente
    axs[1, 1].plot(list(idc_c_data), label='IdC (°C)', color='green')  # Disegna i dati IDC
    axs[1, 1].legend(loc='upper right')  # Aggiunge la legenda
    axs[1, 1].set_title('IdC Celsius')  # Imposta il titolo del sottografico

    # Regola il layout e aggiorna il display
    plt.tight_layout(rect=[0, 0, 1, 0.96])  # Ottimizza il layout dei sottografici
    plt.pause(0.1)  # Piccola pausa per permettere l'aggiornamento del grafico

try:
    while True:  # Ciclo principale del programma
        if ser.in_waiting > 0:  # Controlla se ci sono dati disponibili da leggere
            # Legge e decodifica una riga dalla porta seriale
            line = ser.readline().decode('utf-8').rstrip()
            print(line)  # Stampa la riga di dati grezza

            # Analizza i diversi valori dalla stringa di input
            line_humidity = float(line.split(", ")[0].split(" ")[1].split("%")[0])  # Estrae il valore dell'umidità
            line_temperature_celsius = float(line.split(", ")[1].split(" ")[2].split("°")[0])  # Estrae la temperatura Celsius
            line_temperature_fahrenheit = float(line.split(", ")[1].split(" ")[3].split("°")[0])  # Estrae la temperatura Fahrenheit
            line_idc_celsius = float(line.split(", ")[2].split(" ")[2].split("°")[0])  # Estrae il valore IDC Celsius
            
            # Prova a estrarre il valore IDC Fahrenheit, imposta a 0 se non disponibile
            try:
                line_idc_fahrenheit = float(line.split(", ")[2].split(" ")[3].split("°")[0])
            except Exception:
                line_idc_fahrenheit = 0.0

            # Stampa i valori analizzati
            print(f"Umidità: {line_humidity} %")
            print(f"Temperatura: {line_temperature_celsius} C")
            print(f"Temperatura: {line_temperature_fahrenheit} F")
            print(f"IdC: {line_idc_celsius} C")
            print(f"IdC: {line_idc_fahrenheit} F")

            # Aggiunge i nuovi valori ai rispettivi deque
            humidity_data.append(line_humidity)
            temperature_c_data.append(line_temperature_celsius)
            temperature_f_data.append(line_temperature_fahrenheit)
            idc_c_data.append(line_idc_celsius)
            idc_f_data.append(line_idc_fahrenheit)

            update_plots()  # Aggiorna tutti i grafici con i nuovi dati
            time.sleep(1)  # Attende 1 secondo prima della prossima iterazione

except KeyboardInterrupt:  # Gestisce l'interruzione del programma (Ctrl+C)
    print("Interruzione manuale")
finally:  # Codice di pulizia che viene eseguito sia in caso di errore che non
    ser.close()  # Chiude la connessione alla porta seriale
    plt.ioff()  # Disabilita la modalità interattiva
    plt.show()  # Mostra lo stato finale del grafico

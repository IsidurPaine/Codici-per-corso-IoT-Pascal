#########################################################################################
# graphs_synthetic.py                                                                   #
#                                                                                       #
# author: Pietro Boccadoro                                                              #
# email: pieroboccadoro13[at]gmail[dot]com                                              #
# date: 2025-10-29                                                                      #
# version: 0.1                                                                          #
#                                                                                       #
# Script Python per la generazione di dati sintetici simulando letture sensore e la     #
# visualizzazione in tempo reale di grafici multipli utilizzando Matplotlib.            #
# I dati simulati includono umidità, temperatura in Celsius e Fahrenheit, e IDC.        #
#########################################################################################

# Importa le librerie necessarie
import time  # importa il modulo time per funzioni di temporizzazione come sleep
import matplotlib.pyplot as plt  # importa pyplot di matplotlib per la creazione di grafici
from collections import deque  # importa deque per buffer a lunghezza fissa
import math  # importa il modulo math per funzioni matematiche (es. sin)
import random  # importa random per generare rumore casuale


# Definisce il numero massimo di punti dati da memorizzare
max_len = 100  # numero massimo di elementi che ogni deque può contenere

# Crea oggetti deque (buffer a dimensione fissa) per ogni tipo di dato
humidity_data = deque(maxlen=max_len)        # Memorizza valori di umidità
temperature_c_data = deque(maxlen=max_len)   # Memorizza valori di temperatura Celsius
temperature_f_data = deque(maxlen=max_len)   # Memorizza valori di temperatura Fahrenheit
idc_c_data = deque(maxlen=max_len)           # Memorizza valori IDC Celsius
idc_f_data = deque(maxlen=max_len)           # Memorizza valori IDC Fahrenheit


# Abilita la modalità interattiva per matplotlib
plt.ion()  # attiva l'interactive mode per aggiornare i grafici senza bloccare l'esecuzione
# Crea una figura con sottografici 2x2
fig, axs = plt.subplots(2, 2, figsize=(12, 8))  # crea figura e array 2x2 di assi con dimensione specifica
# Imposta il titolo principale per l'intera figura
fig.suptitle('Dati Sensore Sintetici in Tempo Reale')  # titolo generale della figura

# Funzione per aggiornare tutti e quattro i grafici
def update_plots():  # definisce la funzione che ridisegna i 4 subplot
    # Aggiorna il grafico dell'umidità (in alto a sinistra)
    axs[0, 0].clear()  # pulisce l'asse prima di ridisegnare
    axs[0, 0].plot(list(humidity_data), label='Umidità (%)', color='blue')  # disegna i dati di umidità
    axs[0, 0].legend(loc='upper right')  # aggiunge legenda in alto a destra
    axs[0, 0].set_title('Umidità')  # imposta il titolo del subplot

    # Aggiorna il grafico della temperatura Celsius (in alto a destra)
    axs[0, 1].clear()  # pulisce l'asse della temperatura Celsius
    axs[0, 1].plot(list(temperature_c_data), label='Temperatura (°C)', color='red')  # disegna temperatura Celsius
    axs[0, 1].legend(loc='upper right')  # mostra legenda
    axs[0, 1].set_title('Temperatura Celsius')  # titolo del subplot

    # Aggiorna il grafico della temperatura Fahrenheit (in basso a sinistra)
    axs[1, 0].clear()  # pulisce l'asse della temperatura Fahrenheit
    axs[1, 0].plot(list(temperature_f_data), label='Temperatura (°F)', color='orange')  # disegna temperatura Fahrenheit
    axs[1, 0].legend(loc='upper right')  # mostra legenda
    axs[1, 0].set_title('Temperatura Fahrenheit')  # titolo del subplot

    # Aggiorna il grafico IDC Celsius (in basso a destra)
    axs[1, 1].clear()  # pulisce l'asse IDC Celsius
    axs[1, 1].plot(list(idc_c_data), label='IdC (°C)', color='green')  # disegna i dati IdC Celsius
    axs[1, 1].legend(loc='upper right')  # mostra legenda
    axs[1, 1].set_title('IdC Celsius')  # titolo del subplot

    # Regola il layout e aggiorna il display
    plt.tight_layout(rect=[0, 0, 1, 0.96])  # aggiorna il layout per evitare sovrapposizioni tenendo conto del titolo
    plt.pause(0.1)  # brevemente pausa per permettere a matplotlib di ridisegnare

# Funzione per generare dati sintetici variabili nel tempo
def generate_synthetic_data(t):  # definisce la funzione che genera i valori simulati in base al tempo t
    # Umidità oscillante con rumore casuale (40-60%)
    humidity = 50 + 10 * math.sin(t / 10) + random.uniform(-2, 2)  # valore medio 50 con ampiezza e rumore
    # Temperatura Celsius oscillante (20-30°C)
    temp_c = 25 + 5 * math.sin(t / 15) + random.uniform(-0.5, 0.5)  # temperatura in °C con oscillazione e rumore
    # Converti temperatura in Fahrenheit
    temp_f = temp_c * 9 / 5 + 32  # conversione da °C a °F
    # IDC Celsius fittizio (30-35°C)
    idc_c = 32 + 2 * math.sin(t / 20) + random.uniform(-0.3, 0.3)  # valore IdC in °C simulato
    # IDC Fahrenheit corrispondente
    idc_f = idc_c * 9 / 5 + 32  # conversione IdC in °F

    return humidity, temp_c, temp_f, idc_c, idc_f  # restituisce la tupla dei valori generati

t = 0  # indice temporale iniziale

try:  # inizio blocco try per gestire interruzione da tastiera
    while True:  # ciclo principale infinito per generare e visualizzare dati in tempo reale
        # Genera nuovi dati sintetici
        humidity, temp_c, temp_f, idc_c, idc_f = generate_synthetic_data(t)  # chiama la funzione di generazione

        # Stampa i valori generati in console
        print(f"Umidità: {humidity:.2f} %")  # stampa umidità formattata con 2 decimali
        print(f"Temperatura: {temp_c:.2f} C")  # stampa temperatura in °C
        print(f"Temperatura: {temp_f:.2f} F")  # stampa temperatura in °F
        print(f"IdC: {idc_c:.2f} C")  # stampa IdC in °C
        print(f"IdC: {idc_f:.2f} F")  # stampa IdC in °F

        # Aggiunge i nuovi valori ai rispettivi deque
        humidity_data.append(humidity)  # inserisce umidità nel buffer circolare
        temperature_c_data.append(temp_c)  # inserisce temperatura °C nel buffer
        temperature_f_data.append(temp_f)  # inserisce temperatura °F nel buffer
        idc_c_data.append(idc_c)  # inserisce IdC °C nel buffer
        idc_f_data.append(idc_f)  # inserisce IdC °F nel buffer

        # Aggiorna tutti i grafici con i nuovi dati
        update_plots()  # richiama la funzione che ridisegna i plot
        time.sleep(1)  # attende 1 secondo prima della prossima iterazione
        t += 1  # incrementa l'indice temporale

except KeyboardInterrupt:  # cattura Ctrl+C dall'utente
    print("Interruzione manuale")  # notifica interruzione

finally:  # sempre eseguito alla fine del try/except
    plt.ioff()  # disabilita la modalità interattiva di matplotlib
    plt.show()  # mostra la figura finale (utile se l'interactive è stato disattivato)

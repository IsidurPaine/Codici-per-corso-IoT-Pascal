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
import math  # fornisce funzioni matematiche come sin, cos, ecc.
import matplotlib.pyplot as plt  # modulo per la creazione di grafici
import random  # fornisce funzioni per generare numeri casuali
import time  # fornisce funzioni legate al tempo come sleep

from collections import deque  # importa deque per buffer a lunghezza limitata


# Funzioni di utilità per la gestione dei dati e dei grafici
def init_data_buffers(max_len=100):  # definisce una funzione per inizializzare i buffer dei dati
    """Inizializza i buffer di dati"""  # docstring che descrive la funzione
    return {  # restituisce un dizionario contenente i buffer per ogni tipo di dato
        'humidity': deque(maxlen=max_len),  # buffer per umidità con dimensione massima max_len
        'temp_c': deque(maxlen=max_len),  # buffer per temperatura in Celsius
        'temp_f': deque(maxlen=max_len),  # buffer per temperatura in Fahrenheit
        'idc_c': deque(maxlen=max_len),  # buffer per IdC in Celsius
        'idc_f': deque(maxlen=max_len)  # buffer per IdC in Fahrenheit
    }

# Funzione per inizializzare i grafici
def init_plots():  # definisce una funzione per inizializzare i grafici
    """Inizializza i grafici"""  # docstring che descrive la funzione
    plt.ion()  # abilita la modalità interattiva di Matplotlib per aggiornamenti dinamici
    fig, axs = plt.subplots(2, 2, figsize=(12, 8))  # crea una figura con una griglia 2x2 di assi
    fig.suptitle('Dati Sensore Sintetici in Tempo Reale')  # imposta il titolo principale della figura
    return fig, axs  # restituisce la figura e gli assi creati

# Funzione per aggiornare i grafici con nuovi dati
def update_plots(axs, data_buffers):  # definisce la funzione per aggiornare i grafici con nuovi dati
    """Aggiorna tutti i grafici"""  # docstring che descrive la funzione
    # Umidità
    axs[0, 0].clear()  # pulisce l'asse in posizione (0,0) prima di ridisegnare
    axs[0, 0].plot(list(data_buffers['humidity']), label='Umidità (%)', color='blue')  # disegna la serie di umidità
    axs[0, 0].legend(loc='upper right')  # mostra la legenda in alto a destra
    axs[0, 0].set_title('Umidità')  # imposta il titolo dell'asse umidità

    # Temperatura Celsius
    axs[0, 1].clear()  # pulisce l'asse in posizione (0,1)
    axs[0, 1].plot(list(data_buffers['temp_c']), label='Temperatura (°C)', color='red')  # disegna la serie temp C
    axs[0, 1].legend(loc='upper right')  # mostra la legenda in alto a destra
    axs[0, 1].set_title('Temperatura Celsius')  # imposta il titolo dell'asse temp C

    # Temperatura Fahrenheit
    axs[1, 0].clear()  # pulisce l'asse in posizione (1,0)
    axs[1, 0].plot(list(data_buffers['temp_f']), label='Temperatura (°F)', color='orange')  # disegna la serie temp F
    axs[1, 0].legend(loc='upper right')  # mostra la legenda in alto a destra
    axs[1, 0].set_title('Temperatura Fahrenheit')  # imposta il titolo dell'asse temp F

    # IDC Celsius
    axs[1, 1].clear()  # pulisce l'asse in posizione (1,1)
    axs[1, 1].plot(list(data_buffers['idc_c']), label='IdC (°C)', color='green')  # disegna la serie IdC C
    axs[1, 1].legend(loc='upper right')  # mostra la legenda in alto a destra
    axs[1, 1].set_title('IdC Celsius')  # imposta il titolo dell'asse IdC C

    plt.tight_layout(rect=[0, 0, 1, 0.96])  # ottimizza il layout per evitare sovrapposizioni con il suptitle
    plt.pause(0.1)  # pausa breve per permettere a Matplotlib di aggiornare la finestra

# Funzione per generare dati sintetici
def generate_synthetic_data(t):  # definisce la funzione che genera dati sintetici basati sul tempo t
    """Genera dati sintetici basati sul tempo"""  # docstring che descrive la funzione
    humidity = 50 + 10 * math.sin(t / 10) + random.uniform(-2, 2)  # genera umidità come sinusoide più rumore casuale
    temp_c = 25 + 5 * math.sin(t / 15) + random.uniform(-0.5, 0.5)  # genera temperatura Celsius con oscillazione e rumore
    temp_f = temp_c * 9 / 5 + 32  # converte la temperatura da Celsius a Fahrenheit
    idc_c = 32 + 2 * math.sin(t / 20) + random.uniform(-0.3, 0.3)  # genera IdC in Celsius con piccole variazioni
    idc_f = idc_c * 9 / 5 + 32  # converte IdC da Celsius a Fahrenheit
    return humidity, temp_c, temp_f, idc_c, idc_f  # restituisce tutti i valori generati

# Funzione per stampare i dati sulla console
def print_data(humidity, temp_c, temp_f, idc_c, idc_f):  # definisce la funzione per stampare i dati su console
    """Stampa i dati sulla console"""  # docstring che descrive la funzione
    print(f"Umidità: {humidity:.2f} %")  # stampa l'umidità con due decimali
    print(f"Temperatura: {temp_c:.2f} C")  # stampa la temperatura in Celsius con due decimali
    print(f"Temperatura: {temp_f:.2f} F")  # stampa la temperatura in Fahrenheit con due decimali
    print(f"IdC: {idc_c:.2f} C")  # stampa IdC in Celsius con due decimali
    print(f"IdC: {idc_f:.2f} F")  # stampa IdC in Fahrenheit con due decimali

# Funzione principale
def main():  # definisce la funzione principale dell'applicazione
    """Funzione principale"""  # docstring che descrive la funzione principale
    data_buffers = init_data_buffers()  # inizializza i buffer dei dati con la dimensione di default
    fig, axs = init_plots()  # crea la figura e gli assi per i grafici
    t = 0  # inizializza il contatore temporale a zero

    try:  # blocco try per consentire la gestione di KeyboardInterrupt
        while True:  # loop infinito per generare, memorizzare e visualizzare i dati in tempo reale
            humidity, temp_c, temp_f, idc_c, idc_f = generate_synthetic_data(t)  # genera nuovi dati sintetici
            print_data(humidity, temp_c, temp_f, idc_c, idc_f)  # stampa i dati generati sulla console

            # Aggiorna i buffer
            data_buffers['humidity'].append(humidity)  # aggiunge il nuovo valore di umidità al buffer
            data_buffers['temp_c'].append(temp_c)  # aggiunge il nuovo valore di temp C al buffer
            data_buffers['temp_f'].append(temp_f)  # aggiunge il nuovo valore di temp F al buffer
            data_buffers['idc_c'].append(idc_c)  # aggiunge il nuovo valore di IdC C al buffer
            data_buffers['idc_f'].append(idc_f)  # aggiunge il nuovo valore di IdC F al buffer

            update_plots(axs, data_buffers)  # aggiorna i grafici con i dati correnti
            time.sleep(1)  # attende 1 secondo prima dell'iterazione successiva
            t += 1  # incrementa il contatore temporale

    except KeyboardInterrupt:  # intercetta l'interruzione manuale (Ctrl+C)
        print("Interruzione manuale")  # notifica l'utente dell'interruzione

    finally:  # blocco finally eseguito comunque per pulire le risorse
        plt.ioff()  # disabilita la modalità interattiva di Matplotlib
        plt.show()  # mostra la figura finale in modalità bloccante

# Avvio del programma
if __name__ == "__main__":  # verifica se il modulo è eseguito direttamente
    main()  # avvia la funzione principale

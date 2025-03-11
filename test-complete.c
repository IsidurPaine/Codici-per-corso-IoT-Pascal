/*
 * Autore: Pietro Boccadoro
 * Email: pieroboccadoro13@gmail.com
 * Descrizione: Questo codice implementa diversi processi utilizzando il sistema operativo Contiki per interagire con vari sensori e dispositivi. Include processi per testare il sensore della batteria, il sensore SHT11, l'accelerometro ADXL345, e il sensore di temperatura TMP102. Gestisce anche i LED in base agli interrupt rilevati dall'accelerometro.
 * Data: 11 Marzo 2025
 * working directory: ~/contiki-2.7/examples/z1
 */

#include "contiki.h"                // Include l'header del sistema operativo Contiki
#include "dev/sht11.h"              // Include l'header per il sensore SHT11

#include "dev/battery-sensor.h"     // Include l'header per il sensore della batteria
#include <stdio.h>                  // Include l'header per le funzioni standard di input/output (printf)

#include "serial-shell.h"           // Include l'header per il modulo di shell seriale
#include "shell-ps.h"               // Include l'header per il modulo shell per il monitoraggio dei processi
#include "shell-file.h"             // Include l'header per il modulo shell per la gestione dei file
#include "shell-text.h"             // Include l'header per il modulo shell per la gestione del testo
#include "dev/adxl345.h"            // Include l'header per l'accelerometro ADXL345

#define LED_INT_ONTIME CLOCK_SECOND/2 // Definisce la durata dell'accensione del LED a mezzo secondo
#define ACCM_READ_INTERVAL CLOCK_SECOND // Definisce l'intervallo di lettura dell'accelerometro a un secondo

#include "dev/i2cmaster.h"          // Include l'header per il modulo I2C master
#include "dev/tmp102.h"             // Include l'header per il sensore di temperatura TMP102

#if 1
#define PRINTF(...) printf(__VA_ARGS__) // Definisce PRINTF per stampare output se la condizione è vera
#else
#define PRINTF(...)                     // Definisce PRINTF per non fare nulla se la condizione è falsa
#endif

#if 0
#define PRINTFDEBUG(...) printf(__VA_ARGS__) // Definisce PRINTFDEBUG per stampare output di debug se la condizione è vera
#else
#define PRINTFDEBUG(...)                    // Definisce PRINTFDEBUG per non fare nulla se la condizione è falsa
#endif

#define TMP102_READ_INTERVAL (CLOCK_SECOND/2) // Definisce l'intervallo di lettura del TMP102 a mezzo secondo

static process_event_t ledOff_event; // Dichiarazione di un evento per spegnere il LED

float floor(float x) {
  // Funzione per arrotondare per difetto un numero float
  if (x >= 0.0f) {
    return (float)((int)x);
  } else {
    return (float)((int)x - 1);
  }
}

/*---------------------------------------------------------------------------*/
PROCESS(test_battery_process, "Battery Sensor Test"); // Dichiarazione del processo per testare il sensore della batteria
PROCESS(test_sht11_process, "SHT11 test");            // Dichiarazione del processo per testare il sensore SHT11
PROCESS(accel_process, "Test Accel process");         // Dichiarazione del processo per testare l'accelerometro
PROCESS(led_process, "LED handling process");         // Dichiarazione del processo per gestire i LED
PROCESS(temp_process, "Test Temperature process");    // Dichiarazione del processo per testare il sensore di temperatura
AUTOSTART_PROCESSES(&test_sht11_process, &test_battery_process, &accel_process, &led_process, &temp_process);
// Dichiarazione dei processi da avviare automaticamente

/*---------------------------------------------------------------------------*/
PROCESS_THREAD(test_battery_process, ev, data) {
  // Thread del processo per testare il sensore della batteria

  static struct etimer et; // Dichiarazione di un timer

  PROCESS_BEGIN(); // Inizio del processo

  SENSORS_ACTIVATE(battery_sensor); // Attivazione del sensore della batteria

  for (etimer_set(&et, CLOCK_SECOND);; etimer_reset(&et)) {
    // Ciclo infinito: imposta e resetta il timer ogni secondo
    uint16_t bateria = battery_sensor.value(0); // Legge il valore del sensore della batteria
    float mv = (bateria * 2.500 * 2) / 4096; // Calcola la tensione in millivolt
    printf("Battery: %i (%ld.%03d mV)\n", bateria, (long)mv,
           (unsigned)((mv - floor(mv)) * 1000)); // Stampa il valore della batteria in millivolt
  }

  SENSORS_DEACTIVATE(battery_sensor); // Disattivazione del sensore della batteria

  PROCESS_END(); // Fine del processo
}

/*---------------------------------------------------------------------------*/
PROCESS_THREAD(test_sht11_process, ev, data) {
  // Thread del processo per testare il sensore SHT11

  static struct etimer et; // Dichiarazione di un timer
  static unsigned rh; // Dichiarazione di una variabile per l'umidità relativa

  PROCESS_BEGIN(); // Inizio del processo

  sht11_init(); // Inizializzazione del sensore SHT11

  for (etimer_set(&et, CLOCK_SECOND);; etimer_reset(&et)) {
    // Ciclo infinito: imposta e resetta il timer ogni secondo
    PROCESS_YIELD(); // Cede il controllo e attende un evento
    printf("Temperature: %u degrees Celsius\n",
           (unsigned)(-39.60 + 0.01 * sht11_temp())); // Stampa la temperatura
    rh = sht11_humidity(); // Legge l'umidità relativa
    printf("Rel. humidity: %u%%\n",
           (unsigned)(-4 + 0.0405 * rh - 2.8e-6 * (rh * rh))); // Stampa l'umidità relativa
  }

  PROCESS_END(); // Fine del processo
}

/*---------------------------------------------------------------------------*/
void print_int(uint16_t reg) {
  // Funzione per stampare i vari tipi di interrupt generati dall'accelerometro ADXL345
#define ANNOYING_ALWAYS_THERE_ANYWAY_OUTPUT 0
#if ANNOYING_ALWAYS_THERE_ANYWAY_OUTPUT
  if (reg & ADXL345_INT_OVERRUN) {
    printf("Overrun ");
  }
  if (reg & ADXL345_INT_WATERMARK) {
    printf("Watermark ");
  }
  if (reg & ADXL345_INT_DATAREADY) {
    printf("DataReady ");
  }
#endif
  if (reg & ADXL345_INT_FREEFALL) {
    printf("Freefall ");
  }
  if (reg & ADXL345_INT_INACTIVITY) {
    printf("InActivity ");
  }
  if (reg & ADXL345_INT_ACTIVITY) {
    printf("Activity ");
  }
  if (reg & ADXL345_INT_DOUBLETAP) {
    printf("DoubleTap ");
  }
  if (reg & ADXL345_INT_TAP) {
    printf("Tap ");
  }
  printf("\n");
}

/*---------------------------------------------------------------------------*/
void accm_ff_cb(uint8_t reg) {
  // Callback per la rilevazione della caduta libera dell'accelerometro
  L_ON(LEDS_B); // Accende il LED blu
  process_post(&led_process, ledOff_event, NULL); // Posta l'evento per spegnere il LED
  printf("~~[%u] Freefall detected! (0x%02X) -- ", ((uint16_t)clock_time()) / 128, reg);
  // Stampa un messaggio di rilevazione della caduta libera
  print_int(reg); // Stampa il tipo di interrupt
}

/*---------------------------------------------------------------------------*/
void accm_tap_cb(uint8_t reg) {
  // Callback per la rilevazione del tap e double tap dell'accelerometro
  process_post(&led_process, ledOff_event, NULL); // Posta l'evento per spegnere il LED
  if (reg & ADXL345_INT_DOUBLETAP) {
    L_ON(LEDS_G); // Accende il LED verde
    printf("~~[%u] DoubleTap detected! (0x%02X) -- ", ((uint16_t)clock_time()) / 128, reg);
    // Stampa un messaggio di rilevazione del double tap
  } else {
    L_ON(LEDS_R); // Accende il LED rosso
    printf("~~[%u] Tap detected! (0x%02X) -- ", ((uint16_t)clock_time()) / 128, reg);
    // Stampa un messaggio di rilevazione del tap
  }
  print_int(reg); // Stampa il tipo di interrupt
}

/*---------------------------------------------------------------------------*/
static struct etimer ledETimer; // Dichiarazione di un timer per il LED
PROCESS_THREAD(led_process, ev, data) {
  // Thread del processo per gestire i LED
  PROCESS_BEGIN(); // Inizio del processo
  while (1) {
    PROCESS_WAIT_EVENT_UNTIL(ev == ledOff_event); // Attende l'evento per spegnere il
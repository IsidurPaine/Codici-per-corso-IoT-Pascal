/*
 * Autore: Pietro Boccadoro
 * Email: pieroboccadoro13@gmail.com
 * Descrizione: Questo codice implementa diversi processi utilizzando il sistema operativo Contiki per interagire con vari sensori e dispositivi. Include processi per testare il sensore della batteria, il sensore SHT11, l'accelerometro ADXL345, e il sensore di temperatura TMP102. Gestisce anche i LED in base agli interrupt rilevati dall'accelerometro.
 * Data: 11 Marzo 2025
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
void
print_int(uint16_t reg){
#define ANNOYING_ALWAYS_THERE_ANYWAY_OUTPUT 0
#if ANNOYING_ALWAYS_THERE_ANYWAY_OUTPUT
  if(reg & ADXL345_INT_OVERRUN) {
    printf("Overrun ");
  }
  if(reg & ADXL345_INT_WATERMARK) {
    printf("Watermark ");
  }
  if(reg & ADXL345_INT_DATAREADY) {
    printf("DataReady ");
  }
#endif
  if(reg & ADXL345_INT_FREEFALL) {
    printf("Freefall ");
  }
  if(reg & ADXL345_INT_INACTIVITY) {
    printf("InActivity ");
  }
  if(reg & ADXL345_INT_ACTIVITY) {
    printf("Activity ");
  }
  if(reg & ADXL345_INT_DOUBLETAP) {
    printf("DoubleTap ");
  }
  if(reg & ADXL345_INT_TAP) {
    printf("Tap ");
  }
  printf("\n");
}

/*---------------------------------------------------------------------------*/
/* accelerometer free fall detection callback */

void
accm_ff_cb(uint8_t reg){
  L_ON(LEDS_B);
  process_post(&led_process, ledOff_event, NULL);
  printf("~~[%u] Freefall detected! (0x%02X) -- ", ((uint16_t) clock_time())/128, reg);
  print_int(reg);
}
/*---------------------------------------------------------------------------*/
/* accelerometer tap and double tap detection callback */

void
accm_tap_cb(uint8_t reg){
  process_post(&led_process, ledOff_event, NULL);
  if(reg & ADXL345_INT_DOUBLETAP){
    L_ON(LEDS_G);
    printf("~~[%u] DoubleTap detected! (0x%02X) -- ", ((uint16_t) clock_time())/128, reg);
  } else {
    L_ON(LEDS_R);
    printf("~~[%u] Tap detected! (0x%02X) -- ", ((uint16_t) clock_time())/128, reg);
  }
  print_int(reg);
}
/*---------------------------------------------------------------------------*/
/* When posted an ledOff event, the LEDs will switch off after LED_INT_ONTIME.
      static process_event_t ledOff_event;
      ledOff_event = process_alloc_event();
      process_post(&led_process, ledOff_event, NULL);
*/

static struct etimer ledETimer;
PROCESS_THREAD(led_process, ev, data) {
  PROCESS_BEGIN();
  while(1){
    PROCESS_WAIT_EVENT_UNTIL(ev == ledOff_event);
    etimer_set(&ledETimer, LED_INT_ONTIME);
    PROCESS_WAIT_EVENT_UNTIL(etimer_expired(&ledETimer));
    L_OFF(LEDS_R + LEDS_G + LEDS_B);
  }
  PROCESS_END();
}

/*---------------------------------------------------------------------------*/
/*  Returns a string with the argument byte written in binary.
    Example usage:
      printf("Port1: %s\n", char2bin(P1IN));
*/    
/*
static uint8_t b[9];

static uint8_t
*char2bin(uint8_t x) {
  uint8_t z;
  b[8] = '\0';
  for (z = 0; z < 8; z++) {
    b[7-z] = (x & (1 << z)) ? '1' : '0';
  }
  return b;
}
*/
/*---------------------------------------------------------------------------*/
/* Main process, setups  */

static struct etimer et;

PROCESS_THREAD(accel_process, ev, data) {
  PROCESS_BEGIN();
  {
    int16_t x, y, z;

    serial_shell_init();
    shell_ps_init();
    shell_file_init();  // for printing out files
    shell_text_init();  // for binprint

    /* Register the event used for lighting up an LED when interrupt strikes. */
    ledOff_event = process_alloc_event();

    /* Start and setup the accelerometer with default values, eg no interrupts enabled. */
    accm_init();

    /* Register the callback functions for each interrupt */
    ACCM_REGISTER_INT1_CB(accm_ff_cb);
    ACCM_REGISTER_INT2_CB(accm_tap_cb);

    /* Set what strikes the corresponding interrupts. Several interrupts per pin is 
      possible. For the eight possible interrupts, see adxl345.h and adxl345 datasheet. */
    accm_set_irq(ADXL345_INT_FREEFALL, ADXL345_INT_TAP + ADXL345_INT_DOUBLETAP);

    while (1) {
      x = accm_read_axis(X_AXIS);
      y = accm_read_axis(Y_AXIS);
      z = accm_read_axis(Z_AXIS);
      printf("x: %d y: %d z: %d\n", x, y, z);

      etimer_set(&et, ACCM_READ_INTERVAL);
      PROCESS_WAIT_EVENT_UNTIL(etimer_expired(&et));
    }
  }
  PROCESS_END();
}

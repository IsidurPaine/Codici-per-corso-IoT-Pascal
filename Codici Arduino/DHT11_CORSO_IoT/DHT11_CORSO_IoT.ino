/*
  Questo programma legge il valore della temperatura da un sensore DHT11 
  connesso al pin digitale 3 della scheda Arduino Uno e lo stampa sulla porta seriale ogni secondo.
  
  Setup:
  - Connettere il pin dati del sensore SHT11 al pin digitale 2 della scheda Arduino.
  - Collegare VCC e GND del sensore SHT11 rispettivamente ai pin 5V e GND della scheda Arduino.
  - Caricare questo sketch sulla scheda Arduino.
  - Aprire il monitor seriale per visualizzare i valori della temperatura letti dal sensore.
*/

#include <DHT.h>  // Include la libreria DHT per gestire il sensore DHT11

#define DHTPIN 2       // Definisce il pin usato per connettere il sensore, in questo caso il pin digitale 2
#define DHTTYPE DHT11  // Definisce il tipo di sensore, in questo caso DHT11

DHT dht(DHTPIN, DHTTYPE);  // Crea un oggetto DHT usando il pin e il tipo di sensore definiti

void setup() {
  Serial.begin(9600);  // Inizializza la comunicazione seriale a una velocità di 9600 baud
  //Serial.println(F("Test DHT11!"));  // Stampa una stringa di testo per indicare che il test del sensore DHT11 è iniziato

  dht.begin();  // Inizializza il sensore DHT
}

void loop() {
  delay(2000);  // Aspetta 2 secondi tra le misurazioni, poiché il sensore è lento

  float h = dht.readHumidity();  // Legge l'umidità dal sensore e la memorizza nella variabile h
  float t = dht.readTemperature();  // Legge la temperatura in gradi Celsius e la memorizza nella variabile t
  float f = dht.readTemperature(true);  // Legge la temperatura in gradi Fahrenheit e la memorizza nella variabile f

  if (isnan(h) || isnan(t) || isnan(f)) {  // Controlla se le letture sono fallite (ritornano NaN)
    Serial.println(F("Lettura dal sensore DHT fallita!"));  // Stampa un messaggio di errore se la lettura è fallita
    return;  // Esce dalla funzione loop per riprovare alla prossima iterazione
  }

  float hif = dht.computeHeatIndex(f, h);  // Calcola l'indice di calore in gradi Fahrenheit e lo memorizza nella variabile hif
  float hic = dht.computeHeatIndex(t, h, false);  // Calcola l'indice di calore in gradi Celsius e lo memorizza nella variabile hic

  Serial.print(F("Humidity: "));  // Stampa la stringa "Umidità: " sulla porta seriale
  Serial.print(h);  // Stampa il valore dell'umidità sulla porta seriale
  Serial.print(F("%,  Temperature: "));  // Stampa la stringa "%  Temperatura: " sulla porta seriale
  Serial.print(t);  // Stampa il valore della temperatura in gradi Celsius sulla porta seriale
  Serial.print(F("°C "));  // Stampa la stringa "°C " sulla porta seriale
  Serial.print(f);  // Stampa il valore della temperatura in gradi Fahrenheit sulla porta seriale
  Serial.print(F("°F,  IdC: "));  // Stampa la stringa "°F  Indice di calore: " sulla porta seriale
  Serial.print(hic);  // Stampa il valore dell'indice di calore in gradi Celsius sulla porta seriale
  Serial.print(F("°C "));  // Stampa la stringa "°C " sulla porta seriale
  Serial.print(hif);  // Stampa il valore dell'indice di calore in gradi Fahrenheit sulla porta seriale
  Serial.println(F("°F"));  // Stampa la stringa "°F" e va a capo

  delay(1000);  // Aspetta un secondo prima della prossima iterazione del loop
}

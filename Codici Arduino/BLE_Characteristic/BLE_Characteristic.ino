#include <BLEDevice.h> // Include la libreria per il dispositivo BLE
#include <BLEUtils.h> // Include la libreria per le utility BLE
#include <BLEServer.h> // Include la libreria per il server BLE

BLECharacteristic *pCharacteristic; // Dichiarazione di un puntatore a una caratteristica BLE
bool deviceConnected = false; // Variabile per tracciare lo stato della connessione del dispositivo

// UUID del servizio e della caratteristica
#define SERVICE_UUID "12345678-1234-1234-1234-123456789012"
#define CHARACTERISTIC_UUID "87654321-4321-4321-4321-210987654321"

// Classe per gestire le callback del server BLE
class MyServerCallbacks: public BLEServerCallbacks {
  void onConnect(BLEServer* pServer) {
    deviceConnected = true; // Quando il dispositivo si connette, impostiamo la variabile a true
  };

  void onDisconnect(BLEServer* pServer) {
    deviceConnected = false; // Quando il dispositivo si disconnette, impostiamo la variabile a false
  }
};

void setup() {
  Serial.begin(115200); // Inizializziamo la comunicazione seriale a 115200 baud

  BLEDevice::init("ESP32_BT"); // Inizializziamo il dispositivo BLE con il nome "ESP32_BT"
  BLEServer *pServer = BLEDevice::createServer(); // Creiamo un server BLE
  pServer->setCallbacks(new MyServerCallbacks()); // Impostiamo le callback del server

  BLEService *pService = pServer->createService(SERVICE_UUID); // Creiamo un servizio BLE con l'UUID specificato
  pCharacteristic = pService->createCharacteristic(
                      CHARACTERISTIC_UUID,
                      BLECharacteristic::PROPERTY_READ | // Proprietà di lettura
                      BLECharacteristic::PROPERTY_WRITE // Proprietà di scrittura
                    );

  pCharacteristic->setValue("Hello World"); // Impostiamo il valore iniziale della caratteristica
  pService->start(); // Avviamo il servizio

  BLEAdvertising *pAdvertising = BLEDevice::getAdvertising(); // Otteniamo l'oggetto pubblicitario BLE
  pAdvertising->addServiceUUID(SERVICE_UUID); // Aggiungiamo l'UUID del servizio alla pubblicità
  pAdvertising->setScanResponse(true); // Impostiamo la risposta di scansione
  pAdvertising->setMinPreferred(0x06); // Impostiamo il valore minimo preferito per l'intervallo pubblicitario
  pAdvertising->setMinPreferred(0x12); // Impostiamo un altro valore minimo preferito per l'intervallo pubblicitario
  BLEDevice::startAdvertising(); // Iniziamo la pubblicità BLE
  Serial.println("Il dispositivo è pronto per essere rilevato"); // Messaggio di conferma
}

void loop() {
  if (deviceConnected) { // se il dispositivo si connette
    String value = pCharacteristic->getValue().c_str();  // Otteniamo il valore della caratteristica
    Serial.println("Caratteristica letta: " + value);  // Stampiamo il valore della caratteristica
  } else {
    Serial.println("Dispositivo non connesso"); // Messaggio quando il dispositivo non è connesso
  }
}

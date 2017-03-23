/*  LoRaWAN GPS Tracker
 *  Daniel Saul 2017
 */

#include <rn2xx3.h>
#include <SoftwareSerial.h>
#include <EEPROM.h>
#include "gps.h"

#define EEPROM_LOW_BYTE 0
#define EEPROM_HIGH_BYTE 1

#define TX_COUNT 1
#define WAIT_TIME 5000

const char DEVICE_ADDRESS[]             = "";
const char APPLICATION_SESSION_KEY[]    = "";
const char NETWORK_SESSION_KEY[]        = "";

SoftwareSerial loraSerial(5, 4);

rn2xx3 myLora(loraSerial);

struct payload {
 
  int32_t lat;
  int32_t lon;
  int32_t alt; 
  uint16_t i;
  uint8_t hour;
  uint8_t mins;
  uint8_t secs;
  uint8_t sats;

};

void setup() {

  // Start Serial
  Serial.begin(57600);
  loraSerial.begin(57600);
  delay(1000);
  Serial.println("Startup");

  // Start EEPROM
  EEPROM.begin(4);

  // Setup RN2483 radio
  initialize_radio();

  // Setup GPS
  gps_setup();

  delay(2000);

}

void loop() {

  payload msg;

  msg.lat = 0;
  msg.lon = 0;
  msg.alt = 0;
  msg.hour = 0;
  msg.mins = 0;
  msg.secs = 0;
  msg.sats = 0;
  uint8_t fx = 0;

  uint8_t b = 0;
  while(fx != 3 && fx != 2 ){ 
    Serial.println("Getting GPS...");
    b = getLocation(&msg.lat, &msg.lon, &msg.alt);
    delay(1);
    b = gps_get_time(&msg.hour, &msg.mins, &msg.secs);
    delay(1);
    b = gps_check_lock(&fx, &msg.sats);
    delay(1);
    Serial.println(msg.sats);
  }

  counter_inc();
  msg.i = counter_get();

  Serial.println("TXing...");

  for(int i=0;i<TX_COUNT;i++){
    myLora.txBytes((unsigned char*) &msg, sizeof(msg));
    delay(10);
  }
  
  delay(WAIT_TIME);
}


void initialize_radio() {

  delay(100);
  loraSerial.flush();

  String hweui = myLora.hweui();
  while(hweui.length() != 16)
  {
    Serial.println("Communication with RN2483 unsuccessful. Power cycle the board.");
    Serial.println(hweui);
    delay(10000);
    hweui = myLora.hweui();
  }

  Serial.println(myLora.sysver());

  bool join_result = false;
  join_result = myLora.initABP(DEVICE_ADDRESS, APPLICATION_SESSION_KEY, NETWORK_SESSION_KEY);

  if(!join_result){
    Serial.println("Unable to join network with provided settings.");
  }

  Serial.println("RN2483 Initialised.");

}

uint16_t counter_get()
{
    byte lowByte = EEPROM.read(EEPROM_LOW_BYTE);
    byte highByte = EEPROM.read(EEPROM_HIGH_BYTE);
    return ((highByte << 8) | lowByte);
}

void counter_set(uint16_t new_counter)
{
    EEPROM.write(EEPROM_LOW_BYTE, (byte) (0xFF & new_counter));
    EEPROM.write(EEPROM_HIGH_BYTE, (byte) (new_counter >> 8));
}

void counter_inc()
{
    counter_set(counter_get() + 1);
}

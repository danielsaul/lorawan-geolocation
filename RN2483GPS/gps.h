/**
  * gps.h
  * Daniel Saul
  */


#ifndef GPS_H
#define GPS_H

#include "Arduino.h"
#include <SoftwareSerial.h>


const uint16_t gps_timeout = 10000;

void gps_setup();
bool gps_get(int32_t* lat, int32_t* lon, int32_t* alt, uint8_t* hr, uint8_t* mn, uint8_t* sc, uint8_t* st, uint8_t* fx);
bool setOutputUBX();
bool getBytes(uint8_t count, uint8_t* buff);
uint8_t getLocation(int32_t* lat, int32_t* lon, int32_t* alt);
uint8_t gps_get_time(uint8_t* hour, uint8_t* minute, uint8_t* second);
uint8_t gps_check_lock(uint8_t* lock, uint8_t* sats);
void sendUBX(uint8_t *MSG, uint8_t len);
bool getUBX_ACK(uint8_t *MSG);

#endif

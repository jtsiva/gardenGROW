#include <ESP8266HTTPClient.h>
#include <ESP8266WiFi.h>
#include <ArduinoJson.h>



/*
 * This module is responsible for communicating with the garden spikes
 * over XBee radios, collecting their statistics, passing those statistics
 * to the server, turning the water on/off, and measuring the water usage. * 
 * 
 * */

 

 
const char* host = "";

const uint32 sleepDuration = 1800000000; //30 minutes

float waterUsage = 0.0;
long waterDuration[3] = {0,0,0}

typedef struct SpikeInfo
{
  int temp;
  int light;
  int CMS;
  int RMS;
}SpikeInfo;

bool connect ()
{
  // We start by connecting to a WiFi network
 
  //Serial.println();
  //Serial.println();
  //Serial.print("Connecting to ");
  //Serial.println(ssid);
  
  WiFi.begin(ssid, password);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    //Serial.print(".");
  }
 
//  Serial.println("");
//  Serial.println("WiFi connected");  
//  Serial.println("IP address: ");
//  Serial.println(WiFi.localIP());
}

/* *********** Timing/operation *************
 * Since the deep sleep causes a reset we need to rely on the server
 * to keep track of how much time we have until the next watering event.
 * After each sleep cycle we will do the following:
 *     Initialize Serial and get updated sensor readings from Spikes via XBee
 *     Connect to WiFi
 *     Send updated sensor information to server
 *     Get updates from server
 *     IF it's time to water
 *         Put WiFi to sleep
 *         water for duration
 *         Turn WiFi back on
 *         Send water usage stats to server
 *     Go back to deep sleep
 * */

void setup() {
  Serial.begin(115200);
  delay(100);
  connect ();
  
}

void checkIn ()
{
  updateOffsets ();
  sendUpdatedWaterUsage ();
}

bool updateOffsets ()
{
  //ask server for offsets
}

bool sendWaterUsage ()
{
  //one way update
}

bool sendSensorUpdates ()
{
  //one way update
  return true;
}

bool getWaterUsage(int * pUsage)
{
  //This relies on periodically (using time-based interrupts)
  //checking the meter (and counting revolutions..)

  return true;
}

bool getDataFromSpike(int id, int * pTemp, int * pCMS, int * pRMS, int * pLight)
{
  if (NULL != pTemp && NULL != pCMS && NULL != pRMS && NULL != pLight)
  {
    //broadcast XBee sample request
    //This could be used to parse an XBee response
    //sort out which ID goes with which spike...
  }

  return true;
}


void loop ()
{
  if (WiFi.status() == WL_CONNECTED) { //Check WiFi connection status
 
    StaticJsonBuffer<300> JSONbuffer;   //Declaring static JSON buffer
    JsonObject& JSONencoder = JSONbuffer.createObject(); 
 
    JSONencoder["spikeID"] = 0;
    JSONencoder["temp"] = 20;
    JSONencoder["CMS"] = 500;
    JSONencoder["RMS"] =  600;
    JSONencoder["light"] = 2;
 
    char JSONmessageBuffer[300];
    JSONencoder.prettyPrintTo(JSONmessageBuffer, sizeof(JSONmessageBuffer));
    Serial.println(JSONmessageBuffer);
 
    HTTPClient http;    //Declare object of class HTTPClient
 
    http.begin("http://192.168.0.8:8080/");      //Specify request destination
    http.addHeader("Content-Type", "application/json");  //Specify content-type header
 
    int httpCode = http.POST(JSONmessageBuffer);   //Send the request
    String payload = http.getString();                                        //Get the response payload
 
    Serial.println(httpCode);   //Print HTTP return code
    Serial.println(payload);    //Print request response payload
 
    http.end();  //Close connection
 
  } else {
 
    Serial.println("Error in WiFi connection");
 
  }
 
  delay(30000);  //Send a request every 30 seconds
 
}


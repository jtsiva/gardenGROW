#include <ESP8266HTTPClient.h>
#include <ESP8266WiFi.h>
#include <ArduinoJson.h>
#include <Esp.h>



/*
 * This module is responsible for communicating with the garden spikes
 * over XBee radios, collecting their statistics, passing those statistics
 * to the server, turning the water on/off, and measuring the water usage. * 
 * 
 * */

 
const char* host = "";

const uint32 sleepDuration = 30000000;//30 seconds 1800000000; //30 minutes

//os_timer_t myTimer;

float waterUsage = 0.0;
unsigned long waterDuration[3] = {0,0,0};
#define VALVE_0 12
#define VALVE_1 13
#define VALVE_2 14
const int valvePin[] = {VALVE_0, VALVE_1, VALVE_2};

unsigned long wateringTimeStart;

typedef struct SpikeInfo
{
  int temp;
  int light;
  int CMS;
  int RMS;
}SpikeInfo;


// flow meter code mostly from:
//https://github.com/adafruit/Adafruit-Flow-Meter/blob/master/Adafruit_FlowMeter.pde

// which pin to use for reading the sensor? can use any pin!
#define FLOWSENSORPIN 5

// count how many pulses!
volatile uint16_t pulses = 0;
// track the state of the pulse pin
volatile uint8_t lastflowpinstate;
// you can try to keep time of how long it is between pulses
volatile uint32_t lastflowratetimer = 0;
// and use that to calculate a flow rate
volatile float flowrate;
// Interrupt is called once a millisecond, looks for any pulses from the sensor!
void timerCallback(void *pArg) {
  uint8_t x = digitalRead(FLOWSENSORPIN);
  
  if (x == lastflowpinstate) {
    lastflowratetimer++;
    return; // nothing changed!
  }
  
  if (x == HIGH) {
    //low to high transition!
    pulses++;
  }
  lastflowpinstate = x;
  flowrate = 1000.0;
  flowrate /= lastflowratetimer;  // in hertz
  lastflowratetimer = 0;
}

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

bool getWateringDuration ()
{
  //ask server for offsets
  return true;
}

bool sendWaterUsage ()
{
  //one way update
  return true;
}

bool sendSensorUpdates ()
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
    http.begin("http://192.168.0.11:8080/");      //Specify request destination
    http.addHeader("Content-Type", "application/json");  //Specify content-type header
  
    int httpCode = http.POST(JSONmessageBuffer);   //Send the request
    String payload = http.getString();          //Get the response payload
  
    Serial.println(httpCode);   //Print HTTP return code
    Serial.println(payload);    //Print request response payload
  
    http.end();  //Close connection
  } else {
 
    Serial.println("Error in WiFi connection");
 
  }
  return true;
}

bool getSensorUpdates ()
{
  //send broadcast request for data and parse response
  return true;
}

bool getSpikeInfo(SpikeInfo * pSpike /*, rx16 response*/)
{
  if (NULL != pSpike)
  {
    //broadcast XBee sample request
    //This could be used to parse an XBee response
    //sort out which ID goes with which spike...
    //https://github.com/andrewrapp/xbee-arduino/blob/wiki/DevelopersGuide.md
  }

  return true;
}

// From: https://github.com/esp8266/Arduino/issues/644

void wifiOn()
{
  WiFi.forceSleepWake();
  WiFi.mode(WIFI_STA);  
  //connect();
  WiFi.begin(ssid, password);
}

void wifiOff ()
{
  WiFi.disconnect(); 
  WiFi.mode(WIFI_OFF);
  WiFi.forceSleepBegin();
  delay(1);
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
 *         water for duration (in main loop)
 *         Turn WiFi back on (in main loop)
 *         Send water usage stats to server (in main loop)
 *         Go back to deep sleep (in main loop)
 *     Go back to deep sleep
 * */

void setup() {
  bool startWatering = false;
  Serial.begin(115200);
  getSensorUpdates (); //talk to Spikes to get sensor data
  connect (); // connect to the WiFi!
  sendSensorUpdates ();
  getWateringDuration(); // set waterDuration[] array from server response

  for (int i = 0; !(startWatering |= (waterDuration[i] != 0)) && i < 3; i++);

  if (startWatering)
  {
    //turn off the WiFi radio to save power!
    wifiOff();
    pinMode(FLOWSENSORPIN, INPUT);
    digitalWrite(FLOWSENSORPIN, HIGH);
    lastflowpinstate = digitalRead(FLOWSENSORPIN);
    
    for (int i = 0; i < 3; i++)
    {
      pinMode(valvePin[i], OUTPUT);
    }

    wateringTimeStart = millis();
    //From http://www.switchdoc.com/2015/10/iot-esp8266-timer-tutorial-arduino-ide/
    //os_timer_setfn(&myTimer, timerCallback, NULL);
    //os_timer_arm(&myTimer, 1, true);
  }
  else
  {
    // go back to deep sleep
    //system_deep_sleep_set_option(0);
    //system_deep_sleep(sleepDuration); //- See more at: http://www.esp8266.com/viewtopic.php?f=32&t=2305#sthash.a8lAW0M0.dpuf
    ESP.deepSleep (sleepDuration, WAKE_RF_DEFAULT);
  }
}




void loop ()
{
  bool doneWatering = true;
  
  for (int i = 0; i < 3; i++)
  {
    //check if we should start or stop watering and do that
    if ((millis() - wateringTimeStart) <= waterDuration[i])
    {
      digitalWrite (valvePin[i], HIGH);
      doneWatering = false;
    }
    else
    {
      digitalWrite (valvePin[i], LOW);
      doneWatering &= true;
    }
  }

  if (doneWatering)
  {
    wifiOn (); //back on so we can send data
    sendWaterUsage ();
    //deep sleep
//    system_deep_sleep_set_option(0);
//    system_deep_sleep(sleepDuration);
  ESP.deepSleep (sleepDuration, WAKE_RF_DEFAULT);
  }
  delay(15000);  //Check every 15 seconds
                 //does it matter if we water 15s too much or too little?
 }


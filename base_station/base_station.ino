#include <ESP8266HTTPClient.h>
#include <ESP8266WiFi.h>
#include <ArduinoJson.h>
#include <Esp.h>
#include <XBee.h>




/*
 * This module is responsible for communicating with the garden spikes
 * over XBee radios, collecting their statistics, passing those statistics
 * to the server, turning the water on/off, and measuring the water usage. * 
 * 
 * */


 
const char* host = "";

const uint32 sleepDuration = 10000000;//10 seconds 1800000000; //30 minutes

float waterUsage = 0.0;
unsigned long waterDuration[3] = {0,0,0};
#define VALVE_0 12
#define VALVE_1 13
#define VALVE_2 14
const int valvePin[] = {VALVE_0, VALVE_1, VALVE_2};

unsigned long wateringTimeStart;
typedef struct SpikeData
{
  String addr;
  int temp;
  int light;
  int CMS;
  int RMS;
}SpikeData;

SpikeData spikeData[3]; //max of three spikes

// From https://github.com/andrewrapp/xbee-arduino/blob/master/examples/RemoteAtCommand/RemoteAtCommand.pde

XBee xbee = XBee();

uint8_t sampleCmd[] = {'I', 'S'};
uint8_t dio[4][2] =  {{'D', '4'},
                      {'D', '5'},
                      {'P', '1'},
                      {'P', '2'}};

uint8_t onCmd[] = {0x05};
uint8_t offCmd[] = {0x04};

// SH + SL of your remote radio
XBeeAddress64 remoteAddress = XBeeAddress64(0x00000000, 0x0000FFFF); //broadcast
// Create a remote AT request with the IR command
RemoteAtCommandRequest atRequest = RemoteAtCommandRequest(remoteAddress, sampleCmd, 0x0, 0);

// Create a Remote AT response object
RemoteAtCommandResponse remoteAtResponse = RemoteAtCommandResponse();



volatile unsigned long next;

// which pin to use for reading the sensor? can use any pin!
#define FLOWSENSORPIN 5

// count how many pulses!
volatile uint16_t pulses = 0;

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

bool getUpdatesFromServer ()
{
  //ask server for offsets
  HTTPClient http;
  http.get ("http://192.168.0.11:8080/?update=1");
  //dummy val
  waterDuration[0] = 0;
  return true;
}

bool sendWaterUsage ()
{
  //Serial.println(pulses);
  //one way update
  if (WiFi.status() == WL_CONNECTED) { //Check WiFi connection status
 
    StaticJsonBuffer<300> JSONbuffer;   //Declaring static JSON buffer
    JsonObject& JSONencoder = JSONbuffer.createObject(); 
 
    JSONencoder["waterUsed"] = pulses;
 
    char JSONmessageBuffer[300];
    JSONencoder.prettyPrintTo(JSONmessageBuffer, sizeof(JSONmessageBuffer));
    //Serial.println(JSONmessageBuffer);
 
    HTTPClient http;    //Declare object of class HTTPClient
    http.begin("http://192.168.0.11:8080/");      //Specify request destination
    http.addHeader("Content-Type", "application/json");  //Specify content-type header
  
    int httpCode = http.POST(JSONmessageBuffer);   //Send the request
    String payload = http.getString();          //Get the response payload
  
    //Serial.println(httpCode);   //Print HTTP return code
    //Serial.println(payload);    //Print request response payload
  
    http.end();  //Close connection
  }
  else
  {

    Serial.println ("Not connected!");
  }

  
  return true;
}

bool sendSensorUpdates ()
{
  if (WiFi.status() == WL_CONNECTED) { //Check WiFi connection status
 
    StaticJsonBuffer<300> JSONbuffer;   //Declaring static JSON buffer
    JsonObject& JSONencoder = JSONbuffer.createObject(); 
    HTTPClient http;
    //Declare object of class HTTPClient
    http.begin("http://192.168.0.11:8080/");      //Specify request destination
    http.addHeader("Content-Type", "application/json");  //Specify content-type header
    
    for (int i = 0; i < 3; i++)
    {
      JSONencoder["spikeID"] = spikeData[i].addr;
      JSONencoder["temp"] = spikeData[i].temp;
      JSONencoder["CMS"] = spikeData[i].CMS;
      JSONencoder["RMS"] =  spikeData[i].RMS;
      JSONencoder["light"] = spikeData[i].light;
   
      char JSONmessageBuffer[300];
      JSONencoder.prettyPrintTo(JSONmessageBuffer, sizeof(JSONmessageBuffer));
      //Serial.println(JSONmessageBuffer);
   
          
      int httpCode = http.POST(JSONmessageBuffer);   //Send the request
      String payload = http.getString();          //Get the response payload
    }
  
    //Serial.println(httpCode);   //Print HTTP return code
    //Serial.println(payload);    //Print request response payload
  
    http.end();  //Close connection
  } else {
 
    Serial.println("Error in WiFi connection");
 
  }
  return true;
}

bool getSensorUpdates ()
{
  //Initialize
  for (int i = 0; i < 3; i++)
  {
    spikeData[i].addr = "000000000000";
    spikeData[i].temp = 0;
    spikeData[i].light = 0;
    spikeData[i].CMS = 0;
    spikeData[i].RMS = 0;
    
  }
  
  //send broadcast request for data and parse response

  // Turn the sensors on
  for (int i = 0; i < 4; i++)
  {
    atRequest.setCommand(dio[i]);
    atRequest.setCommandValue (onCmd);
    atRequest.setCommandValueLength (sizeof(onCmd));
    sendRequest (false);
    atRequest.clearCommandValue();
  }

  // send sample request
  atRequest.setCommand(sampleCmd);
  atRequest.setCommandValue (0x0);
  atRequest.setCommandValueLength (0);
  sendRequest (true);
  atRequest.clearCommandValue();

  // Turn the sensors offf
  for (int i = 0; i < 4; i++)
  {
    atRequest.setCommand(dio[i]);
    atRequest.setCommandValue (offCmd);
    atRequest.setCommandValueLength (sizeof(offCmd));
    sendRequest (false);
    atRequest.clearCommandValue();
  }

    
  return true;
}

void sendRequest(bool sampleResponse)
{
  ZBRxIoSampleResponse ioSample = ZBRxIoSampleResponse();
  uint16_t sample;
  int count;
  uint64_t addr;
  xbee.send(atRequest);
  int spikeCount = 0;
  
  while (xbee.readPacket(5000))
  {
     // should be an AT command response
    if (xbee.getResponse().getApiId() == REMOTE_AT_COMMAND_RESPONSE) 
    {
      xbee.getResponse().getRemoteAtCommandResponse(remoteAtResponse);

      if (remoteAtResponse.isOk()) 
      {
        if (remoteAtResponse.getValueLength() > 0 && sampleResponse) 
        { 
//          xbee.remoteAtResponse.getZBRxIoSampleResponse(ioSample);
          addr = remoteAtResponse.getRemoteAddress64().get();
          spikeData[spikeCount].addr = ToString (addr); //change to string for sending to server
          count = 0;

//          spikeData[spikeCount].RMS = ioSample.getAnalog(0);
//          spikeData[spikeCount].CMS = ioSample.getAnalog(1);
//          spikeData[spikeCount].temp = ioSample.getAnalog(2);
//          spikeData[spikeCount].light = ioSample.getAnalog(3);
         
          //samples don't start until the fifth byte    
          for (int i = remoteAtResponse.getValueLength() - 1; i > remoteAtResponse.getValueLength() - 8; i-=2) 
          {
            sample = remoteAtResponse.getValue()[i-1];
            sample <<= 4;
            sample |= remoteAtResponse.getValue()[i];

            if (count == 0)
            {
              spikeData[spikeCount].light = sample;
            }
            else if (count == 2)
            {
              spikeData[spikeCount].temp = sample; 
            }
            else if (count == 4)
            {
              spikeData[spikeCount].CMS = sample; 
            }
            else if (count == 6)
            {
              spikeData[spikeCount].RMS = sample; 
            }
            count += 2;
          }

          spikeCount++;

        
        }
      }
    }
    
  }
}

//from: https://forum.arduino.cc/index.php?topic=378359.0
String ToString(uint64_t x)
{
     boolean flag = false; // For preventing string return like this 0000123, with a lot of zeros in front.
     String str = "";      // Start with an empty string.
     uint64_t y = 10000000000000000000;
     int res;
     if (x == 0)  // if x = 0 and this is not testet, then function return a empty string.
     {
           str = "0";
           return str;  // or return "0";
     }    
     while (y > 0)
     {                
            res = (int)(x / y);
            if (res > 0)  // Wait for res > 0, then start adding to string.
                flag = true;
            if (flag == true)
                str = str + String(res);
            x = x - (y * (uint64_t)res);  // Subtract res times * y from x
            y = y / 10;                   // Reducer y with 10    
     }
     return str;
}

// From: https://github.com/esp8266/Arduino/issues/644

void wifiOn()
{
  WiFi.forceSleepWake();
  WiFi.mode(WIFI_STA);  
  connect();
  //WiFi.begin(ssid, password);
}

void wifiOff ()
{
  WiFi.disconnect(); 
  WiFi.mode(WIFI_OFF);
  WiFi.forceSleepBegin();
  delay(1);
}

//defined per: https://github.com/esp8266/Arduino/issues/2284
void ICACHE_RAM_ATTR simpleCount ()
{
  pulses++;
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
  Serial.begin(9600);
  xbee.begin(Serial);
  delay(5000); //Let the Xbee turn on!
  getSensorUpdates (); //talk to Spikes to get sensor data
  connect (); // connect to the WiFi!
  sendSensorUpdates ();
  getUpdatesFromServer(); // set waterDuration[] array from server response

  if (waterDuration[0] != 0 || waterDuration[1] != 0 || waterDuration[2] != 0)
  {
    //Serial.println ("watering!");
    //turn off the WiFi radio to save power!
    wifiOff();
    
    for (int i = 0; i < 3; i++)
    {
      pinMode(valvePin[i], OUTPUT);
    }

    wateringTimeStart = millis();

    pinMode (FLOWSENSORPIN, INPUT_PULLUP);
    attachInterrupt (FLOWSENSORPIN, simpleCount, CHANGE);
  }
  else
  {
    // go back to deep sleep
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
    //Serial.println("done watering!");
    wifiOn (); //back on so we can send data
    sendWaterUsage ();
    //deep sleep
    ESP.deepSleep (sleepDuration, WAKE_RF_DEFAULT);
  }
  yield ();  // yield the proc!
 }


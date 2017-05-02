# gardenGROW
Garden GROW is a system for monitoring automatically watering a garden. GROW stands for Gadgets for Remote Observation and Watering. The system consists of a base station and up to three spikes. The base station consists of an ESP8266 Huzzah, XBee, three solenoid water valves, a liquid flow meter, and a set of solar panels with a simple LM317 charge controller. The software for the base station is included here. It relies on the Adafruit JSON library (for communcation with the back-end), the Adafruit ESP8266 Huzzah library, and an Arduino XBee library. The base station relies on the back-end for timing information (watering durations and sleep time) and passes information collected from the garden spikes over the XBee radio to the back-end.

The rest of the software is for the back-end / GUI. The GUI is built using PyQt4 with plots provided by PyQtGraph. The server is based off of a Simple HTTP server. 

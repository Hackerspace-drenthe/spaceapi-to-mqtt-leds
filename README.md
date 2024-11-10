# spaceapi-to-mqtt-leds
Monitor HackerSpace Status API and publish led colours to MQTT

Gets space state from https://api.spaceapi.io

Itterates through the JSON array of dictionaries to find the 'valid' entries.
For each valid entry, see if we have the 'space' name in our LED map.
If yes, set LED to green=open, red=closed. 

Publish to our MQTT server as kaart/emmen 

The actual LEDs are then set using the generic MQTT to WS2812 LED on an ESP32. 

Source code for the MQTT listener at https://github.com/Hackerspace-drenthe/esp32-mqtt-ws2812b-driver


## Requires:
 `pip install paho-mqtt` 

## Running:

Run once:
 `python3 main.py` 
 
or in a 30 second loop:
 `./run.sh`


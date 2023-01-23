# Pico Temperature Probe

## Overview 
A small Raspberry Pico W script to measure the temperature and send it to a web server for logging.  For under $10 you can have a temperature monitor that sends the temperature reading to a server periodically.  I've tried to make it robust enough to carry on even when there are errors.

## Needed:
- Raspberry Pi Pico W
- A DS18B20 Onewire temperature probe.  I got a ten pack from amazon (https://www.amazon.ca/gp/product/B0714588F8/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1) which are nicely sealed
- A 4.7K to 10K resistor
- some sort of web server to log the results

## Instructions:
- The script temperature.py needs to be uploaded to your Pico and named main.py so it will automatically run.
- Adjust the SSID and wifi password in the script to match your network
- change the urequests.get line to point to your own web server
- connect the red wire to the Pico 3.3V (Pin 36)
- connect the black wire to a Pico Ground (eg. Pin 38)
- connect the yellow data wire to the Pico GPIO 0 (Pin 1)
- connect the resistor between the red and yellow wires

## Notes:
- The light on the Pico will blink once per second until it connects with the wifi, and then it will give three quick blicks.
- Once every 10 seconds or so it will measure the temperature and attempt to make a web call to report it.
- The script tries to recover from errors and reset itself completely if it loses the network.
- By default it logs to a file temperature.log on the flash memory of the Pico, this can be disabled , but is good for initial debugging.
- web calls look like:  http://10.1.1.80/sensors/temperature/2903514757998460000/15.34  with "2903514757998460000" the serial number of the probe and 15.34 the temperature in celcius.

Feel free to contact me with questions, comments or improvement at jim@mintha.com

![probe1](https://user-images.githubusercontent.com/47866187/213978473-26d448cd-3166-4a0b-b2fb-05700b4b94a3.jpg)
![probe2](https://user-images.githubusercontent.com/47866187/213978478-fb6e1810-b1aa-489b-9c87-668cc162c8e3.jpg)

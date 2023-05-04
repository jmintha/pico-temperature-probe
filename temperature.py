from machine import Pin, reset
import utime
import onewire
import ds18x20
import network
import urequests
import os

def blink(count, length):
    led = Pin("LED", Pin.OUT)

    for _ in range(count):
        led.value(1)
        utime.sleep_ms(length)
        led.value(0)
        utime.sleep_ms(length)


def connect_wifi():
    ssid = 'HOME20'
    password = 'wifipassword'

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)


    # Wait for connect or fail
    max_wait = 100
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1
        print('waiting for connection...')
        blink(1, 500)

    # Handle connection error
    if wlan.status() != 3:
        print('network connection failed')
        return False

    status = wlan.ifconfig()
    print('connected with ip: ' + status[0])
    blink(4, 100)
    return True


def read_temperature():

    ds_pin = Pin(0)
    ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))
    roms = ds_sensor.scan()

    # print out probes found for information
    for rom in roms:
        serial = int.from_bytes(rom, "big")
        print("Probe: %d" % serial)

    # loop forever getting temperatures
    ctr = 90
    while True:
        try:
            ds_sensor.convert_temp()
        except Exception as err:
            print("Error converting temperature: %s" % err)
            return

        # wait for it to be ready
        utime.sleep_ms(750)
        ctr += 1

        # for each probe send the temperature to server
        for rom in roms:
            location = "%d" % int.from_bytes(rom, "big")
            try:
                temperature = ds_sensor.read_temp(rom)
            except Exception as err:
                print("Error reading temperature: %s" % err)
                return

            # only print output once an hour
            if ctr > 360:
                print("Temp for %s: %3.2f" % (location, temperature))
                ctr = 0

            # send it to the server
            response = None
            try:
                response = urequests.get("http://10.1.1.80/sensors/temperature/%s/%3.2f/" % (location, temperature), timeout=1.0)
                response.close()
            except Exception as err:
                if getattr(response, 'close', None):
                    response.close()
                print("unable to upload temperature: %s" % err)
                return

            # flash the light for info
            blink(1, 250)
            utime.sleep(10)


def do_reset(logfile):

    # reset the pico
    print("doing full reset")
    logfile.close()
    reset()


def main():

    # open log file
    logfile = open("temperature.log", "a")
    os.dupterm(logfile)

    bad_count = 0
    while True:

        # first connect (reconnect) to wifi
        success = False
        for _ in range(0, 4):
            rtn = connect_wifi()
            if rtn:
                success = True
                break
            utime.sleep(60)
            print("Unable to connect to wifi, retrying")

        # give up and reset everything
        if not success:
            do_reset(logfile)

        # start reading temperature
        read_temperature()

        # something went wrong, loop
        bad_count += 1
        utime.sleep(30)

        # too many bad, do reset
        if bad_count > 30:
            do_reset(logfile)


if __name__ == '__main__':
    main()

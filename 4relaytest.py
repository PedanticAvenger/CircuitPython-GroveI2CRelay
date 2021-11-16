#!/usr/bin/python

import sys
import time

from grove_i2c_relay import Relay


def process_loop():

    # now cycle each relay every second in an infinite loop
    while True:
        relay.channel_on(1)
        time.sleep(1)
        relay.channel_off(1)
        time.sleep(1)
        relay.channel_on(2)
        time.sleep(1)
        relay.channel_off(2)
        time.sleep(1)
        relay.channel_on(3)
        time.sleep(1)
        relay.channel_off(3)
        time.sleep(1)
        relay.channel_on(4)
        time.sleep(1)
        relay.channel_off(4)
        time.sleep(1)
        relay.channel_on(1)
        relay.channel_on(3)
        time.sleep(1)
        relay.channel_off(1)
        relay.channel_off(3)
        time.sleep(1)
        relay.channel_on(2)
        relay.channel_on(4)
        time.sleep(1)
        relay.channel_off(2)
        relay.channel_off(4)
        time.sleep(1)


# Now see what we're supposed to do next
if __name__ == "__main__":
    # Create the relay object
    relay = Relay(debug_action=True)
    relay.print_status_all()

    try:
        relay.all_channel_on()
        time.sleep(1)
        relay.all_channel_off()
        time.sleep(1)
        process_loop()
    except KeyboardInterrupt:
        print("\nExiting application")
        # turn off all of the relays
        relay.all_channel_off()
        # exit the application
        sys.exit(0)

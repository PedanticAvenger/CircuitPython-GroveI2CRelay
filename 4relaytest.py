#!/usr/bin/python
'''*****************************************************************************************************************
    Seeed Studio Relay Board Library V2
    Test Application #1
    By John M. Wargo (https://www.johnwargo.com)
********************************************************************************************************************'''

import sys
import time

from grove_i2c_relay import Relay


def process_loop():

    # now cycle each relay every second in an infinite loop
    while True:
        relay.on(2)
        relay.print_status_all()
        time.sleep(2)
        relay.off(2)
        relay.print_status_all()
        time.sleep(2)


# Now see what we're supposed to do next
if __name__ == "__main__":
    # Create the relay object
    relay = Relay(debug_action=True)
    relay.print_status_all()

    try:
        process_loop()
    except KeyboardInterrupt:
        print("\nExiting application")
        # turn off all of the relays
        relay.all_off()
        # exit the application
        sys.exit(0)


#!/usr/bin/python

import sys
import time

from grove_i2c_relay import Relay


# Now see what we're supposed to do next
if __name__ == "__main__":
    # Create the relay object
    relay = Relay(debug_action=False)

    try:
        version = relay.getFirmwareVersion()
        v2 = version.hex()
        print("\nVersion: {}".format(v2))

    except KeyboardInterrupt:
        print("\nExiting application")
        # turn off all of the relays
        relay.all_off()
        # exit the application
        sys.exit(0)

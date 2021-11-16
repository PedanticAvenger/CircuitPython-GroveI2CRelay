# Seeed Studio Relay Board

Working on a CircuitPython based system for a meat dry curing chamber and I wanted to leverage I2C devices in the build as much as possible.  Discovered that there were no modules available to support this hardware in CircuitPython, or Python at all.  Found [Seeed Studio Relay V2](https://github.com/johnwargo/seeed-studio-relay-v2) which is functionally what I needed but didn't leverage CircuitPython calls, and it was for a different board which behaves differently.  The hardware I'm using to base my work/testing on is not the Raspberry Pi Relay board as @johnwargo used but instead the https://wiki.seeedstudio.com/Grove-4-Channel_SPDT_Relay/ which has functional differences.  This repository is a circuitpython rewrite based off @johnwargo repo and the SEEED Arduino repo.  

> **Note:** I am CircuitPython novice so this module will be functional for my purposes but may have issues and I'm more than willing to accept PRs and/or hand this over to more capable hands if ongoing support for it is deemed appropriate.

In the repository, you'll find three files:

+	`grove_i2c_relay.py` - A CircuitPython module that exposes several functions you can use in your own applications to control the relay board. The module is covered in the next section.
+	`4relaytesttest.py` - This is a sample CircuitPython application to exercise the 4 channel module and validate that everything works.
+   `getversion.py` - Small script to get the firmware version of the board mostly to verify comms are working.

## Using the CircuitPython Module

To use the module in your ownCircuitPython applications, copy the module (`relay_lib_seeed_cp.py`) into your project folder, then import the module in your CircuitPython application by adding the following line to the beginning of your application:

	import grove_i2c_relay

This exposes a series of object functions to your application:

+	`channel_on(int_value)` - Turns a single relay on. Pass an integer value between `1` and `4` (inclusive) to the function to specify the relay you wish to turn on. For example: `relay_on(1)` will turn the first relay (which is actually relay `0` internally) on.
+	`channel_off(int_value)` - Turns a single relay on. Pass an integer value between 1 and 4 (inclusive) to the function to specify the relay you wish to turn on. For example: `relay_on(4)` will turn the first relay (which is actually relay `3` internally) off.
+	`all_channel_on()` - Turns all of the relays on simultaneously.    
+	`all_channel_off()` - Turns all of the relays off simultaneously.
+	`toggle_channel(int_value)` - Toggles the status of the specified relay. 0 -> 1, 1 -> 0
+	`get_channel_status` - Returns a Boolean value indicating the status of the specified relay. `True` if the relay is on, `false` if the relay is off. This function was added to enable the capabilities of the `toggle_channel` function described previously.
+	`print_channel_status(int_value)` - Prints out a formatted line with "Relay X On" or "Relay X Off"
+	`print_channel_status_all` - Prints out a formatted line with status of all the relays displayed. e.g.  
"| 1: On  | 2: Off | 3: Off | 4: On  |" for a 4 relay module 
+   `get_firmware_version` - returns a byte value to display the version of the firmware installed on the board, included for development troubleshooting.

Bit Values for control of relays.

       1   2   3   4
       ---------------
0x00:  OFF OFF OFF OFF
0x01:  ON  OFF OFF OFF
0x02:  OFF ON  OFF OFF
0x03:  ON  ON  OFF OFF
0x04:  OFF OFF ON  OFF
0x05:  ON  OFF ON  OFF
0x06:  OFF ON  ON  OFF
0x07:  ON  ON  ON  OFF
0x08:  OFF OFF OFF ON
0x09:  ON  OFF OFF ON
0x0a:  OFF ON  OFF ON
0x0b:  ON  ON  OFF ON
0x0c:  OFF OFF ON  ON
0x0d:  ON  OFF ON  ON
0x0e:  OFF ON  ON  ON
0x0f:  ON  ON  ON  ON

The module has a couple configuration Values you will want to keep track of:

	DEVICE_ADDRESS = 0x11
    NUM_RELAY_PORTS = X   Where X should be either 4 or 8  

The board defaults to 0x11 address, but you can change the address of the board through software, you will need to update this variable accordingly if you do. I haven't incorporated those functions into this module yet as that is a job for after this all works properly.

To see the module in action, open a terminal window on the Raspberry Pi, navigate to the folder where you extracted this repository's files, and execute the following command:

	python ./relay_lib_seeed_test_cp.py

The application will:

+	Turn all of the relays on for a second
+	Turn all of the relays off
+	Cycle through each of the relays (1 through 4) turning each on for a second

LEDs on the relay board (one for each relay) will illuminate when the relays come one. On my board, they weren't in sequence, so don't expect them to light in order.

***

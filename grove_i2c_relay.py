# =========================================================
# Seeed Studio Grove - 4/8-Channel I2C SPDT/SSR Relay Board
# CircuitPython Module
#
# by Raymond Richmond
#
# Modified from code by John M. Wargo (https://github.com/johnwargo/seeed-studio-relay-v2)
# to support CircuitPython and this specific relay board family.
# =========================================================
CMD_READ_FIRMWARE_VER = 0x13
CMD_CHANNEL_CONTROL = 0x10
CMD_SAVE_I2C_ADDR = 0x11
CMD_READ_I2C_ADDR = 0x12
CMD_READ_FIRMWARE_VER = 0x13
CHANNEL_BIT = {
    "1": 0b00000001,
    "2": 0b00000010,
    "3": 0b00000100,
    "4": 0b00001000,
    "5": 0b00010000,
    "6": 0b00100000,
    "7": 0b01000000,
    "8": 0b10000000,
}


class Relay:
    def __init__(
        self,
        device_address=0x11,
        num_relays=4,
        SCL=None,
        SDA=None,
        debug_action=False,
    ):
        import board
        import busio

        self.DEVICE_ADDRESS = device_address
        self.NUM_RELAY_PORTS = num_relays  # 4 or 8 are really the only allowed numbers
        self.channel_state = 0

        print("Initializing relay board at 0x{:x}".format(device_address))

        if SCL is None:
            SCL = board.D5  # Set this based on board pins, defined in Adafruit board.

        if SDA is None:
            SDA = board.D3  # Set this based on board pins, defined in Adafruit board.

        self.i2c = busio.I2C(SCL, SDA)

        if debug_action:
            print("Enabling action_output mode")

        while not self.i2c.try_lock():
            pass
        try:
            self.i2c.writeto(
                self.DEVICE_ADDRESS,
                bytes(CMD_CHANNEL_CONTROL + self.channel_state),
            )

        finally:
            self.i2c.unlock()
        self.debug = debug_action

    def channel_on(self, relay_num):
        if isinstance(relay_num, int):  # Check that not getting garbage
            if 0 < relay_num <= self.NUM_RELAY_PORTS:  # check for valid relay number
                if self.debug:
                    print("Turning relay {} on".format(relay_num))
                self.channel_state |= 1 << (relay_num - 1)
                print("Current Channel State: {0:8b}".format(self.channel_state))
                while not self.i2c.try_lock():
                    pass
                try:
                    self.i2c.writeto(
                        self.DEVICE_ADDRESS,
                        bytes(CMD_CHANNEL_CONTROL + self.channel_state),
                    )
                    if self.debug:
                        print("Sent {:x}".format(self.DEVICE_ADDRESS))
                        print("Sent {:b}".format(self.channel_state))
                finally:
                    self.i2c.unlock()
            else:
                print("Invalid relay: #{}".format(relay_num))
        else:
            print("Relay number must be an Integer value")

    def channel_off(self, relay_num):
        if isinstance(relay_num, int):  # Check that not getting garbage
            if 0 < relay_num <= self.NUM_RELAY_PORTS:  # check for valid relay number
                if self.debug:
                    print("Turning relay {} off".format(relay_num))
                self.channel_state &= ~(1 << (relay_num - 1))
                print("Current Channel State: {0:8b}".format(self.channel_state))
                while not self.i2c.try_lock():
                    pass
                try:
                    self.i2c.writeto(
                        self.DEVICE_ADDRESS,
                        bytes(CMD_CHANNEL_CONTROL + self.channel_state),
                    )
                    if self.debug:
                        print("Sent {:x}".format(self.DEVICE_ADDRESS))
                        print("Sent {:b}".format(self.channel_state))

                finally:
                    self.i2c.unlock()
            else:
                print("Invalid relay: #{}".format(relay_num))
        else:
            print("Relay number must be an Integer value")

    def all_channel_on(self):
        if self.debug:
            print("Turning all relays ON")
        self.channel_state |= 0xF << 0
        while not self.i2c.try_lock():
            pass
        try:
            self.i2c.writeto(
                self.DEVICE_ADDRESS,
                bytes(CMD_CHANNEL_CONTROL + self.channel_state),
            )

        finally:
            self.i2c.unlock()

    def all_channel_off(self):
        if self.debug:
            print("Turning all relays OFF")
        self.channel_state &= ~(0xF << 0)
        while not self.i2c.try_lock():
            pass
        try:
            self.i2c.writeto(
                self.DEVICE_ADDRESS,
                bytes(CMD_CHANNEL_CONTROL + self.channel_state),
            )

        finally:
            self.i2c.unlock()

    def toggle_channel(self, relay_num):
        if self.debug:
            print("Toggling relay:", relay_num)
        if self.get_port_status(relay_num):
            # it's on, so turn it off
            self.channel_off(relay_num)
        else:
            # it's off, so turn it on
            self.channel_on(relay_num)

    def get_channel_status(self, relay_num):
        output = str(relay_num)
        status = self.channel_state
        status = bin(int(status))
        status >> bin(CHANNEL_BIT[output]) & 1
        return status

    def print_channel_status(self, relay_num):
        output = str(relay_num)
        status = self.channel_state
        if status & CHANNEL_BIT[output] > 0:
            output += ": On  "
        else:
            output += ": Off "
        print("Relay {}".format(relay_num, output))

    def print_status_all(self):
        output = "| "
        for x in range(1, self.NUM_RELAY_PORTS + 1):
            status = self.channel_state
            output += str(x)
            if status & CHANNEL_BIT[str(x)] > 0:
                output += ": On  | "
            else:
                output += ": Off | "
        print("Relay status: {}".format(output))

    def get_firmware_version(self):
        while not self.i2c.try_lock():
            pass
        try:
            self.i2c.writeto(
                self.DEVICE_ADDRESS,
                bytes(CMD_READ_FIRMWARE_VER),
                stop=False,
            )
            buffer = bytearray(1)
            self.i2c.readfrom_into(self.DEVICE_ADDRESS, buffer)
            # return the specified version
            return buffer

        finally:
            self.i2c.unlock()

from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService
import board
import digitalio
import neopixel
import random
import time


from adafruit_bluefruit_connect.packet import Packet
from adafruit_bluefruit_connect.button_packet import ButtonPacket
from adafruit_bluefruit_connect.color_packet import ColorPacket

ble = BLERadio()
ble.name = "VINCENT"
uart = UARTService()
uart_service = UARTService()
advertisement = ProvideServicesAdvertisement(uart)
led = digitalio.DigitalInOut(board.RED_LED)
led.direction = digitalio.Direction.OUTPUT
pixel = neopixel.NeoPixel(board.NEOPIXEL,1,brightness=.25)
pixel2 = neopixel.NeoPixel(board.D5,300,brightness=.25)
current_color = (0,0,0)
pixel.fill(current_color)

while True:
    ble.start_advertising(advertisement)
    while not ble.connected:
        pass

    # Now we're connected

    while ble.connected:
        if uart.in_waiting:
            packet = Packet.from_stream(uart)
            if isinstance(packet, ButtonPacket):
                if packet.pressed:
                    if packet.button == ButtonPacket.BUTTON_1:
                        # The 1 button was pressed.
                        pixel[0] = (255,0,0)
                        print("LED RED")
                    elif packet.button == ButtonPacket.BUTTON_2:
                        # The 2 button was pressed.
                        pixel[0] = (0,255,0)
                        print("LED GREEN")
                    elif packet.button == ButtonPacket.BUTTON_3:
                        # The 3 button was pressed.
                        pixel[0] = (0,0,255)
                        print("LED BLUE")
                    elif packet.button == ButtonPacket.BUTTON_4:
                        # The 4 button was pressed.
                        for i in range(10000):
                            for i in range(239):
                                if (i % 2) == 0:
                                    pixel2[i] = (255,97,0)
                                if (i % 2) == 1:
                                    pixel2[i] = (75,0,127)

                            time.sleep(1)

                            for i in range(239,0,-1):
                                if (i % 2) == 0:
                                    pixel2[i] = (75,0,127)
                                if (i % 2) == 1:
                                    pixel2[i] = (255,97,21)

                            time.sleep(1)
                        print("HAPPY HALLOWEEN")
                    elif packet.button == ButtonPacket.UP:
                        # The UP button was pressed.
                        sum = 0
                        for i in range(239):
                            sum = i
                            if (sum % 2) == 0:
                                pixel2[sum] = (0,255,0)
                            if (sum % 2) == 1:
                                pixel2[sum] = (255,0,0)

                    elif packet.button == ButtonPacket.DOWN:
                        # The DOWN button was pressed.
                        for i in range(10000):
                            for i in range(239):
                                if (i % 2) == 0:
                                    pixel2[i] = (0,255,0)
                                if (i % 2) == 1:
                                    pixel2[i] = (255,0,0)

                            time.sleep(1)

                            for i in range(200,0,-1):
                                if (i % 2) == 0:
                                    pixel2[i] = (255,0,0)
                                if (i % 2) == 1:
                                    pixel2[i] = (0,255,0)

                            time.sleep(1)
                    elif packet.button == ButtonPacket.LEFT:
                        # The LEFT button was pressed.
                        sum = 0
                        for i in range(200):
                            sum = i
                            pixel2[sum] = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
                    elif packet.button == ButtonPacket.RIGHT:
                        # The RIGHT button was pressed.
                        for i in range(1000):
                            r = random.randint(0,255)
                            pixel.fill(r)
                            pixel2.fill(r)
                            time.sleep(1)

            if isinstance(packet, ColorPacket):
                print(packet.color)
                pixel.fill(packet.color)
                pixel2.fill(packet.color)
                pixel2[1] = (0,255,0)

# If we got here, we lost the connection. Go up to the top and start
# advertising again and waiting for a connection.
# Write your code here :-)

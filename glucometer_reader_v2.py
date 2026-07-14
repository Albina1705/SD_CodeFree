#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import serial
import time

PORT = "COM4"
BAUD = 38400

CHALLENGE = bytes.fromhex("53 20 04 10 30 20 AA")
RESPONSE  = bytes.fromhex("53 10 04 10 40 50 AA")
FETCH     = bytes.fromhex("53 10 04 10 60 70 AA")


def wait_packet(ser, timeout=2.0):
    start = time.time()
    buf = bytearray()

    while time.time() - start < timeout:

        if ser.in_waiting:
            buf.extend(ser.read(ser.in_waiting))

            if len(buf) >= 4:
                length = buf[2]
                total = 3 + length

                if len(buf) >= total:
                    pkt = bytes(buf[:total])
                    return pkt

        time.sleep(0.001)

    return None


def decode_reading(pkt):

    msg = pkt[3:-2]

    # Structură determinată experimental
    # msg[0] = tip (0x20)
    # msg[1] = status
    # msg[2] = an (00..99)
    # msg[3] = lună
    # msg[4] = zi
    # msg[5] = oră
    # msg[6] = minut
    # msg[7:9] = glicemie (big-endian)

    year   = 2000 + msg[2]
    month  = msg[3]
    day    = msg[4]
    hour   = msg[5]
    minute = msg[6]

    value = (msg[7] << 8) | msg[8]

    meal = msg[13]

    if meal == 0x10:
        meal_txt = "Before meal"
    elif meal == 0x20:
        meal_txt = "After meal"
    else:
        meal_txt = "-"

    print(f"{year:04d}-{month:02d}-{day:02d} "
          f"{hour:02d}:{minute:02d}   "
          f"{value:3d} mg/dL   {meal_txt}")

ser = serial.Serial(
    PORT,
    BAUD,
    bytesize=8,
    parity='N',
    stopbits=1,
    timeout=0.02
)

print()
print("Waiting for glucometer...")

buffer = bytearray()

while True:

    if ser.in_waiting:

        data = ser.read(ser.in_waiting)

        print("RX:", data.hex(" ").upper())

        buffer.extend(data)

        if CHALLENGE in buffer:
            break

    time.sleep(0.001)

print()
print("Handshake...")

ser.write(RESPONSE)
ser.flush()

pkt = wait_packet(ser)

if pkt is None:
    print("No count packet")
    quit()

print()
print("COUNT:", pkt.hex(" ").upper())

msg = pkt[3:-2]

count = (msg[1] << 8) | msg[2]

print()
print("Readings:", count)
print()

for i in range(count):

    ser.write(FETCH)
    ser.flush()

    pkt = wait_packet(ser)

    if pkt is None:
        print("Timeout")
        break

    print(pkt.hex(" ").upper())

    if pkt[2] == 0x13:
        decode_reading(pkt)

print()
print("Finished.")

ser.close()
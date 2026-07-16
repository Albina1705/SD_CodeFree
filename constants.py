BAUDRATE = 38400

ETX = 0xAA

HANDSHAKE_REQUEST = bytes.fromhex("53 20 04")
HANDSHAKE_REPLY   = bytes.fromhex("53 10 04 10 40 50 AA")

COUNT_PACKET      = bytes.fromhex("53 20 18")

REQUEST_RECORD    = bytes.fromhex("53 10 04 10 60 70 AA")
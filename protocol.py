import serial
import time

from serial.tools import list_ports
from serial_utils import find_serial_port

from constants import *
from decoder import decode_record

from protocol_analysis import debug_checksum

class SDCodefreeProtocol:

    def __init__(self,
                port=None,
                baudrate=38400,
                debug=False,
                analyze_protocol=False):

        self.port = port
        self.baudrate = baudrate
        self.debug = debug
        self.analyze_protocol = analyze_protocol
        self.ser = None

    def find_port(self):

        ports = list(list_ports.comports())

        if self.debug:
            print("Porturi găsite:")

            for p in ports:
                print(f"  {p.device}  {p.description}")

        if len(ports) == 0:
            raise RuntimeError("Nu există niciun port serial.")
            raise RuntimeError("Nu am găsit adaptorul USB-Serial.")

        if len(ports) == 1:
            return ports[0].device

        for p in ports:

            d = p.description.upper()

            if (
                "CP210" in d or
                "SILICON LABS" in d or
                "FT232" in d or
                "FTDI" in d or
                "CH340" in d or
                "CH910" in d or
                "USB SERIAL" in d
            ):
                return p.device

        raise Exception("Nu am găsit adaptorul USB-Serial.")    

    def connect(self):
        if self.port is None:
            self.port = self.find_port()

        if self.port is None:
            raise RuntimeError("Nu a fost găsit niciun adaptor USB-Serial.")

        

        self.ser = serial.Serial(
            port=self.port,
            baudrate=self.baudrate,
            bytesize=8,
            parity="N",
            stopbits=1,
            timeout=0.05,
        )
       
        self.ser.reset_input_buffer()
        self.ser.reset_output_buffer()
        

    def disconnect(self):
        if self.ser and self.ser.is_open:
            self.ser.close()

    def send_packet(self, packet):
        if self.debug:
            print("TX :", packet.hex(" ").upper())
        self.ser.write(packet)
        self.ser.flush()

    def validate_packet(self, packet: bytes) -> bool:
        if len(packet) < 7:
            print("Pachet prea scurt")
            return False

        if packet[0] != 0x53:
            print("Header invalid")
            return False

        if packet[-1] != 0xAA:
            print("Footer invalid")
            return False

        return True

    def read_packet(self):
        packet = bytearray()
        start = time.time()
        last_data = start

        while True:
            if self.ser.in_waiting:
                packet.extend(self.ser.read(self.ser.in_waiting))
                last_data = time.time()

            # S-a primit ceva și apoi 50 ms liniște
            if packet and (time.time() - last_data) > 0.05:
                break

            # Nu s-a primit nimic timp de 2 secunde
            if not packet and (time.time() - start) > 2:
                print("Timeout")
                break

            time.sleep(0.002)

        packet = bytes(packet)

        # Unele adaptoare USB-UART emit un 0x00 la conectare. Îl ignorăm.
        if packet == b"\x00":
            return b""

        if self.debug and packet:
            print("RX :", packet.hex(" ").upper())

        # Verificăm dacă pachetul este valid
        if not self.validate_packet(packet):
            return b""
        
        if self.analyze_protocol:
            debug_checksum(packet)

        return packet

    def wait_handshake(self):
        print("Aștept pornirea glucometrului...")
        while True:
            packet = self.read_packet()
            if not packet:
                continue
            if packet.startswith(HANDSHAKE_REQUEST):
                return packet

    def send_handshake(self):
        self.send_packet(HANDSHAKE_REPLY)

    def read_count(self):
        print("Aștept pachetul COUNT...")
        time.sleep(0.2)  # <-- doar pentru test

        packet = self.read_packet()
        print("Pachet brut:", packet.hex(" ").upper())

        if packet.startswith(COUNT_PACKET):
            count = (packet[4] << 8) | packet[5]
            return count

        return 0

    def request_record(self):
        self.send_packet(REQUEST_RECORD)
        return self.read_packet()

    

    def download_all(self):

        self.wait_handshake()
        print("Handshake primit!")

        self.send_handshake()
        print("Handshake trimis!")

        count = self.read_count()
        print(f"Memorie: {count} înregistrări")

        readings = []

        for i in range(count):
            print(f"\n=== Înregistrarea {i+1}/{count} ===")

            packet = self.request_record()

            if not packet:
                print("Pachet invalid.")
                continue

            if self.analyze_protocol:
                debug_checksum(packet)

            reading = decode_record(packet)

            if reading is not None:
                print(reading)
                readings.append(reading)

        return readings
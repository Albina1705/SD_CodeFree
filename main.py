from protocol_v1 import SDCodefreeProtocol

meter = SDCodefreeProtocol("COM4", debug=True)

print("Conectare...")

meter.connect()

print("OK!")

meter.wait_handshake()

print("Handshake primit!")

meter.send_handshake()

print("Handshake trimis!")

count = meter.read_count()

print("Memorie:", count, "înregistrări")

for i in range(count):

    print(f"\n=== Înregistrarea {i+1}/{count} ===")

    meter.request_record()

    record = meter.fetch_record()

    print(record)

meter.close()

print("Memorie:", count, "înregistrări")

meter.close()

print("Port închis.")
def debug_checksum(packet):

    check = packet[-2]

    print(f"\nCHECK = {check:02X}")

    found = False

    for i in range(len(packet) - 2):
        s = sum(packet[i:-2]) & 0xFF

        if s == check:
            print(f"MATCH începe la byte {i}")
            found = True

    if not found:
        print("Nu s-a găsit nicio potrivire.")
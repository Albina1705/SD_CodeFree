"""
Instrumente pentru analiza protocolului SD CodeFree.

Aceste funcții NU sunt folosite de aplicația propriu-zisă,
ci doar pentru reverse engineering și depanare.
"""

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

def hexdump(packet, width=8):
    """
    Afișează conținutul unui pachet în format hexazecimal.
    """

    print("\nOffset  Hex")
    print("------  -------------------------------")

    for offset in range(0, len(packet), width):
        chunk = packet[offset:offset + width]
        hexbytes = " ".join(f"{b:02X}" for b in chunk)
        print(f"{offset:04X}    {hexbytes}") 

def analyze_record(packet):
    """
    Analizează payload-ul unui pachet RECORD.
    """

    if len(packet) < 21:
        print("Pachet prea scurt.")
        return

    data = packet[4:19]

    print("\n=== RECORD ANALYSIS ===")

    print(f"Payload : {' '.join(f'{b:02X}' for b in data)}")
    print()

    print(f"Year      : {2000 + data[1]}")
    print(f"Month     : {data[2]}")
    print(f"Day       : {data[3]}")
    print(f"Hour      : {data[4]}")
    print(f"Minute    : {data[5]}")
    print(f"Glucose   : {data[7]} mg/dL")
    print()

    print("Necunoscute:")
    print(f"data[0]   = {data[0]:02X}")
    print(f"data[6]   = {data[6]:02X}")
    print(f"data[8]   = {data[8]:02X}")
    print(f"data[9]   = {data[9]:02X}")
    print(f"data[10]  = {data[10]:02X}")
    print(f"data[11]  = {data[11]:02X}")
    print(f"data[12]  = {data[12]:02X}")
    print(f"data[13]  = {data[13]:02X}")
    print(f"data[14]  = {data[14]:02X}")    

    print(
        f"Flags: "
        f"data6={data[6]}  "
        f"data10={data[10]:02X}  "
        f"data12={data[12]}  "
        f"data13={data[13]:02X}"
    )

def analyze_dataset(packets):

    values = [set() for _ in range(15)]

    for packet in packets:
        data = packet[4:19]

        for i, value in enumerate(data):
            values[i].add(value)

    print("\n===== PAYLOAD ANALYSIS =====\n")

    for i, vals in enumerate(values):
        vals = sorted(vals)

        print(
            f"data[{i:2}] : "
            f"{len(vals):2} valori -> "
            + " ".join(f"{v:02X}" for v in vals)
        )               

def analyze_flags(packets):
    """
    Analizează câmpurile încă necunoscute din payload și
    afișează ce combinații apar în memorie.
    """

    print("\n===== FLAG ANALYSIS =====\n")

    fields = {
        0: {},
        6: {},
        8: {},
        9: {},
        10: {},
        11: {},
        12: {},
        13: {},
        14: {},
    }

    for packet in packets:
        data = packet[4:19]

        for index in fields:
            value = data[index]
            fields[index][value] = fields[index].get(value, 0) + 1

    for index in sorted(fields):
        print(f"data[{index}]:")

        for value, count in sorted(fields[index].items()):
            print(f"   {value:02X} -> {count}")

        print()        
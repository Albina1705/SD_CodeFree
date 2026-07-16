from serial.tools import list_ports


def find_serial_port():
    """
    Caută automat adaptorul USB-Serial.
    Returnează numele portului (ex. COM4) sau None.
    """

    ports = list_ports.comports()

    preferred = (
        "CP210",
        "Silicon Labs",
        "FT232",
        "FTDI",
        "CH340",
        "CH910",
        "USB Serial",
    )

    # întâi caută adaptoarele cunoscute
    for port in ports:
        description = port.description or ""

        if any(name.lower() in description.lower() for name in preferred):
            print(f"Adaptor găsit: {description} ({port.device})")
            return port.device

    # dacă există un singur port serial, îl folosim
    if len(ports) == 1:
        print(f"Singurul port disponibil: {ports[0].device}")
        return ports[0].device

    return None
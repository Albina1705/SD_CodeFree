# SD CodeFree Reader

Aplicație Python pentru citirea memoriei glucometrului SD CodeFree prin cablu USB-Serial.

## Funcții

- conectare la glucometru
- handshake automat
- descărcare completă a memoriei
- decodare dată/oră/glicemie
- export JSON
- export CSV

## Structura proiectului

main.py
protocol.py
decoder.py
constants.py
models.py
export_csv.py
output/

## Cerințe

Python 3.x

pip install pyserial

## Utilizare

python main.py
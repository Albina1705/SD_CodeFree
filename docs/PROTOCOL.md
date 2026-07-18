# SD CodeFree Communication Protocol

## Overview

This document describes the serial communication protocol used by the SD CodeFree blood glucose meter.

---

## Serial parameters

| Parameter | Value |
|-----------|-------|
| Baud rate | 38400 |
| Data bits | 8 |
| Parity | None |
| Stop bits | 1 |

---

## Handshake

### Meter → PC

53 20 04 10 30 20 AA

### PC → Meter

53 10 04 10 40 50 AA

---

## COUNT packet

Used to read the number of stored records.

Example:

53 20 18 30 00 44 AA AA AA AA AA AA AA AA AA AA AA AA AA AA AA AA AA AA AA DE AA

Meaning:

- Record count = 68

---

## RECORD packet

Payload length: **15 bytes**

| Offset | Description | Status |
|-------:|-------------|--------|
| 0 | Unknown | ❓ |
| 1 | Year (2000 + value) | ✅ |
| 2 | Month | ✅ |
| 3 | Day | ✅ |
| 4 | Hour | ✅ |
| 5 | Minute | ✅ |
| 6 | Unknown | ❓ |
| 7 | Glucose (mg/dL) | ✅ |
| 8 | Meal marker | ✅ |
| 9 | Unknown | ❓ |
| 10 | Unknown | ❓ |
| 11 | Unknown | ❓ |
| 12 | Unknown | ❓ |
| 13 | Unknown | ❓ |
| 14 | Unknown | ❓ |

### Meal marker

| Value | Meaning |
|------:|---------|
| 0x00 | Normal |
| 0x10 | Before meal |
| 0x20 | After meal |
| 0x30 | Control solution *(from manual, not experimentally confirmed)* |

---

## Checksum

Work in progress.

The checksum algorithm has not yet been fully identified.

---

## Status

Confirmed by experimental testing on SD CodeFree meters.

## Hardware

The protocol is independent of the USB-to-Serial adapter.

The following adapters have been successfully tested:

- CP2102
- CH340C
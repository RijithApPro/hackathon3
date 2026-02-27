# Challenge 3 – ARXML Watchdog Boilerplate

## Overview

This challenge provides an AUTOSAR R4.3-compatible ARXML boilerplate for a
**Watchdog Manager (WdgM)** software component and its integration with an
application component.

### What is ARXML?

ARXML (AUTOSAR XML) is the exchange format used by the AUTOSAR (AUTomotive
Open System ARchitecture) tool-chain to describe software components, their
interfaces, and compositions.

### What does the watchdog boilerplate contain?

| Element | Description |
|---------|-------------|
| `WdgM_AliveInterface` | Sender-Receiver interface carrying an 8-bit alive counter |
| `WdgM_TriggerInterface` | Client-Server interface with a `Trigger` operation |
| `WdgM_Component` | Atomic SWC with `WdgM_Init` and `WdgM_MainFunction` runnables |
| `App_Component` | Example application SWC supervised by WdgM |
| `WdgM_App_Composition` | Composition wiring WdgM ↔ App via the two interfaces |

### Watchdog supervision flow

```
App_MainFunction (every 10 ms)
  │  increments AliveCounter  ──────────►  WdgM reads AliveCounter
  │                                             │
  └──── calls Trigger ◄──────────────── WdgM_TriggerPort provided
```

## Files

| File | Purpose |
|------|---------|
| `watchdog.arxml` | Complete ARXML boilerplate |
| `arxml_utils.py` | Python helper to load/inspect the ARXML without a full AUTOSAR tool-chain |

## Inspect the boilerplate

```bash
python arxml_utils.py
```

Expected output:
```
Loaded: watchdog.arxml

Software Components (3):
  • App_Component
  • WdgM_App_Composition
  • WdgM_Component

Runnables (3):
  • App_MainFunction
  • WdgM_Init
  • WdgM_MainFunction
```

## Test

```bash
pytest test_arxml_watchdog.py
```

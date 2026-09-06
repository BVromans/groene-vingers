# Groene vingers — Architecture Overview

```text
Physical devices
      ↓
Raw sensor / integration layer
      ↓
Plant configuration / abstraction
      ↓
Plant state & measurements
      ├────────────→ Dashboard
      ↓
Watering events
      ↓
Learning / statistics / confidence
      ↓
Recommendation engine
      ↓
Safety layer
      ↓
Irrigation execution
```

## Separation of concerns

### Raw device layer
Knows Ecowitt, LinkTap, Rain Bird and other integrations. It should not know
that a sensor represents a particular plant.

### Plant abstraction layer
Maps stable plant slots to physical sensors and configuration.

Example:
```text
Plant 7
  name = Mandevilla
  sensor = Ecowitt sensor X
  location = Balcony
  target = 35%
  container_type = pot
  watering_method = irrigation
  irrigation_zone = 2
```

### Measurement layer
Provides normalized plant-level moisture, battery, health, target and trend.

### Event layer
Records watering observations independently of physical implementation.

The canonical event is one watering observation, regardless of whether the
water came from a manual action or a LinkTap zone. It should contain:

```text
event_id
plant_slots[]
zone_id
location
timestamp_started
timestamp_stopped
method
amount_ml
runtime_min
volume_l
moisture_before
moisture_after
moisture_delta
stabilization_min
weather_context
rain_context
sensor_health
confidence
notes
```

Required invariants:

- `moisture_delta = moisture_after - moisture_before`.
- `runtime_min` is the trusted irrigation quantity until LinkTap volume is
      physically calibrated.
- `volume_l` remains measured data with an explicit trust status; it must not
      silently become the learning input.
- A zone event may reference multiple plant slots. Unmonitored containers in
      the zone remain part of the zone context but do not receive invented plant
      measurements.
- Missing, stale or implausible measurements produce an incomplete or rejected
      learning event, not a zero-valued measurement.

Current zone measurement roles:

```text
Binnen / no irrigation zone
      slots: 1, 2, 3

Tuin / Zone 1
      tap_id: 58BF1A36004B1200_1
      measured slots: 4, 5, 8, 9

Balkon / Zone 2
      tap_id: 58BF1A36004B1200_2
      measured slots: 6, 7
      additional unmonitored containers: yes
```

The event model must preserve the distinction between the zone being watered,
the plant slots with measurements, and other unmonitored containers receiving
the same water.

Zone summaries are retained for historical comparison. New learning data is
also recorded as one sensor-specific row per measured plant slot, correlated by
one `event_id`. Sensor-specific deltas are primary learning data; zone delta is
an aggregate only.

### Learning layer
Calculates response, trends, confidence and outliers.

### Decision layer
Uses current state, learned behaviour, weather/rain and safety constraints.

### Execution layer
Starts/stops irrigation or records manual watering.

### Presentation layer
Dashboard only. Business logic should not live here.

## Key invariants
- A physical sensor can change without changing plant identity.
- A plant can be renamed without losing history.
- A plant can move without rewriting the automation engine.
- An irrigation controller can be replaced without rewriting the learning model.

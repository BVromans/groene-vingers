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

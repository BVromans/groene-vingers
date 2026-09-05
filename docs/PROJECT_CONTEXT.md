# Groene vingers — Project Context

## Purpose
Groene vingers is a Home Assistant system for intelligent plant monitoring,
irrigation and eventually self-learning irrigation decisions.

The long-term goal is to learn how individual plants and growing situations
respond to water and weather, then produce increasingly accurate and safe
recommendations and, only after sufficient validation, autonomous irrigation.

## Current environment
- Home Assistant runs on a NUC.
- VS Code is connected to the HA environment over SSH.
- The current development focus is Groene vingers.
- The installation will later contain other unrelated HA automations.
- The old configuration is a backup/reference, not something to restore blindly.
- Do not restore old `.storage` into the clean installation.

## Hardware / integrations

### Ecowitt
GW1200A gateways are used for soil monitoring.
Known historical gateway details:
- model: GW1200A
- firmware previously observed: GW1200A_V1.4.6
- 868 MHz
- upload interval about 60 seconds

A second gateway has been added and a ninth soil sensor is sending data.

Raw entities historically included names such as:
`sensor.gw1200a_soil_moisture_1`

Never hard-code raw Ecowitt entities into plant-specific automations. Use an
abstraction/mapping layer.

The Ecowitt webhook previously required a leading `/` in its path.

### Soil battery
Raw battery is voltage, not percentage. A previously useful approximation:
1.0 V ≈ 0%, 1.3 V ≈ 60%, 1.5 V ≈ 100%, clamped to 0–100%.
Keep raw voltage and derived percentage separate.

## Plants / locations

### Indoor
- Ficus
- Schefflera
- Strelitzia Nicolai

### Garden
- Rhododendron
- Acer Pixie
- Oleander

### Balcony
- Mandevilla
- Kweektafel
- additional balcony-bak sensor / ninth sensor

All plants are currently exposed to rain. Do not permanently hard-code the
balcony as sheltered. Rain exposure should be configurable if needed.

## Stable plant-slot architecture
Use stable logical plant slots (e.g. Plant 1–9) rather than plant names as
identity.

A slot can contain:
- plant name;
- assigned sensor;
- location;
- target moisture;
- container type;
- watering method;
- irrigation zone;
- learning enabled;
- rain exposure.

Sensor swapping should be a configuration/mapping change, not a YAML rewrite.
Plant renaming must preserve history. Moving a plant must be configuration.

## Logical layers
Keep these separated:
1. Raw sensor/integration layer
2. Plant configuration/abstraction
3. Measurement/state
4. Watering events
5. Learning/statistics
6. Recommendation/decision
7. Irrigation execution
8. Dashboard

Do not put business logic in dashboard cards.

## Watering event model
Treat manual and automated watering as the same generic event type.

Useful fields:
- plant
- zone
- timestamp
- method
- amount_ml
- runtime_min
- volume_l
- moisture_before
- moisture_after
- moisture_delta
- weather/rain context
- confidence
- sensor health
- notes

Core relationship:
`moisture_delta = moisture_after - moisture_before`

Until LinkTap volume is calibrated, use runtime as the more trustworthy input.

## Learning
Capture before, watering action, runtime/amount, weather/rain context,
stabilization period, after, delta and confidence.

A previous outdoor test used 45 minutes stabilization; keep this configurable.

Never let one observation silently redefine watering behaviour.

Distinguish:
- measured data;
- calculated values;
- learned values;
- recommendations;
- autonomous decisions.

Use confidence and outlier handling.

## Historical observations
These are starting knowledge, not immutable rules.

Mandevilla: relatively high water use and full sun; good learning candidate.

Strelitzia Nicolai: historically slow moisture loss and relatively sensitive to
overwatering.

Schefflera Gold Capella: medium response; one historical observation was about
22% → 28% after watering.

## Irrigation
Rain Bird + LinkTap are used.

A balcony zone historically had 15 drippers at about 2 L/h each:
theoretical flow ≈ 30 L/h, so 15 min ≈ 7.5 L and 30 min ≈ 15 L.
These are theoretical, not measured values.

### LinkTap measurement issue
LinkTap previously reported implausibly low volumes:
- ~15 min → 0.88 L
- ~30.1 min → 0.84 L

Physical inspection showed actual water flow. Therefore runtime is currently
more trustworthy than reported volume. Do not use current volume readings as
high-confidence learning data until a physical calibration is performed.

## Kweektafel lesson
Water can flow and drain without the sensor showing a meaningful moisture rise.
A historical setup had the sensor about 15 cm from drippers, with 2×2 L/h for
strawberries and 1×2 L/h for raspberry.

Possible causes include distribution, sensor placement, drainage or substrate.
Do not assume "water ran" means "sensor moisture increased".

## Reservoir containers
Some reservoir boxes retained about 2 cm water after irrigation. A topsoil
sensor only tells part of the story. `container_type` must distinguish
reservoir/self-watering systems where relevant.

## Weather
Historically:
- Buienradar for local/short-term rain;
- KNMI for forecast, temperature, wind and warnings.

A first-pass weather stress heuristic was approximately:
temperature × 2 + (100 - humidity) × 0.6 + wind × 1.5, clamped to 0–100.
This is a heuristic, not validated plant science.

Historical rain thresholds:
- <1 mm ignore;
- 1–3 mm reduce;
- >4 mm skip;
- >8 mm hard skip.

Keep these configurable. Do not treat them as universal truth.

## Safety
Before autonomous irrigation:
- minimum/maximum moisture;
- maximum runtime;
- maximum daily irrigation;
- minimum interval;
- rain skip/reduction;
- sensor health/stale data;
- irrigation controller health;
- sufficient learning confidence.

If required data is unavailable or implausible, fail safely.

Default mode should be advisory/learning, not autonomous.

## Sensor health
Eventually distinguish:
- healthy;
- stale;
- unavailable;
- low battery;
- implausible reading;
- abnormal jump.

Bad sensor data must not silently become learning truth.

## Dashboard
Preferred sections:
- Binnen
- Tuin
- Balkon

Plant cards should show moisture, target, battery, status, trend, last watering
and learning/delta where useful. Outdoor cards may also show runtime, trusted
volume and irrigation state.

Mushroom is preferred for visual cards. ApexCharts can be used for detailed
history/learning graphs. Keep business logic out of dashboards.

## HACS
Useful candidates:
- Mushroom
- ApexCharts Card
- possibly auto-entities
- possibly layout-card
- possibly card-mod

Do not install components just because they exist. Functionality first, styling
later.

## Legacy lessons
The previous system accumulated too many plant-specific helpers/entities and
duplicate automations, causing orphaned entities, stale storage and fragile
templates.

Avoid patterns such as:
`input_number.ficus_last_water`
`automation.ficus_water`
when generic event/plant architecture can handle the same requirement.

Handle unknown/unavailable numeric states safely.

## Development phases
1. Preserve backup/reference
2. Clean HA base
3. Verify integrations
4. Verify raw Ecowitt sensors
5. Sensor abstraction
6. Plant-slot configuration
7. Battery conversion
8. Moisture/target
9. Dashboard
10. Manual watering logging
11. Irrigation event logging
12. Before/after measurement
13. Weather/rain context
14. Learning statistics/confidence
15. Recommendations
16. Autonomous irrigation only later

Validate between phases.

## Decision rules
When several solutions are valid, prefer the one that:
- keeps stable logical identities;
- separates devices from plants;
- is generic/reusable;
- preserves history;
- is testable and observable;
- fails safely;
- scales to more plants/sensors/zones;
- does not require rewrites when sensors are swapped, plants renamed or moved.

## Future HA expansion
Groene vingers is a module, not the whole HA installation. Keep plant-specific
business logic isolated from future energy, network, media, climate, security
and household modules.

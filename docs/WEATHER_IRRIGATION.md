# Groene vingers - Weather and Irrigation Design

## Purpose and safety boundary
This document defines the provider-independent weather design for Groene
vingers. Weather data supports advisory and learning decisions first. Missing,
stale, unavailable or unverified safety-relevant weather data must prevent
autonomous outdoor irrigation rather than silently receive a default value.

## Physical weather hardware

### Ecowitt gateway 1
`GW1200A-EJS60` has soil sensors 1-8 and the physical rain gauge. The rain
gauge is installed in a representative location and is not under cover.

Canonical measured-rain entities:

- `sensor.gw1200a_rain_rate`
- `sensor.gw1200a_hourly_rain`
- `sensor.gw1200a_24h_rain`
- `sensor.gw1200a_event_rain`
- `sensor.gw1200a_daily_rain`
- `sensor.gw1200a_weekly_rain`
- `sensor.gw1200a_monthly_rain`
- `sensor.gw1200a_total_rain`

Ecowitt gateway environment values, including `tempinc` and `humidityin`, are
not outdoor-weather inputs and must not be used for irrigation decisions.

### Ecowitt gateway 2
`GW1200A-EJS60-2` currently has soil sensor 9 only. It is reserved for future
soil-sensor expansion. Its duplicated rain and gateway-environment entities are
not inputs to the current weather model.

### Future local outdoor climate sensor
A future Ecowitt outdoor temperature/humidity sensor will become the preferred
source for current local outdoor temperature and humidity after its placement,
entity IDs and update behaviour are verified.

## Registered Home Assistant weather entities
The following entities were found in the entity registry. Registry presence does
not prove that an entity is enabled, current or suitable for autonomous use.
Live state and update-age validation remains required before implementation.

| Source | Entity | Data | Kind | Unit | Intended use |
| --- | --- | --- | --- | --- | --- |
| Ecowitt 1 | `sensor.gw1200a_rain_rate` | Rain intensity | measured | mm/h | Primary local rain intensity |
| Ecowitt 1 | `sensor.gw1200a_hourly_rain` | Rain in last hour | measured | mm | Primary local rain history |
| Ecowitt 1 | `sensor.gw1200a_24h_rain` | Rain in last 24 hours | measured | mm | Primary local rain history |
| Ecowitt 1 | `sensor.gw1200a_event_rain` | Rain event total | measured | mm | Rain-event context |
| Ecowitt 1 | `sensor.gw1200a_daily_rain` | Daily rain | measured | mm | Supporting local history |
| KNMI | `sensor.home_temperature` | Temperature | provider current/unknown | C | Candidate primary outdoor temperature |
| KNMI | `sensor.home_humidity` | Humidity | provider current/unknown | % | Candidate primary outdoor humidity |
| KNMI | `sensor.home_wind_speed` | Wind speed | provider current/unknown | km/h | Candidate primary wind speed |
| KNMI | `sensor.home_solar_irradiance` | Solar irradiance | provider current/unknown | W/m2 | Candidate primary solar context |
| KNMI | `sensor.home_min_temperature_tomorrow` | Tomorrow minimum temperature | forecast | C | Candidate frost gate |
| KNMI | `sensor.home_max_temperature_tomorrow` | Tomorrow maximum temperature | forecast | C | Supporting seasonal context |
| KNMI | `sensor.home_precipitation_today` | Precipitation probability | forecast | % | Supporting rain forecast context |
| KNMI | `sensor.home_precipitation_tomorrow` | Precipitation probability | forecast | % | Supporting rain forecast context |
| KNMI | `binary_sensor.knmi_warning` | Weather warning | provider warning | boolean | Candidate safety gate |
| Buienradar | `sensor.precipitation_intensity` | Precipitation intensity | provider current/unknown | mm/h | Secondary local rain context |
| Buienradar | `sensor.rain_last_hour` | Rain in last hour | provider current/unknown | mm | Secondary rain history |
| Buienradar | `sensor.rain_last_24h` | Rain in last 24 hours | provider current/unknown | mm | Secondary rain history |
| Buienradar | `sensor.precipitation_forecast_average` | Forecast precipitation intensity | forecast | mm/h | Candidate short-term rain forecast |
| Buienradar | `sensor.precipitation_forecast_total` | Forecast precipitation total | forecast | mm | Candidate short-term rain forecast |
| Buienradar | `sensor.temperature` | Temperature | provider current/unknown | C | Temperature fallback |
| Buienradar | `sensor.humidity` | Humidity | provider current/unknown | % | Humidity fallback |
| Buienradar | `sensor.wind_speed` | Wind speed | provider current/unknown | km/h | Wind-speed fallback |
| Buienradar | `sensor.wind_direction` | Wind direction | provider current/unknown | text | Context only |
| Buienradar | `sensor.wind_direction_azimuth` | Wind direction | provider current/unknown | degrees | Context only |
| Buienradar | `sensor.irradiance` | Irradiance | provider current/unknown | W/m2 | Solar-context fallback |
| Met.no | `weather.forecast_home` | Forecast object | forecast | n/a | General forecast fallback |

The registry also contains Buienradar daily forecast entities for days 1-5,
including temperature, minimum temperature, rain, minimum/maximum rain,
rain chance, wind speed and direction. They are not part of the first normalized
weather layer until their live state and forecast horizon are verified.

## PWS Weather status
No PWS Weather, Weather Underground, Wunderground or Personal Weather Station
config entry, device or entity was found. The local Ecowitt rain gauge is
available through the built-in Ecowitt integration, not through PWS Weather.

## Source-of-truth policy

| Weather data | Primary source | Fallback | Autonomous behaviour if unavailable |
| --- | --- | --- | --- |
| Current local rain and rain rate | Ecowitt gateway 1 | None | Do not make rain-based autonomous decision |
| Rain in last hour and 24 hours | Ecowitt gateway 1 | Buienradar after live validation | Do not make rain-based autonomous decision |
| Outdoor temperature | KNMI after live validation | Buienradar, then Met.no | Block autonomous outdoor irrigation if frost safety depends on it |
| Outdoor humidity | KNMI after live validation | Buienradar | Keep advisory-only or reduce confidence |
| Wind speed | KNMI after live validation | Buienradar | Keep advisory-only or reduce confidence |
| Wind direction | Buienradar after live validation | None | Context only |
| Solar irradiance | KNMI after live validation | Buienradar | Context only |
| Short-term rain forecast | Buienradar after horizon validation | Met.no or KNMI context | Do not automatically skip irrigation |
| Forecast minimum temperature | KNMI after live validation | Buienradar daily minimum | Block autonomous outdoor irrigation |
| Weather warning | KNMI after live validation | None | Block autonomous outdoor irrigation |

## Normalized weather model
Plant and irrigation logic must consume provider-independent normalized entities
rather than provider-specific IDs. The initial advisory model is:

```text
weather_current_temperature
weather_current_humidity
weather_current_wind_speed
weather_current_wind_direction
weather_current_solar_irradiance
weather_rain_rate
weather_rain_last_1h
weather_rain_last_24h
weather_forecast_rain_next_6h
weather_forecast_rain_next_24h
weather_forecast_min_temperature
weather_warning
weather_effective_rain
weather_frost_risk
weather_season
weather_source_health
```

`weather_rain_last_6h` and `weather_rain_last_48h` are deferred until they can
be calculated from reliable measured-rain history. They must not be inferred
from a forecast.

## Effective rain
Effective rain is an advisory classification, not a conversion from millimetres
to irrigation runtime.

Initial inputs:

- measured local rain amount and rain rate;
- rain exposure of the plant/container;
- container type, drainage and substrate;
- moisture before rain or irrigation;
- moisture response after the event;
- temperature and wind where verified.

Initial rules:

- Missing local measured rain produces `unknown` effective rain.
- Low rain amount may be ignored only as an advisory heuristic.
- Brief high-intensity rain receives lower infiltration confidence than steady
  rain.
- High existing moisture raises overwatering risk but does not prove deep root
  moisture.
- A missing moisture increase is not proof that water was ineffective,
  especially for the kweektafel.
- Per-sensor moisture deltas are primary learning evidence; zone averages are
  summaries only.

## Watering windows
Watering windows are decision windows, not watering schedules.

| Window | Role |
| --- | --- |
| 05:00-09:00 | Primary decision window |
| 19:00-22:00 | Secondary decision window |
| Other times | Avoid unless an explicit future safety/stress exception allows it |

Morning is preferred because it gives water availability before warmer drying
conditions while avoiding routine late-night wetness. A decision inside a window
remains `WATER`, `WAIT` or `SKIP` based on measurements, weather, season,
recent watering and safety gates.

## Seasonal and frost model
Initial regimes:

```text
SPRING
SUMMER_HIGH_DEMAND
AUTUMN_TRANSITION
WINTER
```

Calendar period is only a baseline. The eventual regime uses temperature trend,
forecast minimum temperature, measured rain, solar context, dryback and learned
plant response.

For autonomous outdoor irrigation, the first conservative frost gate is:

```text
forecast minimum temperature unavailable -> block
forecast minimum temperature <= 2 C -> block
weather warning active -> block or advisory-only
winterization state is WINTERIZED -> block
```

## Winterization state

```text
NORMAL
WINTER_PREP
WINTERIZED
```

`WINTERIZED` blocks autonomous outdoor irrigation. Physical winterization is a
manual procedure: close the water supply, protect or remove LinkTap as required
by its manufacturer, drain lines, manifolds and drippers, and confirm the
physical state before setting the logical state.

## Learning-event weather context
Future per-sensor irrigation records should snapshot the following at event
start and completion where available:

```text
event_id
zone_id
plant_slot
rain_rate
rain_last_1h
rain_last_24h
forecast_rain
current_temperature
current_humidity
wind_speed
solar_irradiance
forecast_min_temperature
season
frost_risk
weather_source_health
sensor_health
confidence
```

Runtime remains the trusted irrigation quantity until LinkTap volume is
physically calibrated. Weather context must be stored with the event, not
reconstructed later from current weather state.

## Implementation order

1. Completed: verify Ecowitt measured-rain and selected KNMI entities as
  enabled/current. Buienradar precipitation/irradiance and KNMI solar
  irradiance remain disabled and unverified.
2. Completed: implement an advisory-only normalized weather layer using the
  verified Ecowitt and KNMI entities. Unverified fields remain `unknown`.
3. Verify forecast horizon before mapping any provider forecast value to a
  normalized 6-hour or 24-hour field.
4. Persist reliable measured-rain history for 6-hour and 48-hour calculations.
5. Implement effective-rain and frost classifications as advisory values.
6. Add weather snapshots to new per-sensor learning events.
7. Add dashboard observability for source health and advisory decisions.
8. Consider autonomous watering only after enough validated events, physical
   winterization controls and complete safety gates exist.

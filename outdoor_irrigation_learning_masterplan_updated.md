# Outdoor Irrigation Intelligence — Masterplan

# Doel

We gaan jouw bestaande Home Assistant + LinkTap + moisture sensor setup uitbreiden naar een volledig zelflerend irrigatieplatform.

Het systeem moet uiteindelijk:

- automatisch runtime per zone optimaliseren
- leren hoeveel vocht een runtime toevoegt
- rekening houden met regenverwachting
- irrigatie skippen bij aankomende regen
- inefficiënte druppelaars detecteren
- advies geven over:
  - langere/kortere runtime
  
  - extra druppelaars
  - 2L/u vs 4L/u
  - sensorplaatsing
  - drainage
- seizoensverschillen leren
- verschillende substraten leren
- historische trends analyseren

---

# Huidige setup

Dashboard status bevestigd via huidige Home Assistant dashboard export.

Belangrijke verduidelijking:

- Zone 1 = alleen tuin
- Zone 2 = balkon + potten + kweektafel

Zone 2 bevat dus:
- deels overdekt
- deels regenblootstelling
- verschillende substraten
- verschillende potgroottes
- verschillende verdampingssnelheden

Dit verschil wordt later expliciet meegenomen in weather learning.

---

# Sensorarchitectuur

## Zone 1 — Tuin

### Sensor 4
Primary learning sensor.

Locatie:
- Rhododendron / Dahlia XXL omgeving

Doel:
- representatieve high-water-demand referentie
- snelle respons
- early-warning sensor

### Sensor 5
Protection sensor.

Locatie:
- Acer Pixie

Doel:
- bescherming tegen overwatering
- monitoring gevoelige wortelzone
- bewust iets verder van druppelaar geplaatst

### Sensor 8
Protection sensor.

Locatie:
- Oleander

Doel:
- losse pot zonder reservoir
- snelle dryback detectie
- hoge zomervraag
- afwijkende hydrauliek t.o.v. tuin

---

## Zone 2 — Balkon

### Sensor 7
Primary learning sensor.

Locatie:
- midden tussen aardbei en framboos in kweektafel

Doel:
- stabiele referentiesensor
- collectieve root-zone monitoring
- ideale weather-learning sensor
- rain-exposed benchmark

### Sensor 6
Protection/reference sensor.

Locatie:
- Mandevilla + petunia’s onder afdak

Doel:
- covered irrigation benchmark
- regen-onafhankelijke learning
- drought stress monitoring

---

# Architectuur straks

## Runtime learning

LinkTap runtime
+
water volume
+
moisture delta
+
weather
=
learning dataset

---

# FASE 1 — Outdoor Foundation

# Stap 1 — LinkTap integratie

STATUS:

DONE

Beschikbare entities:

- switches
- valves
- runtime sensors
- flow sensors
- volume sensors
- watering state
- leak/clog detection

---

# Stap 2 — Outdoor helpers

We maken helpers voor:

## Zone Tuin

- moisture_before
- waiting_for_delta
- last_runtime
- last_volume
- learning_enabled

## Zone Balkon

- moisture_before
- waiting_for_delta
- last_runtime
- last_volume
- learning_enabled

---

# Stap 3 — Outdoor logging automations

Bij start watering:

Opslaan:

- moisture before
- runtime target
- timestamp
- volume before

Bij einde watering:

Start learning timer.

Na X minuten:

Opslaan:

- moisture after
- moisture delta
- runtime
- liters
- flow rate
- zone
- timestamp

Alles wordt geschreven naar:

/config/outdoor_learning_log.csv

---

# Stap 4 — Outdoor Python analytics

Nieuwe parser:

analyze_outdoor_log.py

Deze leert:

- moisture increase per minute
- moisture increase per liter
- runtime efficiency
- flow efficiency
- zone performance
- drainage speed

---

# FASE 2 — Predictive Irrigation

# Runtime prediction

Systeem leert:

"Hoeveel minuten nodig om target moisture te bereiken?"

Voorbeeld:

- huidige moisture = 24%
- target = 32%
- historical runtime efficiency = 0.8% per minuut

→ advies:

10 minuten runtime

---

# Dynamische runtime adviezen

Per zone:

- aanbevolen runtime
- aanbevolen liters
- confidence score
- historical accuracy

---

# FASE 3 — Plant Intelligence

# Doel

Het systeem moet leren welke planten:

- sneller uitdrogen
- meer water nodig hebben
- minder efficiënt irrigeren
- te weinig druppelaars hebben
- last hebben van drainage

---

# Plant-specific modelling

Voorbeelden:

## Framboos

- hoog waterverbruik
- diepere wortels
- tragere sensorrespons

## Aardbei

- oppervlakkige wortels
- snelle vochtrespons
- gevoelig voor oversaturatie

## Balkonpotten

- sterk afhankelijk van:
  - zon
  - wind
  - potvolume
  - substraat

---

# FASE 4 — Weather Intelligence

# Weerintegratie

We gaan toevoegen:

- regenverwachting
- temperatuur
- evapotranspiratie
- luchtvochtigheid
- wind
- zonbelasting

---

# Rain Skip Logic

Voorbeeld:

"Sla irrigatie over als binnen 6 uur meer dan 4 mm regen valt"

OF:

"Verlaag runtime met 40% als regen binnen 3 uur verwacht wordt"

---

# Dynamische thresholds

Niet vaste regels.

Systeem leert:

- hoeveel regen effectief helpt
- verschil tussen lichte regen en langdurige regen
- effect van zomer/winter

---

# FASE 5 — Advanced Irrigation Intelligence

# Detectie van inefficiëntie

Systeem detecteert:

- verstopte druppelaars
- lekkage
- sensor mismatch
- overwatering
- drainageproblemen
- slechte sensorlocatie

---

# Adviessysteem

Voorbeelden:

"Zone balkon reageert traag op irrigatie"

"Overweeg extra 2L/u druppelaar bij Oleander"

"Kweektafel houdt vocht langer vast bij lage temperaturen"

"Balkon runtime kan met 20% omlaag bij bewolkt weer"

---

# FASE 6 — Frequency Intelligence

Het systeem leert:

- dry-back curves
- optimale irrigatiefrequentie
- lange vs korte droogcycli
- recovery speed
- time-above-target
- time-below-target

Voorbeelden:

- Oleander prefereert diepere droog/nat cycli
- Rhododendron prefereert stabieler vocht
- Kweektafel reageert beter op langere intervallen

---

# FASE 7 — Seizoensleren

Het systeem leert:

- zomer vs winter
- warm vs koud
- droog vs vochtig
- zonnige periodes
- regenperiodes

---

# Uiteindelijk einddoel

Volledig autonoom irrigatiesysteem:

- moisture gestuurd
- weather aware
- self learning
- predictive
- runtime optimalisatie
- waterbesparing
- plantgezondheid optimalisatie

---

# Implementatievolgorde

1. Outdoor helpers
2. Outdoor automations
3. Outdoor CSV logging
4. Outdoor Python analytics
5. Runtime prediction
6. Dashboard uitbreiding
7. Weather integration
8. Rain skip automations
9. Advanced learning
10. Frequency intelligence
11. Seasonal intelligence

---

# Belangrijke ontwerpprincipes

## Veiligheid

- nooit blind automatisch runtime verhogen
- altijd max runtime limieten
- fail-safe irrigatie
- leak detection actief

## Betrouwbaarheid

- averages gebruiken
- filtering van slechte metingen
- meerdere samples nodig voor learning

## Modulariteit

- binnen en buiten gescheiden
- Python analytics los van HA
- CSV logging eenvoudig backupbaar

## Onderhoudbaarheid

- standaard HA architectuur
- minimale custom dependencies
- duidelijke YAML structuur
- makkelijk uitbreidbaar
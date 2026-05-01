import csv
import json
from collections import defaultdict

results = defaultdict(list)

with open('/config/water_learning_log.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)

    for row in reader:
        if len(row) < 7:
            continue

        timestamp, plant, before, after, delta, water, method = [x.strip() for x in row]

        try:
            delta = float(delta)
            water = float(water)

            if water > 0:
                efficiency = (delta / water) * 100
                results[plant].append(efficiency)

        except:
            pass

output = {}

for plant, values in results.items():
    if len(values) > 0:
        avg = round(sum(values) / len(values), 2)

        output[plant] = {
            "samples": len(values),
            "avg_efficiency": avg
        }

print(json.dumps(output))
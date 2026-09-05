#!/usr/bin/env python3
"""Summarize outdoor irrigation events without trusting LinkTap volume."""

from __future__ import annotations

import csv
import json
import math
import sys
from collections import defaultdict
from pathlib import Path

DEFAULT_LOG = Path("/config/outdoor_learning_log.csv")


def as_float(value: str) -> float | None:
    try:
        number = float(value.strip())
    except (TypeError, ValueError):
        return None
    return number if math.isfinite(number) else None


def analyze(path: Path) -> dict[str, object]:
    grouped: defaultdict[str, list[dict[str, float]]] = defaultdict(list)

    if not path.exists():
        return {}

    with path.open(newline="", encoding="utf-8", errors="replace") as log_file:
        for row in csv.reader(log_file):
            if len(row) < 7:
                continue

            timestamp, zone, before, after, delta, runtime, volume = (
                value.strip() for value in row[:7]
            )
            before_value = as_float(before)
            after_value = as_float(after)
            delta_value = as_float(delta)
            runtime_value = as_float(runtime)
            volume_value = as_float(volume)

            if (
                not zone
                or before_value is None
                or after_value is None
                or delta_value is None
                or runtime_value is None
                or runtime_value <= 0
            ):
                continue

            # Keep the logged delta as measured data, but calculate the same
            # relationship from before/after so inconsistent rows are visible.
            measured_delta = round(after_value - before_value, 3)
            event = {
                "delta": delta_value,
                "measured_delta": measured_delta,
                "runtime_min": runtime_value,
            }
            if volume_value is not None and volume_value >= 0:
                event["volume_l"] = volume_value
            grouped[zone].append(event)

    result: dict[str, object] = {}
    for zone, events in grouped.items():
        runtime_rates = [event["delta"] / event["runtime_min"] for event in events]
        volume_observations = [
            event["volume_l"] for event in events if "volume_l" in event
        ]
        delta_mismatches = [
            event
            for event in events
            if abs(event["delta"] - event["measured_delta"]) > 0.1
        ]

        result[zone] = {
            "samples": len(events),
            "avg_delta": round(sum(event["delta"] for event in events) / len(events), 3),
            "avg_delta_per_min": round(sum(runtime_rates) / len(runtime_rates), 4),
            "reported_volume_samples": len(volume_observations),
            "avg_reported_volume_l": (
                round(sum(volume_observations) / len(volume_observations), 3)
                if volume_observations
                else None
            ),
            "volume_trust": "untrusted_until_calibrated",
            "delta_mismatch_samples": len(delta_mismatches),
        }

    return result


def main() -> None:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_LOG
    print(json.dumps(analyze(path), separators=(",", ":"), sort_keys=True))


if __name__ == "__main__":
    main()

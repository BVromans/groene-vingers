# Copilot Instructions — Home Assistant

Follow `AGENTS.md` as the primary project-wide guidance.

Before non-trivial changes:
- inspect existing configuration;
- search for existing entities/helpers/automations;
- avoid duplicates;
- prefer generic reusable solutions;
- preserve historical data;
- do not edit `.storage` unless explicitly requested;
- validate configuration after YAML changes;
- never claim tests were performed when they were not.

For consequential automations, preserve safety limits, sensor-health checks,
minimum intervals and maximum runtime/amount limits.

When working on Groene vingers, read `docs/PROJECT_CONTEXT.md`.

The Home Assistant installation will later contain other unrelated
automations, so do not make general HA architecture dependent on Groene vingers.

Use:
INSPECT → PLAN → IMPLEMENT → VALIDATE → TEST → REPORT
# Home Assistant Project — Agent Instructions

## Scope
This is a Home Assistant configuration. It currently focuses heavily on
**Groene vingers**, but the installation will also contain unrelated
automations and integrations in the future. These are general HA engineering
rules; Groene vingers-specific rules belong in `docs/PROJECT_CONTEXT.md`.

## Core principles
Priorities:
1. Safety and correctness.
2. Maintainability and clarity.
3. Reusability and generic architecture.
4. Observability and debuggability.
5. Reversibility.
6. Minimal unnecessary complexity.

Do not optimize for the fewest lines of YAML. Optimize for a system that can
still be understood and safely modified months later.

## Before changing anything
For every non-trivial change:
1. Inspect relevant existing configuration.
2. Search for existing entities, helpers, scripts, automations and integrations.
3. Understand dependencies before modifying or deleting anything.
4. Prefer extending/refactoring an existing generic component over duplicates.
5. Briefly state the approach before a large architectural change.

Never assume an entity/helper/automation does not exist because it was not in
the first file inspected.

## Avoid duplication
Avoid one automation/helper per plant when generic logic can handle all plants.
Avoid duplicate sensors and repeated YAML when reusable abstractions are
possible.

## Entity IDs
Use stable, meaningful entity IDs. Do not make a user-facing name the
fundamental identity when it may later change. Renaming a plant, room or label
should not fragment its history.

## Templates
Home Assistant states can be `unknown` or `unavailable`. Numeric templates
must handle invalid states safely. Bad sensor data must not silently cause
dangerous actions.

## Safety-critical automations
For water, heating, electricity, locks, alarms and similar actions:
- use explicit safety limits;
- check sensor health;
- enforce minimum intervals where appropriate;
- enforce maximum duration/amount;
- fail safely when required data is unavailable;
- do not make autonomous decisions from a single anomalous observation;
- keep manual override possible.

Never remove a safety condition merely to make an automation work.

## Configuration
Do not manually edit `.storage` unless explicitly requested and understood.
Do not restore old `.storage` into a clean HA installation.
Do not delete historical learning data or entities merely to clean things up.
Explain destructive changes before making them.

## Validation
After YAML/config changes:
1. Validate syntax/configuration where possible.
2. Check referenced entity IDs.
3. Consider unknown/unavailable states.
4. Review triggers and conditions.
5. Check for duplicates/conflicts.
6. Report what was tested and what still needs manual testing.

Never claim a test was performed when it was not.

## Development workflow
For substantial changes:
**INSPECT → PLAN → IMPLEMENT → VALIDATE → TEST → REPORT**

Prefer small, independently testable changes. Do not mix unrelated refactors
with functional changes without a clear reason.

## Documentation
Document important architectural decisions in `docs/`. If deliberately
departing from an existing rule, explain why.

## Groene vingers
When working on Groene vingers, read `docs/PROJECT_CONTEXT.md`.

## Future modules
Keep Groene vingers logically separate from future domains such as energy,
network, media, climate, security or household automation. Share generic
infrastructure only when appropriate.

## Reporting
When reporting a change, include:
- what changed;
- why;
- files affected;
- entities/helpers/automations affected;
- validation performed;
- manual tests still required;
- notable risks/follow-up items.

Ask before implementing if ambiguity could materially affect architecture or
safety.

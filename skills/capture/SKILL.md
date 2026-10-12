---
name: capture
description: >
  Capture a specification or a design against an OTO pack: the pack's capture schema says which
  questions to ask, by whom, and which items with which fields and links each needs; the person
  answers, confirms a section, and the section becomes facts in the knowledge base through the
  curate gates. Guided interview, or structure-from-notes. Use when Atlas specifies or designs,
  or when the user wants to capture a PRD, an architecture, requirements, personas, journeys,
  policies, decisions, components or any section of a product against a pack.
---

# Capture against a pack

The pack knows what to ask. OTO's **capture-form** skill asks it: it reads `capture.json`, takes
the questions group by group, and sends every confirmed group through the curate gates. Run it;
this skill adds the studio's way of running it. You are a facilitator and a peer; never invent
content the person has not confirmed.

## Which form

The packs to capture against are the ones the project composes (`project.config.json`,
`ontology`): for a specification, `product` and `product-<type>`; for a design, `ddd` (which
brings `software-architecture`). The capture file's `scope` is the product, so its `FR1` stays
apart from another product's.

## The studio's confirmation: the BMAD menu

Where capture-form drafts a group's items and asks the person to confirm, offer the menu the
studio has always used:

**[A] Advanced elicitation · [P] Perspectives · [C] Continue & contribute**

- **A**: probe deeper: edge cases, missing actors, weak measures, counter-examples.
- **P**: re-examine from the other askers the form names (the data team, compliance…).
- **C**: contribute the group through capture-form's gates, then the next question.

Only contribute on **C**. Atlas decides when `oto curate apply` closes a candidate.

## Hand-off

When the specification's sections are captured, Atlas moves to scene 3 (OTO's **start** on the
specification, then **ontology-interview**). When the design's are, to the flow. The site
(`prd-site`) is a view the engine fills from the graph on every build; nobody edits its data.

## Guardrails

capture-form's guardrails hold (the form is the schema, never fill `validated_by`, never invent).
On top of them:

- **No implementation leakage in a specification; decision-first in a design.**
- **Measurable:** a criterion has a metric, a baseline, a target, a date; "fast" is not a value.

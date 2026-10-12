---
name: architecture-build
description: >
  Design the solution as a knowledge base: captures the architecture against
  `software-architecture` through the elicit skill — context and drivers, ADRs, systems,
  components, interfaces, data stores, environments — then each part with the design pattern it
  follows (DDD's bounded contexts, aggregates and events through `ddd`; a data pipeline's layers
  through its pack), every component traced to the requirement it satisfies, every decision
  recorded with its alternatives. Use when the user wants to design or extend the architecture,
  record an ADR as the decision is made, or model a part's domain or pipeline. Writing up an ADR
  or a design brief from decisions already in the graph is OTO's spec.
---

# Build the architecture

The design level of the knowledge base: how the solution is shaped to do what the specification
says. Captured against packs, cross-linked to the specification by relations, not conventions.
The architecture itself assumes no pattern; each part of it may follow one, and one product may
use several (DDD for an application, a medallion pipeline for its data).

1. The project holds `software-architecture`: this pack embeds it, on `product` (Atlas's scene 1
   started the project from the pack), with the pattern each part follows merged beside it
   (`--ontology product-<type>,ddd,flow`). `oto ontology capture` writes the form.
2. **The architecture, pattern-neutral.** Run the **elicit** skill with the schema of that
   project. Its askers are the architect, the on-call engineer, the data owner, the risk owner,
   the builder, compliance; its items are systems, components, interfaces, data stores,
   environments, teams, runbooks, repositories, and the links that make the design traceable: a
   system or a component `satisfies` a requirement (SA17 says what is left), a decision is
   `about` what it shaped, a risk `threatens` an asset. An external source is a `System` another
   team owns, with the `Interface` it exposes (an API, a file feed, a database view). The
   people, the requirements, the policies, the scenarios, the terms, the decisions and the open
   questions are the product's: never captured twice.
3. **Each part, with its pattern.** Ask which parts follow which pattern; a pattern's ontology
   must be in the project (scene 1). For a part designed with **DDD** (`ddd`): subdomains,
   bounded contexts and their map, use cases, events, commands, reactions, read models, external
   systems, aggregates, entities, value objects, business rules, domain services; a context is
   `deployed_as` the component that runs it, a use case `satisfies` a requirement (DD24 says what
   is left). A part with no pattern is designed at step 2 only.
4. Decision-first: an ADR is captured with its alternatives and consequences before the
   components it shapes; a component with no decision behind it is a finding (`kg_policy`).

What this skill no longer does: keep its own section list, write `window.__ARCH__`, or assume
that every product is designed with DDD.
